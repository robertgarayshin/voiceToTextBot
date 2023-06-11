import subprocess


def convert():
    input_file = './.tmp/audio.mp3'

    wavefile = input_file[:-4] + '.wav'
    pcmfile = input_file[:-4] + '.pcm'
    command_pcm = ['ffmpeg', '-y', '-i', input_file, '-acodec', 'pcm_s16le', '-f', 's16le', '-ac', '1', '-ar',
                   '16000', pcmfile]
    command_wav = ['ffmpeg', '-y', '-i', input_file, '-ar', '48000', '-ac', '1', '-f', 'wav', wavefile]
    process = subprocess.Popen(args=command_wav, stdout=subprocess.PIPE)
    process.wait()
    process = subprocess.Popen(args=command_pcm, stdout=subprocess.PIPE)
    process.wait()
    return wavefile, pcmfile

def remove():
    pr = subprocess.Popen(args=['rm', './.tmp/audio.mp3'], stdout=subprocess.PIPE)
    pr.wait()
    pr = subprocess.Popen(args=['rm', './.tmp/audio.wav'], stdout=subprocess.PIPE)
    pr.wait()
    pr = subprocess.Popen(args=['rm', './.tmp/audio.pcm'], stdout=subprocess.PIPE)
    pr.wait()
