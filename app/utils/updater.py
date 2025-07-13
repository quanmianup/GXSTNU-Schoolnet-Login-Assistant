import json
import os
import subprocess
import tempfile

import requests

GITHUB_REPO = "https://api.github.com/repos/yourusername/schoolnet/releases/latest"
UPDATE_URL = "https://github.com/yourusername/schoolnet/releases/download/v{version}/schoolnet_update.exe"


class Updater:
    def check_for_updates(self):
        try:
            response = requests.get(GITHUB_REPO)
            latest_release = response.json()
            latest_version = latest_release['tag_name']
            current_version = self.get_current_version()

            if latest_version > current_version:
                return latest_version
            return None
        except Exception as e:
            print("检查更新失败:", e)
            return None

    def get_current_version(self):
        try:
            with open('config/version.json', 'r') as f:
                version_info = json.load(f)
            return version_info.get('version', '0.0.0')
        except:
            return '0.0.0'

    def download_update(self, version):
        update_path = os.path.join(tempfile.gettempdir(), f"schoolnet_update_{version}.exe")
        response = requests.get(UPDATE_URL.format(version=version), stream=True)
        with open(update_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        return update_path

    def apply_update(self, update_path):
        updater_script = os.path.join(tempfile.gettempdir(), "updater.bat")
        with open(updater_script, 'w') as f:
            f.write(f'@echo off\nping 127.0.0.1 -n 5 > nul\nstart "" "{update_path}"\ntaskkill /im schoolnet.exe /f')
        subprocess.Popen(['start', 'cmd', '/c', updater_script], shell=True)
        QApplication.quit()
