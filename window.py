import customtkinter
import socket
import threading
import random


class Window(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Local Proxy Logger")
        self.minsize(width=600, height=500)
        self.maxsize(width=600, height=500)
        self._set_appearance_mode("dark")

        self.server_running = False
        self.proxy_socket = None
        self.initialize_ui()

    def initialize_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Main Frame
        self.frame_main = customtkinter.CTkFrame(self, fg_color="transparent")
        self.frame_main.grid(row=0, column=0, sticky="ew",padx=10, pady=(13,10))

        self.lbl_server_ip = customtkinter.CTkLabel(self.frame_main, text="Server IP:")
        self.lbl_server_ip.grid(row=0, column=0)

        self.entry_server_ip = customtkinter.CTkEntry(
            self.frame_main, placeholder_text="127.0.0.1"
        )
        self.entry_server_ip.grid(row=0, column=1, padx=(10,15))

        self.lbl_server_port = customtkinter.CTkLabel(self.frame_main, text="Port:")
        self.lbl_server_port.grid(row=0, column=2)

        self.entry_server_port = customtkinter.CTkEntry(
            self.frame_main, placeholder_text="8888", width=60
        )
        self.entry_server_port.grid(row=0, column=3, padx=10)

        self.btn_start_stop = customtkinter.CTkButton(
            self.frame_main, text="Start", command=self.toggle_server,width=80
        )
        self.btn_start_stop.grid(row=0, column=4)

        # Log Frame
        self.frame_log = customtkinter.CTkFrame(self, fg_color="transparent")
        self.frame_log.grid(row=1, column=0, sticky="nsew", padx=5)
        self.grid_rowconfigure(1, weight=1)

        self.txt_log = customtkinter.CTkTextbox(self.frame_log)
        self.txt_log.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.frame_log.grid_columnconfigure(0, weight=1)
        self.frame_log.grid_rowconfigure(0, weight=1)

        # Status Frame
        self.frame_status = customtkinter.CTkFrame(self, fg_color="transparent")
        self.frame_status.grid(row=2, column=0, sticky="ew",padx=10, pady=(0,7))

        self.lbl_url = customtkinter.CTkLabel(self.frame_status, text="Address:Port")
        self.lbl_url.grid(row=0, column=0)

        self.lbl_status = customtkinter.CTkLabel(
            self.frame_status, text="Not Running", text_color="red"
        )
        self.lbl_status.grid(row=0, column=1 , padx=10)

    def log(self, message):
        self.txt_log.insert("end", message + "\n")
        self.txt_log.see("end")

    def toggle_server(self):
        if self.server_running:
            self.stop_server()
        else:
            self.start_server()

    def start_server(self):
        self.server_running = True
        self.btn_start_stop.configure(text="Stop")
        self.lbl_status.configure(text="Running", text_color="green")
        proxy_address = self.entry_server_ip.get() or "127.0.0.1"
        proxy_port = int(self.entry_server_port.get() or 8888)
        self.lbl_url.configure(text=f"{proxy_address}:{proxy_port}")

        self.proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.proxy_socket.bind((proxy_address, proxy_port))
            self.proxy_socket.listen(5)
            self.log(f"Server listening on {proxy_address}:{proxy_port}")
            threading.Thread(target=self.accept_connections, daemon=True).start()
        except Exception as e:
            self.log(f"Failed to start server: {e}")
            self.stop_server()

    def stop_server(self):
        self.server_running = False
        self.btn_start_stop.configure(text="Start")
        self.lbl_status.configure(text="Not Running", text_color="red")
        if self.proxy_socket:
            self.proxy_socket.close()
            self.proxy_socket = None
        self.log("Server stopped.")

    def accept_connections(self):
        while self.server_running:
            try:
                client_socket, address = self.proxy_socket.accept()
                self.log(f"Connection from {address}")
                threading.Thread(
                    target=self.handle_client, args=(client_socket,), daemon=True
                ).start()
            except OSError:
                break  # Socket closed
            except Exception as e:
                self.log(f"Error accepting connections: {e}")

    def handle_client(self, client_socket):
        try:
            request = client_socket.recv(4096)
            if not request:
                raise Exception("Client disconnected")
            self.log(f"Request from client: {request.decode()}")
            client_socket.close()
        except Exception as e:
            self.log(f"Error handling client: {e}")
