import customtkinter as ctk

app = ctk.CTk()
app.title("hehehe")
app.geometry("690x690")

entry = ctk.CTkEntry(app, placeholder_text="smth new")
entry.pack()

app.mainloop()