import customtkinter as ctk
import pygame
from name_formatter import name_formatter
import os
import threading

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("DOT.")
        self.geometry("690x690")
        self.grid_columnconfigure(0, weight=1)
        
        pygame.mixer.init()
        script_path = os.path.abspath(__file__)
        parent_dir = os.path.dirname(os.path.dirname(script_path))
        os.chdir(parent_dir)

        # Main container to hold different views
        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True)
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_rowconfigure(0, weight=1)
        
        self.show_view_1()

    def clear_container(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    def show_view_1(self):
        self.clear_container()
        
        frame = ctk.CTkFrame(self.container)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=3)
        frame.grid_columnconfigure(2, weight=1)
        frame.grid_columnconfigure(3, weight=1)
        
        self.entry = ctk.CTkEntry(frame, placeholder_text="Enter YT playlist link", width=400)
        self.entry.grid(row=1, column=1, padx=20, pady=50, sticky="ew")

        self.btn = ctk.CTkButton(frame, text="Submit", width=120)
        self.btn.grid(row=1, column=2, padx=(0, 20), pady=50, sticky="ew")
        self.btn.configure(command=self.submit_clicked)

    def submit_clicked(self):
        link = self.entry.get()
        if not link:
            return
        
        self.show_view_2()
        
        # Run processing in a separate thread
        threading.Thread(target=self.process_download, args=(link,), daemon=True).start()

    def show_view_2(self):
        self.clear_container()
        
        frame = ctk.CTkFrame(self.container)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)
        
        # Wrapper frame for centering
        inner_frame = ctk.CTkFrame(frame, fg_color="transparent")
        inner_frame.grid(row=0, column=0)
        
        label = ctk.CTkLabel(inner_frame, text="Downloading and Processing...\nPlease wait.", font=("Helvetica", 24, "bold"))
        label.pack(pady=20)
        
        progressbar = ctk.CTkProgressBar(inner_frame, mode="indeterminate", width=300)
        progressbar.pack(pady=20)
        progressbar.start()

    def process_download(self, link):
        try:
            final_names = name_formatter(link)
            self.after(0, self.show_view_3, final_names)
        except Exception as e:
            print(f"Error during processing: {e}")
            # If error, return to view 1
            self.after(0, self.show_view_1)

    def show_view_3(self, final_names):
        self.clear_container()
        
        self.frame = ctk.CTkScrollableFrame(self.container, width=690, height=690)
        self.frame.pack(fill="both", expand=True)
        
        self.buttons = {}
        for row, song in enumerate(final_names):
            display_name = song[:50] + "..." if len(song) > 50 else song
            btn = ctk.CTkButton(self.frame, width=670, text=display_name)
            
            # Bind events for play (left click) and edit (right click)
            btn.bind("<Button-1>", lambda event, b=btn, s=song: self.play_song(b, s))
            btn.bind("<Button-3>", lambda event, b=btn, s=song: self.edit_song(b, s))
            
            btn.grid(row=row, column=0, padx=5, pady=(5, 0))
            self.buttons[btn] = {'song': song, 'row': row}

        done_btn = ctk.CTkButton(self.frame, width=670, text="Done", command=self.done_clicked)
        done_btn.grid(row=len(final_names)+1, column=0, padx=5, pady=(20, 10))

    def play_song(self, btn, song):
        file_path = f"downloads/{song}.mp3"
        print(f"Playing {file_path}")
        try:
            pygame.mixer.music.stop()
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()
        except Exception as e:
            print(f"Failed to play {file_path}: {e}")

    def edit_song(self, btn, song):
        # Prevent multiple edits at once on the same button
        if hasattr(btn, 'is_editing') and btn.is_editing:
            return
        btn.is_editing = True
        
        row_info = self.buttons[btn]['row']
        
        # Hide the button
        btn.grid_remove()
        
        # Create an entry in its place
        entry = ctk.CTkEntry(self.frame, width=670)
        entry.insert(0, song)
        entry.grid(row=row_info, column=0, padx=5, pady=(5, 0))
        entry.focus()
        
        def save_edit(event):
            new_name = entry.get().strip()
            if new_name and new_name != song:
                safe_new_name = new_name.replace("/", "-").replace("\\", "-").replace(":", "-").replace('"', "").replace("*", "").replace("?", "").replace("<", "").replace(">", "").replace("|", "")
                old_path = f"downloads/{song}.mp3"
                new_path = f"downloads/{safe_new_name}.mp3"
                try:
                    os.rename(old_path, new_path)
                    print(f"Renamed {old_path} to {new_path}")
                    
                    display_name = safe_new_name[:50] + "..." if len(safe_new_name) > 50 else safe_new_name
                    btn.configure(text=display_name)
                    self.buttons[btn]['song'] = safe_new_name
                    
                    # Re-bind events with the new song name
                    btn.bind("<Button-1>", lambda e, b=btn, s=safe_new_name: self.play_song(b, s))
                    btn.bind("<Button-3>", lambda e, b=btn, s=safe_new_name: self.edit_song(b, s))
                except Exception as e:
                    print(f"Error renaming file: {e}")
            
            entry.destroy()
            btn.grid()
            btn.is_editing = False

        entry.bind("<Return>", save_edit)
        entry.bind("<FocusOut>", lambda e: save_edit(None)) # Save if user clicks away

    def done_clicked(self):
        print("Done was clicked...")
        pygame.mixer.music.stop()
        self.show_view_1()

if __name__ == "__main__":
    app = App()
    app.mainloop()