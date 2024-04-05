# Transcription

## 目的
whisper-apiを用いて動画ファイルの会話内容を日本語で文字起こしします。

## 環境設定
FFMPEG: 2024-03-28-git-5d71f97e0e-essentials_build

requirements.txt から必要なモジュールをインストールしてください。
環境変数 OPENAI_API_KEY の設定が必要です。

## 利用方法
python main.py [.mp4ファイルのパス]

resultファイルにtxtファイルが生成されます。

注意！ 特殊な記号等を含むファイルはエラーが発生する恐れがあります。
今後のアップデートで対応予定です。
