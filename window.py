import customtkinter


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

        self.frameStatus = customtkinter.CTkFrame(
            self, fg_color="transparent"
        )
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
            self.frameMain, text="Start", width=70
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
