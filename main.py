import yt_dlp


def search_videos(query):
    ydl_opts = {
        'default_search': 'ytsearch10',  # Ищем до 10 результатов
        'quiet': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(query, download=False)
        return result['entries'][:10]


def get_video_info(video_url):
    ydl_opts = {
        'quiet': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=False)

    video_info = [(f"{stream['format_note']} ({stream['height']}p)", stream['filesize'])
                  for stream in info['formats'] if 'height' in stream and stream['filesize']]

    audio_info = [(f"{stream['abr']} kbps", stream['filesize'])
                  for stream in info['formats'] if
                  stream['acodec'] != 'none' and stream['vcodec'] == 'none' and stream['filesize']]

    return info['title'], video_info, audio_info


def download_video(video_url, quality_index, download_path='.'):
    ydl_opts = {
        'format': f'bestvideo[ext=mp4][height<=1080]+bestaudio[ext=m4a]/best[ext=mp4]',
        # Скачиваем с ограничением на 1080p
        'outtmpl': f'{download_path}/%(title)s.%(ext)s'
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])
    print(f"Видео скачано в {download_path}")


def download_audio(video_url, quality_index, download_path='.'):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': f'{download_path}/%(title)s.%(ext)s'
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])
    print(f"Аудио скачано и сохранено как MP3 в {download_path}")


def main():
    while True:
        print("\nМеню:")
        print("1. Скачать видео")
        print("2. Скачать аудио")
        print("3. Выход")

        choice = input("Выберите опцию: ")

        if choice == '1':
            query = input("Введите запрос видео: ")
            results = search_videos(query)

            print("Выберите видео:")
            for i, result in enumerate(results):
                print(f"{i + 1}. {result['title']}")

            video_choice = int(input("Введите номер видео для скачивания: ")) - 1
            video_url = results[video_choice]['webpage_url']

            title, video_info, _ = get_video_info(video_url)

            print("Доступные качества видео:")
            for i, (resolution, filesize) in enumerate(video_info):
                print(f"{i + 1}. {resolution} - {filesize / 1024 / 1024:.2f} MB")

            quality_choice = int(input("Введите номер качества для скачивания: ")) - 1
            download_video(video_url, quality_choice)

        elif choice == '2':
            query = input("Введите запрос видео: ")
            results = search_videos(query)

            print("Выберите видео:")
            for i, result in enumerate(results):
                print(f"{i + 1}. {result['title']}")

            video_choice = int(input("Введите номер видео для скачивания: ")) - 1
            video_url = results[video_choice]['webpage_url']

            title, _, audio_info = get_video_info(video_url)

            print("Доступные качества аудио:")
            for i, (abr, filesize) in enumerate(audio_info):
                print(f"{i + 1}. {abr} - {filesize / 1024 / 1024:.2f} MB")

            quality_choice = int(input("Введите номер качества для скачивания: ")) - 1
            download_audio(video_url, quality_choice)

        elif choice == '3':
            break

        else:
            print("Неверный выбор. Пожалуйста, выберите снова.")


if __name__ == "__main__":
    main()
