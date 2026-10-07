# Gemini 3.8 Voice Studio 🎙️✨

Googleの最新音声生成モデル **Gemini 3.8 Flash TTS** および **Gemini 3.8 Flash-Lite TTS** を活用した、表現力豊かな音声合成＆ボイスレプリケーション（声の複製）Webアプリケーションです。

---

## 🌟 主な特徴

- 🎭 **感情・演技タグの簡単挿入**
  - `<laugh>`（笑い）、`<sigh>`（ため息）、`<whisper>`（ささやき）、`<excited>`（興奮）、`<gasp>`（息をのむ）、`<sad>`（悲しみ）、`<short pause>`（間）などをワンクリックで文章に反映。
  - テキストを選択してタグボタンを押すと、自動的にタグで囲まれます。
- 🗣️ **多彩なキャラクター音声**
  - **Puck**: 元気・アップテンポ（親しみやすいトーク）
  - **Charon**: 落ち着いた低音（ニュース・解説風）
  - **Aoede**: 上品・洗練・自然（小説の朗読・オーディオブック）
  - **Fenrir**: 重厚・ダイナミック（ゲーム・力強い場面）
  - **Kore**: 明瞭・親しみやすい（日常会話・アシスタント）
- 🎤 **ボイスレプリケーション（自分の声の複製）**
  - ブラウザのマイクを使って「声のサンプル（10〜30秒）」と「同意文」を録音するだけで、あなた専用のボイスモデルを作成可能！
- ⚡ **モデル切り替え**
  - **Gemini 3.8 Flash TTS**: 高音質・豊かな演技表現向け
  - **Gemini 3.8 Flash-Lite TTS**: 超高速・低遅延向け
- 🎧 **即時試聴 & WAVダウンロード**
  - 生成された音声をブラウザ上で即座に自動再生。
  - WAV形式でワンクリックダウンロード可能。
  - 直近の生成履歴を一覧表示して、声やタグによる表現の違いを聴き比べできます。

---

## 🚀 クイックスタート

### 1. リポジトリをクローン
```bash
git clone https://github.com/kametora-lab/gemini-voice-studio.git
cd gemini-voice-studio
```

### 2. 依存パッケージをインストール
```bash
pip install -r requirements.txt
```

### 3. APIキーを設定
[Google AI Studio](https://aistudio.google.com/apikey) で無料のAPIキーを取得します。

`.env.example` をコピーして `.env` を作成し、取得したキーを入力します：
```bash
cp .env.example .env
```
`.env`:
```env
GEMINI_API_KEY="あなたのAPIキー"
```

### 4. アプリを起動
```bash
python app.py
```
ブラウザで **http://localhost:5000** を開くとアプリが利用できます！

---

## 📁 ディレクトリ構成

```
gemini-tts/
├── app.py                 # Flaskバックエンド (Gemini API 連携)
├── templates/
│   └── index.html         # Web Studio UI (Tailwind CSS, Web Audio API)
├── static/
│   └── audio/             # 生成されたWAV音声の保存先
├── requirements.txt       # Python依存ライブラリ
├── .env.example           # 環境変数テンプレート
├── .gitignore             # Git除外設定 (APIキーや音声データを除外)
└── README.md              # プロジェクト説明書
```

---

## 🔒 セキュリティとプライバシーについて

- `.env` や `custom_voices.json`、生成された音声ファイル（`static/audio/*.wav`）は `.gitignore` に登録されているため、GitリポジトリやGitHubに公開されることはありません。
- 音声複製（Voice Replication）機能は、Googleの規定に基づき話者本人の明示的な同意音声（生体照合）が必須となっています。

---

## 📄 ライセンス

[MIT License](LICENSE)
