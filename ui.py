import tkinter
import tkinter.messagebox
import customtkinter
import webbrowser


customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("GestureFlow")
        self.iconbitmap("gestureflow.ico") 
        self.geometry(f"{1100}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="GestureFlow", font=customtkinter.CTkFont(size=30, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(30, 10))
        
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["System", "Dark", "Light"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(5, 50))
        
        

        frame = customtkinter.CTkFrame(self, width=300, corner_radius=0)
        frame.grid(row=0, column=1, padx=20, pady=(0, 20))
        mode_label = customtkinter.CTkLabel(frame, text="Select a mode:",font=customtkinter.CTkFont(size=20, weight="bold"))
        mode_label.grid(row=1, column=1, padx=20, pady=(30, 20))
    
        def switch_event1():
            if(switch1.get() == "on"):
                print("Volume/Brightness Control")
                switch2.deselect()
                switch3.deselect()
        def switch_event2():
            if(switch2.get() == "on"):
                print("Media Control")
                switch1.deselect()
                switch3.deselect()
        def switch_event3():
            if(switch3.get() == "on"):
                print("PDF Control")
                switch1.deselect() 
                switch2.deselect()
                

        # switch_var = customtkinter.StringVar(value="off")
        switch1 = customtkinter.CTkSwitch(frame, text="Volume/Brightness Control",button_color="green", command=switch_event1,
                                 onvalue="on", offvalue="off")
        switch1.grid(row=2, column=1, padx=20, pady=(0, 20))
        switch2 = customtkinter.CTkSwitch(frame, text="Media Control",button_color="green", command=switch_event2,
                                 onvalue="on", offvalue="off")
        switch2.grid(row=3, column=1, padx=20, pady=(0, 20))
        switch3 = customtkinter.CTkSwitch(frame, text="PDF Control",button_color="green", command=switch_event3,
                                 onvalue="on", offvalue="off")
        switch3.grid(row=4, column=1, padx=20, pady=(0, 30))

        def run_event():
            print("Run")


        run_button = customtkinter.CTkButton(frame, text="Run", command=run_event,font=customtkinter.CTkFont(size=15), width=100, height=40)
        run_button.grid(row=5, column=1, padx=20 , pady=(0, 50))

        def button_event():
            webbrowser.open("https://shamans1.github.io/mini-project/")

        web_label = customtkinter.CTkLabel(self, text="Documentation of GestureFow",font=customtkinter.CTkFont(size=22, weight="bold"))
        web_label.grid(row=2, column=1, padx=20)
        web_button = customtkinter.CTkButton(self, text="Click Here", command=button_event,font=customtkinter.CTkFont(size=15), width=100, height=40)
        web_button.grid(row=3, column=1, padx=20 , pady=(0, 50))
       
        

    

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)



if __name__ == "__main__":
    app = App()
    app.mainloop()