import customtkinter
import socket
import colors
import random
import threading


class Window(customtkinter.CTk):

    def __init__(self):
        super().__init__()
        # self._set_appearance_mode("system")
        self.title("Local Proxy Logger")
        self.minsize(width=600, height=500)
        self.maxsize(width=600, height=500)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=2)
        self.grid_rowconfigure(1, weight=8)
        self.grid_rowconfigure(2, weight=1)
        self.server_running = False
        # frames ---
        self.frameMain = customtkinter.CTkFrame(self, fg_color="transparent")
        self.frameMain.grid(row=0, column=0, sticky="w")
        self.frameMain.grid_rowconfigure(0, weight=1)
        self.frameMain.grid_columnconfigure(0, weight=1)
        self.frameMain.grid_columnconfigure(1, weight=1)
        self.frameMain.grid_columnconfigure(2, weight=1)
        self.frameMain.grid_columnconfigure(3, weight=1)
        self.frameMain.grid_columnconfigure(4, weight=1)

        self.frameLog = customtkinter.CTkFrame(self, fg_color="transparent")
        self.frameLog.grid(row=1, column=0, sticky="nsew")
        self.frameLog.grid_rowconfigure(0, weight=1)
        self.frameLog.grid_columnconfigure(0, weight=1)

        self.frameStatus = customtkinter.CTkFrame(self, fg_color="transparent")
        self.frameStatus.grid(row=2, column=0, sticky="w")
        self.frameStatus.grid_rowconfigure(0, weight=1)
        self.frameStatus.grid_columnconfigure(0, weight=1)
        self.frameStatus.grid_columnconfigure(1, weight=1)

        self.lblServerIp = customtkinter.CTkLabel(
            self.frameMain, text="Server IP :", padx=10
        )
        self.lblServerIp.grid(row=0, column=0)

        self.txtServerIp = customtkinter.CTkEntry(
            self.frameMain, placeholder_text="127.0.0.1"
        )
        self.txtServerIp.grid(row=0, column=1, padx=(0, 10))

        self.lblServerPort = customtkinter.CTkLabel(self.frameMain, text="Port :")
        self.lblServerPort.grid(row=0, column=2, padx=10)

        self.txtServerPort = customtkinter.CTkEntry(
            self.frameMain, placeholder_text="8888", width=60
        )
        self.txtServerPort.grid(row=0, column=3)

        self.btnToggleServerStatus = customtkinter.CTkButton(
            self.frameMain, text="Start", width=70, command=self.main
        )
        self.btnToggleServerStatus.grid(row=0, column=4, padx=20)

        self.txtLog = customtkinter.CTkTextbox(self.frameLog)
        self.txtLog.grid(row=0, column=0, sticky="nsew", padx=10)

        self.lblUrl = customtkinter.CTkLabel(self.frameStatus, text="127.0.0.1:8888")
        self.lblUrl.grid(row=0, column=0, padx=10)

        self.lblStatus = customtkinter.CTkLabel(
            self.frameStatus, text="not running", text_color="red"
        )
        self.lblStatus.grid(row=0, column=1, padx=10)

    def main(self):
        if not self.server_running:
            proxy_address = (
                self.txtServerIp.get() if self.txtServerIp.get() != "" else "127.0.0.1"
            )
            proxy_port = int(
                self.txtServerPort.get() if self.txtServerPort.get() != "" else "8888"
            )
            proxy_client = 5

            # set available port
            while True:
                try:
                    proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    proxy_socket.bind((proxy_address, proxy_port))
                    proxy_socket.listen(proxy_client)
                except Exception as error:
                    if error.errno == 98:
                        self.txtLog.insert(
                            "end", f"Server already in use on port {proxy_port}\n"
                        )
                        proxy_port = random.randint(1111, 9999)
                        self.txtLog.insert("end", f"Try again on port {proxy_port} \n")
                        continue
                break

            # server running style
            self.btnToggleServerStatus.configure(text="Stop")
            self.lblUrl.configure(text=f"{proxy_address}:{proxy_port}")
            self.lblStatus.configure(text="running", text_color="green")
            self.txtServerIp.configure(state="disable")
            self.txtServerPort.configure(state="disable")

            self.txtLog.insert(
                "end", "Lestening on : " + f"{proxy_address}:{proxy_port}\n"
            )
            self.server_running = True
            server_thread = threading.Thread(
                target=self.start_server, args=(proxy_socket,)
            )
            server_thread.start()

        else:
            self.server_running = False
            self.txtLog.insert("end", "\nServer Stopped!\n")
            # server running style
            self.btnToggleServerStatus.configure(text="Start")
            self.lblStatus.configure(text="not running", text_color="red")
            self.txtServerIp.configure(state="normal")
            self.txtServerPort.configure(state="normal")

    def handle_client(self, client_socket):
        try:
            request = client_socket.recv(4096)
            self.txtLog.insert("end", "Client sended data : \n")
            self.txtLog.insert("end", request.decode())
            client_socket.close()
        except Exception as error:
            print("error 127")
            exit()

    def start_server(self, proxy_socket):
        while self.server_running:
            self.txtLog.insert("end", "\nConnection Accepted : \n")

            try:
                client_socket, address = proxy_socket.accept()
                self.txtLog.insert("end", f"Address : {address[0]}:{address[1]}\n")
                self.handle_client(client_socket)
            except Exception as error:
                print("error 117")
                exit()
