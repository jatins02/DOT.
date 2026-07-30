import yt_dlp

def download_playlist(playlist_url):
    ydl_opts = {
        'format': 'bestaudio/best',                         # get the highest quality audio available
        'outtmpl': f'downloads/%(title)s.%(ext)s',     # save path and filename
        'noplaylist': False,                                 # ensure it only downloads the specific video, not the whole playlist again
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
        'quiet': True,                                     # set to True if you want to hide the download progress bars
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([playlist_url])


# KIM to cd to proper dir, before downloading
download_playlist("https://youtube.com/playlist?list=PLazTozPlnVQ-QBpOKEm406va_sqNcROew&si=msJpltGAgIKA5mpd")


# import threading
# from pathlib import Path
# import yt_dlp


# def download_playlist(playlist_url: str):
#     # Ensure the downloads folder exists on disk
#     download_path = Path("downloads")
#     download_path.mkdir(parents=True, exist_ok=True)

#     ydl_opts = {
#         'format': 'bestaudio/best',
#         # Save directly to output_dir with YouTube title
#         'outtmpl': f'{download_path}/%(title)s.%(ext)s',
#         'noplaylist': False,  # Allow downloading full playlist
#         'postprocessors': [{
#             'key': 'FFmpegExtractAudio',
#             'preferredcodec': 'mp3',
#             'preferredquality': '192',  # Optimal size-to-quality ratio
#         }],
#         'quiet': True,
#     }

#     with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#         ydl.download([playlist_url])


# # def start_download_in_background(playlist_url: str):
# #     """Call this function from your CustomTkinter button to prevent freezing."""
# #     thread = threading.Thread(
# #         target=download_playlist, args=(playlist_url,), daemon=False
# #     )
# #     thread.start()


# download_playlist("https://youtube.com/playlist?list=PLazTozPlnVQ-QBpOKEm406va_sqNcROew&si=aaVaL9UceyOUAb0r")

