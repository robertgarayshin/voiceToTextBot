import subprocess


def write_to_file(transcript):
    text_file = open("./.tmp/input.txt", "w")
    text_file.write(transcript)
    text_file.close()


def predict_ru(transcript):
    write_to_file(transcript)
    com = ['python3', 'example_ru.py', './.tmp/input.txt']
    process = subprocess.Popen(args=com, stdout=subprocess.PIPE)
    process.wait()
    output = process.stdout.read().decode('utf-8')
    rm = subprocess.Popen(args=['rm', './.tmp/input.txt'])
    rm.wait()
    return output


def predict_en(transcript):
    write_to_file(transcript)
    com = ['python3', 'example_en.py', './.tmp/input.txt']
    process = subprocess.Popen(args=com, stdout=subprocess.PIPE)
    process.wait()
    output = process.stdout.read().decode('utf-8')
    rm = subprocess.Popen(args=['rm', './.tmp/input.txt'])
    rm.wait()
    return output
