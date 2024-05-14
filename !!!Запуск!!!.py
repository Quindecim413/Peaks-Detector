import os
import subprocess
import time
from pathlib import Path

if not os.path.exists('venv'):
    print('Перед запуском приложения произведите его установку')
    print('Для этого запустите файл "Установка.bat"')
    input()
    exit(1)

with open('start app.txt') as f:
    file_name = f.readlines()[0]

os.environ["PYTHONIOENCODING"] = 'utf-8'

def detect_server_for_folder(app_folder):
    notebook_list = subprocess.run('jupyter notebook list', capture_output=True, shell=True)
    servers = notebook_list.stdout.decode().split('\n')[1:]
    found = list(filter(lambda el: app_folder in el, servers))
    if found:
        return found[0].split(' ')[0]

if __name__ == '__main__':
    try:
        file_dir = os.path.dirname(str(Path(__file__).resolve()))
        found = detect_server_for_folder(file_dir)
        if not found:
            subprocess.run('start cmd.exe /c run_server.bat', shell=True)
            time.sleep(2)

        for i in range(10):
            found = detect_server_for_folder(file_dir)
            if not found:
                time.sleep(1)
            else:
                base, token = found.split('?')

                open_file_url = '{}apps/app/{}?{}'.format(base, file_name, token)
                subprocess.run('start chrome --app="{}"'.format(open_file_url), shell=True)#)
                break
        else:
            print('Не удалось подключиться к серверу jupyter')
            exit(1)
    except Exception as e:
        print(e)
        input()

