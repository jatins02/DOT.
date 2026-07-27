import customtkinter as ctk
from name_formatter import name_formatter

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("DOT.")
        self.geometry("690x690")
        self.grid_columnconfigure(0, weight=1)
        self.click_timer = None
        self.initWindow()

    def initWindow(self):
        self.entry = ctk.CTkEntry(self, placeholder_text="Enter YT playlist link", width=540)
        self.entry.grid(row=1, columns=1, padx=20, pady=20, sticky="w")

        self.btn = ctk.CTkButton(self, text="submit", width=180)
        self.btn.grid(row=1, column=2, padx=(0, 20), pady=20, sticky="ew")
        self.btn.configure(command=self.submit_clicked)

    def submit_clicked(self):
        self.link = self.entry.get()
        print(self.link)

        self.entry.destroy()
        self.btn.destroy()


        self.frame = ctk.CTkScrollableFrame(self, width=690, height=690)
        self.frame.pack(fill="both", expand=True)
        self.final = name_formatter()
        row = 0
        for song in self.final:
            btn = ctk.CTkButton(self.frame, width=690, text=(song[:40] if len(song)>40 else song))
            btn.bind("<Button-1>", self.on_click_event)
            btn.grid(row=row, column=0, padx=(0, 10), pady=(5, 0))
            row += 1

    def on_click_event(self, event):
        if event.type == '4' and self.click_timer:
            self.after_cancel(self.click_timer)
            self.click_timer = None
            self.double_click_action()
        else:
            if self.click_timer:
                self.after_cancel(self.click_timer)
            self.click_timer = self.after(200, self.single_click_action)

    def single_click_action(self):
        print("single clcik detected")

    def double_click_action(self):
        print("double click detected")
        

if __name__ == "__main__":
    app = App()
    app.mainloop()