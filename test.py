from pytube import YouTube, Search
import os

def search_videos(query):
    search = Search(query)
    results = search.results[:10]
    return results

def get_video_info(video_url):
    yt = YouTube(video_url)
    video_streams = yt.streams.filter(file_extension='mp4')
    audio_streams = yt.streams.filter(only_audio=True)

    video_info = [(stream.resolution, stream.filesize) for stream in video_streams if stream.resolution is not None]
    audio_info = [(stream.abr, stream.filesize) for stream in audio_streams]

    return yt.title, video_info, audio_info

def download_video(video_url, quality_index, download_path='.'):
    yt = YouTube(video_url)
    video_stream = yt.streams.filter(file_extension='mp4')#[quality_index]
    video_stream.download(output_path=download_path)
    print(f"Видео '{yt.title}' скачано в {download_path}")

def download_audio(video_url, quality_index, download_path='.'):
    yt = YouTube(video_url)
    audio_stream = yt.streams.filter(only_audio=True)[quality_index]
    audio_file = audio_stream.download(output_path=download_path)

    # Переименовываем файл в mp3
    base, ext = os.path.splitext(audio_file)
    new_file = base + '.mp3'
    os.rename(audio_file, new_file)
    print(f"Аудио '{yt.title}' скачано и сохранено как {new_file}")

def main():
    while True:
        print("\nМеню:")
        print("1. Скачать видео")
        print("2. Скачать аудио")
        print("3. Выход")

        choice = input("Выберите опцию: ")

        if choice == '1':
            video_url = input("Введите ссылку на видео")
            download_video(video_url) #quality_choice

        elif choice == '2':
            query = input("Введите запрос видео: ")
            results = search_videos(query)

            print("Выберите видео:")
            for i, result in enumerate(results):
                print(f"{i + 1}. {result.title}")

            video_choice = int(input("Введите номер видео для скачивания: ")) - 1
            video_url = results[video_choice].watch_url

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
