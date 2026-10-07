import os
import json
import time
import uuid
from flask import Flask, render_template, request, jsonify
from google import genai
from google.genai import types

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
AUDIO_DIR = os.path.join(BASE_DIR, "static", "audio")
CUSTOM_VOICES_FILE = os.path.join(BASE_DIR, "custom_voices.json")
os.makedirs(AUDIO_DIR, exist_ok=True)

# Load API Key from .env or environment variable
def get_api_key():
    api_key = os.environ.get("GEMINI_API_KEY")
    env_file = os.path.join(BASE_DIR, ".env")
    if not api_key and os.path.exists(env_file):
        with open(env_file, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("GEMINI_API_KEY="):
                    api_key = line.strip().split("=", 1)[1].strip("\"' ")
                    break
    return api_key

# Prebuilt voices metadata
PREBUILT_VOICES = [
    {"id": "Iapetus", "name": "Iapetus", "gender": "男性 (20代)", "tone": "爽やか・明瞭・好青年", "desc": "ハキハキとした20代の爽やかな青年声。解説や案内、好印象なトークに最適", "is_custom": False},
    {"id": "Achird", "name": "Achird", "gender": "男性 (20代)", "tone": "親しみ・温かみ・日常会話", "desc": "親しみやすく温かい20代の日常会話・Vlog風ボイス。友達感覚の語りかけに最適", "is_custom": False},
    {"id": "Umbriel", "name": "Umbriel", "gender": "男性 (20代)", "tone": "リラックス・自然体", "desc": "落ち着いたトーンの20代青年声。ゆったりとしたレビューや雑談に最適", "is_custom": False},
    {"id": "Sadachbia", "name": "Sadachbia", "gender": "男性 (20代)", "tone": "表情豊か・活気・アニメ調", "desc": "抑揚豊かで明るい20代の男性声。アニメキャラクターや楽しいトークに最適", "is_custom": False},
    {"id": "Puck", "name": "Puck", "gender": "男性 (20代)", "tone": "元気・アップテンポ", "desc": "明るく活発なトーン。親しみやすい語りに最適", "is_custom": False},
    {"id": "Charon", "name": "Charon", "gender": "男性 (低音)", "tone": "落ち着いた低音", "desc": "重厚で深みのある知的な声。ニュースや解説風に", "is_custom": False},
    {"id": "Fenrir", "name": "Fenrir", "gender": "男性 (迫力)", "tone": "重厚・ダイナミック", "desc": "力強くエネルギッシュな声。ゲームや迫力ある場面に", "is_custom": False},
    {"id": "Aoede", "name": "Aoede", "gender": "女性", "tone": "上品・洗練・自然", "desc": "滑らかで透き通るような声。小説の朗読や案内音声に", "is_custom": False},
    {"id": "Kore", "name": "Kore", "gender": "女性", "tone": "明瞭・親しみやすい", "desc": "聞き取りやすく自然なトーン。日常会話やアシスタントに", "is_custom": False},
]

def load_custom_voices():
    if os.path.exists(CUSTOM_VOICES_FILE):
        try:
            with open(CUSTOM_VOICES_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_custom_voices(voices):
    with open(CUSTOM_VOICES_FILE, "w", encoding="utf-8") as f:
        json.dump(voices, f, ensure_ascii=False, indent=2)

@app.route("/")
def index():
    custom_voices = load_custom_voices()
    all_voices = custom_voices + PREBUILT_VOICES
    return render_template("index.html", voices=all_voices)

@app.route("/api/voices", methods=["GET"])
def get_voices():
    custom_voices = load_custom_voices()
    return jsonify({
        "success": True,
        "voices": custom_voices + PREBUILT_VOICES
    })

@app.route("/api/voices/replicate", methods=["POST"])
def replicate_voice():
    data = request.get_json() or {}
    display_name = data.get("display_name", "私のカスタムボイス").strip()
    source_b64 = data.get("source_audio_b64", "").strip()
    consent_b64 = data.get("consent_audio_b64", "").strip()

    if not source_b64 or not consent_b64:
        return jsonify({"success": False, "error": "参照音声と同意音声の両方が必要です。"}), 400

    api_key = get_api_key()
    if not api_key:
        return jsonify({"success": False, "error": "GEMINI_API_KEY が設定されていません。"}), 500

    try:
        client = genai.Client(api_key=api_key)
        
        # Call Gemini Voice Replication API
        replicated_voice = client.voices.create(
            store=True,
            voice={
                "type": "replicated",
                "display_name": display_name,
                "model": "gemini-3.8-flash-tts",
                "replicated": {
                    "source_audio": {
                        "mime_type": "audio/wav",
                        "data": source_b64,
                    },
                    "consent_audio": {
                        "mime_type": "audio/wav",
                        "data": consent_b64,
                    },
                },
            },
        )

        voice_id = replicated_voice.id
        new_voice_entry = {
            "id": voice_id,
            "name": display_name,
            "gender": "あなた",
            "tone": "カスタム複製ボイス",
            "desc": f"録音から作成したあなたの声 (ID: {voice_id[:12]}...)",
            "is_custom": True,
            "created_at": time.strftime("%Y-%m-%d %H:%M")
        }

        # Save to local custom_voices.json
        custom_voices = load_custom_voices()
        # Avoid duplicate
        custom_voices = [v for v in custom_voices if v["id"] != voice_id]
        custom_voices.insert(0, new_voice_entry)
        save_custom_voices(custom_voices)

        return jsonify({
            "success": True,
            "voice": new_voice_entry
        })

    except Exception as e:
        error_msg = str(e)
        if "Paid Quota Tier 1" in error_msg:
            return jsonify({
                "success": False, 
                "error": "Google Gemini APIの仕様により、カスタム音声複製（Voice Replication）機能は「有料従量課金プラン（Tier 1以上）」のアカウントでのみご利用いただけます。\n\n無料枠（Free Tier）のAPIキーをご利用の場合は、標準ボイス（Puck, Charon, Kore, Fenrir, Aoede）による音声合成機能をお楽しみください。"
            }), 403
        return jsonify({"success": False, "error": f"ボイス作成に失敗しました: {error_msg}"}), 500

@app.route("/api/voices/<voice_id>", methods=["DELETE"])
def delete_voice(voice_id):
    custom_voices = load_custom_voices()
    custom_voices = [v for v in custom_voices if v["id"] != voice_id]
    save_custom_voices(custom_voices)
    
    # Try deleting from Google API as well
    api_key = get_api_key()
    if api_key:
        try:
            client = genai.Client(api_key=api_key)
            client.voices.delete(voice=voice_id)
        except Exception:
            pass

    return jsonify({"success": True})

@app.route("/api/generate", methods=["POST"])
def generate_speech():
    data = request.get_json() or {}
    text = data.get("text", "").strip()
    voice = data.get("voice", "Puck")
    model_name = data.get("model", "gemini-3.8-flash-tts")

    if not text:
        return jsonify({"success": False, "error": "テキストを入力してください。"}), 400

    api_key = get_api_key()
    if not api_key:
        return jsonify({"success": False, "error": "GEMINI_API_KEY が設定されていません。"}), 500

    try:
        client = genai.Client(api_key=api_key)
        
        # Check if voice is custom or prebuilt
        custom_voices = load_custom_voices()
        is_custom = any(v["id"] == voice for v in custom_voices) or voice.startswith("voice_")

        if is_custom:
            voice_config = types.VoiceConfig(voice=voice)
        else:
            voice_config = types.VoiceConfig(
                prebuilt_voice_config=types.PrebuiltVoiceConfig(
                    voice_name=voice
                )
            )

        response = client.models.generate_content(
            model=model_name,
            contents=text,
            config=types.GenerateContentConfig(
                response_modalities=["AUDIO"],
                speech_config=types.SpeechConfig(
                    voice_config=voice_config
                ),
            ),
        )

        audio_bytes = None
        if response.candidates and response.candidates[0].content:
            for part in response.candidates[0].content.parts:
                if part.inline_data:
                    audio_bytes = part.inline_data.data
                    break

        if not audio_bytes:
            return jsonify({"success": False, "error": "モデルから音声データが返されませんでした。"}), 500

        # Save audio file
        safe_voice_name = voice if not is_custom else "MyVoice"
        filename = f"{int(time.time())}_{safe_voice_name}_{uuid.uuid4().hex[:6]}.wav"
        file_path = os.path.join(AUDIO_DIR, filename)
        with open(file_path, "wb") as f:
            f.write(audio_bytes)

        # Get display name for response
        voice_display = voice
        for v in custom_voices + PREBUILT_VOICES:
            if v["id"] == voice:
                voice_display = v["name"]
                break

        return jsonify({
            "success": True,
            "audio_url": f"/static/audio/{filename}",
            "filename": filename,
            "voice": voice_display,
            "model": model_name,
            "text": text,
            "timestamp": time.strftime("%H:%M:%S")
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    port = 5000
    print(f"Gemini TTS Web App running at http://localhost:{port}")
    app.run(host="127.0.0.1", port=port, debug=False)
