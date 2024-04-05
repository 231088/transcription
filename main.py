import sys
import os
import ffmpeg
from openai import OpenAI
import re

def main():
    
    # 引数チェック
    if len(sys.argv) == 1:
        sys.exit("Usage: python main.py [mp4]")
    if sys.argv[1].split('.')[-1] != 'mp4':
        sys.exit("Usage: python main.py [mp4]")
    
    # パスとファイル名(拡張子除く)を取得
    mp4_file_path = sys.argv[1]
    mp4_file_name = re.split(r'\\|/', sys.argv[1])[-1][0:-4]
    
    # 結果ファイルがすでに存在する場合はユーザーに確認
    if os.path.exists(f'./result/' + mp4_file_name + '.txt'):
        print('同じ名前のファイルがすでに存在します。上書きしますか？(y/n)')
        if input() != 'y' and input() != 'Y':
            print('処理を中断しました。')
            sys.exit()
        
        # すでに存在するファイルを削除
        os.remove(f'./result/' + mp4_file_name + '.txt')
    
    try:
        # 引数に置かれたファイルが存在するか確認
        with open(mp4_file_path, 'r') as f:
            pass
        
        # mp3に変換しtempファイル内に一時保存
        ffmpeg.input(mp4_file_path).output('./temp/temp.mp3').run()

        # 秒数を取得
        duration = ffmpeg.probe('./temp/temp.mp3')['format']['duration']
        # 整数に変換
        duration = int(float(duration))
        
        # 分割する秒数を設定
        # APIのファイルサイズ制限に合わせ、約20分ごとに分割
        split_time = 1220

        # 分割数を取得
        split_count = duration // split_time + 1

        # mp3ファイルを分割
        for i in range(split_count):
            ffmpeg.input('./temp/temp.mp3', ss=i*split_time, t=split_time).output(f'./temp/{i}.mp3').run()
        
        # 一時ファイル削除
        os.remove('./temp/temp.mp3')
        
        # 結果を書き込むテキストファイルを作成
        result_file = open(f'./result/' + mp4_file_name + '.txt', 'w')
        result_file.close()
        
        # OpenAIクライアントのインスタンスを生成
        client = OpenAI()
        
        # 分割された音声ファイルをwhisper-1でテキスト化
        for i in range(split_count):
            audio_file = open(f'./temp/{i}.mp3', "rb")
            transcription = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language='ja'
            )
            # 結果を書き加える
            with open('./result/' + mp4_file_name + '.txt', 'a') as f:
                f.write(transcription.text)
                f.write('\n')
            audio_file.close() 
        
        # 一時ファイル削除
        for i in range(split_count):
            os.remove(f'./temp/{i}.mp3')
            
                

    except FileNotFoundError:
        sys.exit("File not found")

main()