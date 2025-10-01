import tkinter
from tkinter import PhotoImage
import threading
import sys
import subprocess
import my_ee_server

running_clients = []


def start_server_button():
    server_thread = threading.Thread(target=my_ee_server.start_server, daemon=True)
    server_thread.start()
    start_button.config(state="disabled")
    print("Server started in the background.")


def start_new_client():
    print("Starting a new client console...")
    client_process = subprocess.Popen(
        [sys.executable, 'my_ee_client.py'],
        creationflags=subprocess.CREATE_NEW_CONSOLE
    )
    running_clients.append(client_process)


def on_closing():
    print("Main window is closing, terminating all client processes...")
    for process in running_clients:
        process.kill()
    # Finally, destroy the main window
    window.destroy()


# --- Main Window Setup ---
window = tkinter.Tk()
window.title("Server-Client Launcher")
window.config(bg='black', pady=50, padx=50)

# --- Server Side UI ---
canvas_server = tkinter.Canvas(window, width=400, height=400, background='white')
canvas_server.grid(column=0, row=0)
canvas_server.create_text(200, 180, text="Server Control", font=("Arial", 20))

# --- Client Side UI ---
canvas_client = tkinter.Canvas(window, width=400, height=400, background='#D3D3D3')
canvas_client.grid(row=0, column=1)
canvas_client.create_text(200, 180, text="Client Launcher", font=("Arial", 20))

# --- Buttons ---
button_frame = tkinter.Frame(window, bg="black")
button_frame.grid(row=1, column=0, columnspan=2, pady=20)

# SERVER START BUTTON
start_image = PhotoImage(file='images/right.png')
start_button = tkinter.Button(button_frame, text="Start Server", image=start_image, compound="left",
                              command=start_server_button)
start_button.grid(row=0, column=0, padx=50)

# CLIENT START BUTTON
client_image = PhotoImage(file='images/right.png')
client_button = tkinter.Button(button_frame, text="Start Client", image=client_image, compound="left",
                               command=start_new_client)
client_button.grid(row=0, column=1, padx=50)

window.protocol("WM_DELETE_WINDOW", on_closing)

window.mainloop()
