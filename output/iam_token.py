import subprocess


def get_token():
    command = ['yc', 'iam', 'create-token']
    process = subprocess.check_output(args=command, text=True)#, stdout=subprocess.PIPE, )
    return process[:-1]

print(get_token())