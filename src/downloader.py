import yt_dlp

def download_playlist(playlist_url):
    ydl_opts = {
        'format': 'bestaudio/best',                         # get the highest quality audio available
        'outtmpl': f'DOT./downloads/%(title)s.%(ext)s',     # save path and filename
        'noplaylist': True,                                 # ensure it only downloads the specific video, not the whole playlist again
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
download_playlist("https://youtube.com/playlist?list=PLazTozPlnVQ-QBpOKEm406va_sqNcROew&si=r5gI9ghCkuOA9WbH")