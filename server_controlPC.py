import socket
import threading
import win32api
import keyboard
import json

BIND_IP = "0.0.0.0"
PORT_KEYBOARD_SOCKET = 12346
BUFFER_SIZE = 1024

SIZE_HEADER_FORMAT = "0000000|" # n digits for data size + one delimiter
size_header_size = len(SIZE_HEADER_FORMAT)
TCP_DEBUG = True
LEN_TO_PRINT = 100


def send_with_size(sock, bdata):
    if type(bdata) == str:
        bdata = bdata.encode()
    len_data = len(bdata)
    header_data = str(len_data).zfill(size_header_size - 1) + "|"

    bytea = bytearray(header_data,encoding='utf8') + bdata
    sock.send(bytea)


    if TCP_DEBUG and  len_data > 0:
        print ("\nSent(%s)>>>" % (len_data,), end='')
        print ("%s"%(bytea[:min(len(bytea),LEN_TO_PRINT)],))


def send_button(button,sock):
    # sock.settimeout(1)
    # data = {
    #     "key":button
    # }
    # json_message = json.dumps(data) + "\n"
    # try:
    #     if sock.recv(BUFFER_SIZE) == b"":
    #         return
    #
    # except socket.error as err:
    #     if err.errno == 10035 or str(err) == "timed out":
    #         sock.sendall(json_message.encode('utf-8'))
    #     elif err.errno == 10054:
    #         print("Error %d Client is Gone.  reset by peer." % (err.errno))
    #         return
    #     else:
    #         print("%d General Sock Error Client disconnected" % (err.errno))
    #         return

    send_with_size(sock,button)



def new_key(event,sock):
    button = event.name
    send_button(button,sock)


def computer_keyboard_server():
    print("wait for computer keyboard client...")
    keyboard_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    keyboard_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    keyboard_socket.bind((BIND_IP,PORT_KEYBOARD_SOCKET))
    keyboard_socket.listen(1)
    sock,address = keyboard_socket.accept()

    print(f"{address} connect with our keyboard socket")

    keyboard.on_press(callback=lambda e: send_button(e.name, sock))
    keyboard.wait()

    sock.close()
    keyboard_socket.close()




def computer_mouse_server():
    pass


def picture_stream_server():
    pass



def main():
    threads = []


    t_computer_keyboard = threading.Thread(target = computer_keyboard_server)
    threads.append(t_computer_keyboard)
    t_computer_keyboard.start()


    for t in threads:
        t.join()



if __name__ == "__main__":
    main()