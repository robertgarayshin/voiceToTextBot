import pytube


def download(message):
    link = message.text
    yt = pytube.YouTube(link, use_oauth=True, allow_oauth_cache=True)

    mus = yt.streams.get_audio_only()
    mus.download(filename='./.tmp/audio.mp3', skip_existing=False)
