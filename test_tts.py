import os
import sys
from google import genai
from google.genai import types

def get_api_key():
    api_key = os.environ.get("GEMINI_API_KEY")
    env_file = os.path.join(os.path.dirname(__file__), ".env")
    
    if not api_key and os.path.exists(env_file):
        with open(env_file, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("GEMINI_API_KEY="):
                    api_key = line.strip().split("=", 1)[1].strip("\"' ")
                    break

    if not api_key:
        print("APIキーが環境変数または .env に見つかりませんでした。")
        api_key = input("コピーした Gemini API キーをここに貼り付けて Enter を押してください: ").strip("\"' ")
        if api_key:
            save = input("このAPIキーを .env に保存しますか？ (y/n) [y]: ").strip().lower()
            if save != "n":
                with open(env_file, "w", encoding="utf-8") as f:
                    f.write(f'GEMINI_API_KEY="{api_key}"\n')
                print(f".env に保存しました！")

    return api_key

def main():
    api_key = get_api_key()
    if not api_key:
        print("APIキーが入力されなかったため終了します。")
        sys.exit(1)

    print("\nGemini クライアントを初期化中...")
    client = genai.Client(api_key=api_key)

    # 喋らせたいテキスト（日本語や感情表現）
    text_to_speak = "こんにちは！Geminiの最新の音声合成モデルです。とても自然に喋れているでしょうか？"
    
    print(f"\n音声を生成しています...")
    print(f"テキスト: 「{text_to_speak}」")
    print(f"モデル: gemini-3.8-flash-tts")

    try:
        response = client.models.generate_content(
            model="gemini-3.8-flash-tts",
            contents=text_to_speak,
            config=types.GenerateContentConfig(
                response_modalities=["AUDIO"],
                speech_config=types.SpeechConfig(
                    voice_config=types.VoiceConfig(
                        prebuilt_voice_config=types.PrebuiltVoiceConfig(
                            voice_name="Kore"  # Kore, Puck, Aoede, Fenrir など
                        )
                    )
                ),
            ),
        )

        audio_bytes = None
        for part in response.candidates[0].content.parts:
            if part.inline_data:
                audio_bytes = part.inline_data.data
                break

        if audio_bytes:
            output_file = os.path.join(os.path.dirname(__file__), "output.wav")
            with open(output_file, "wb") as f:
                f.write(audio_bytes)
            print(f"\n[成功] 音声ファイルを保存しました: {output_file}")
            
            # Windowsで自動再生（既定のプレイヤーを起動）
            try:
                os.startfile(output_file)
                print("音声を再生しています...")
            except Exception:
                pass
        else:
            print("エラー: 音声データがレスポンスに含まれていませんでした。")

    except Exception as e:
        print(f"\nエラーが発生しました: {e}")

if __name__ == "__main__":
    main()
