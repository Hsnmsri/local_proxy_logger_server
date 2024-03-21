import socket
import ssl
import threading
import random


class colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"


def handle_client(client_socket):
    request = client_socket.recv(4096)
    print(colors.CYAN + "Client sended data : " + colors.RESET)
    print(request.decode())
    client_socket.close()


def main():
    proxy_address = "127.0.0.1"
    proxy_port = 8888
    proxy_client = 5

    proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        try:
            proxy_socket.bind((proxy_address, proxy_port))
            proxy_socket.listen(proxy_client)
        except Exception as e:
            if e.errno == 98:
                proxy_port = random.randint(1111, 9999)
                continue
        break

    print(
        colors.BLUE + "Listening on : " + colors.RESET + f"{proxy_address}:{proxy_port}"
    )

    while True:
        print("\n" + colors.GREEN + "Connection Accepted : " + colors.RESET)
        client_socket, address = proxy_socket.accept()
        print(
            "Address : "
            + colors.BLUE
            + f"{address[0]}"
            + colors.RESET
            + ":"
            + colors.BLUE
            + f"{address[1]}"
            + colors.RESET
        )

        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()


if __name__ == "__main__":
    main()
