import customtkinter as ctk
import pygame
from name_formatter import name_formatter

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("DOT.")
        self.geometry("690x690")
        self.grid_columnconfigure(0, weight=1)
        self.click_timer = None
        self.initWindow()
        pygame.mixer.init()

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
            btn = ctk.CTkButton(self.frame, width=690, text=(song[:50] if len(song)>50 else song))
            btn.bind("<Any-Button>", command=self.handle_click)
            btn.grid(row=row, column=0, padx=(0, 10), pady=(5, 0))
            row += 1

        done_btn = ctk.CTkButton(self.frame, width = 690, text="done", command=self.done_clicked)
        done_btn.grid(row=row+1, column=0, padx=(0, 10), pady=(5, 0))

    def handle_click(self, event):
        clicked_button = event.widget.master
        print(type(clicked_button))
        button_text = clicked_button.cget("text")

        mouse_button = event.num 
        
        mouse_names = {1: "Left Click", 2: "Middle Click", 3: "Right Click"}
        click_type = mouse_names.get(mouse_button, "Unknown Click")

        if (click_type == "Left Click"):
            song = pygame.mixer.Sound(f"downloads/{button_text}/.mp3")
            song.play(max_time = 6769)
            pygame.time.wait(7000)

        
        print(f"Button '{button_text}' was clicked using: {click_type}")


    def done_clicked(self):
        print(f"done was clicked...")


if __name__ == "__main__":
    app = App()
    app.mainloop()