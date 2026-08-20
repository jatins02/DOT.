import yt_dlp
import os

def download_playlist(playlist_url):
    os.makedirs("downloads", exist_ok=True)
    ydl_opts = {
        'format': 'bestaudio/best',                         # get the highest quality audio available
        'outtmpl': f'downloads/%(title)s.%(ext)s',          # save path and filename
        'noplaylist': False,                                # ensure it only downloads the specific video, not the whole playlist again
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
        'quiet': True,                                      # set to True if you want to hide the download progress bars
    }
    try: 
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([playlist_url])
    except:
        print(f"error in donwloading playlist")
