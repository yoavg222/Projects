import socket
import threading
import  pyautogui
import win32api
import keyboard
import json
import time

SERVER_IP = "192.168.1.126"
PORT_KEYBOARD_SOCKET = 12346

SIZE_HEADER_FORMAT = "0000000|"
size_header_size = len(SIZE_HEADER_FORMAT)
TCP_DEBUG = True
LEN_TO_PRINT = 100


def recv_by_size(sock):
    size_header = b''
    data_len = 0
    while len(size_header) < size_header_size:
        _s = sock.recv(size_header_size - len(size_header))
        if _s == b'':
            size_header = b''
            break
        size_header += _s
    data  = b''
    if size_header != b'':
        data_len = int(size_header[:size_header_size - 1])
        while len(data) < data_len:
            _d = sock.recv(data_len - len(data))
            if _d == b'':
                data  = b''
                break
            data += _d

    if  TCP_DEBUG and size_header != b'':
        print ("\nRecv(%s)>>>" % (size_header,), end = '')
        print ("%s"%(data[:min(len(data),LEN_TO_PRINT)],))
    if data_len != len(data):
        data=b''
    return data


def check_turn_on_button(button):
    # time.sleep(5)
    # pyautogui.click()
    pyautogui.write(button)
    # pyautogui.typewrite(["enter"])


def computer_keyboard_client():
    keyboard_socket_client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    keyboard_socket_client.connect((SERVER_IP,PORT_KEYBOARD_SOCKET))

    # try:
    #     socket_file = keyboard_socket_client.makefile('r')
    # except:
    #     return

    time.sleep(5)
    pyautogui.click()
    while True:
        try:
            data = recv_by_size(keyboard_socket_client).decode()
            if not data:
                break

            print(f"i got: {data}")
            check_turn_on_button(data)
        except KeyboardInterrupt:
            break

    keyboard_socket_client.close()




def main():
    threads = []

    t_computer_keyboard = threading.Thread(target=computer_keyboard_client)
    threads.append(t_computer_keyboard)
    t_computer_keyboard.start()

    for t in threads:
        t.join()


if __name__ == "__main__":
    main()