import socket
import threading
import win32api
import keyboard
import json


SERVER_IP = "192.168.1.126"
PORT_KEYBOARD_SOCKET = 12345



def check_turn_on_button(button):
    pass

def computer_keyboard_client():
    keyboard_socket_client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    keyboard_socket_client.connect((SERVER_IP,PORT_KEYBOARD_SOCKET))

    socket_file = keyboard_socket_client.makefile('r')
    while True:
        try:
            line = socket_file.readline()

            if not line:
                break

            data = json.loads(line)
            print(f"i got: {data['key']}")

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