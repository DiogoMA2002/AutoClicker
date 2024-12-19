import tkinter as tk
from threading import Thread, Event
from pynput.mouse import Button, Controller
import keyboard
import time

# Initialize mouse controller
mouse = Controller()

# Autoclicker control variables
clicking_event = Event()  # Event to manage clicking state
stop_event = Event()      # To stop all threads
f6_pressed = False        # Track the F6 key state

# Function to perform clicking
def autoclick():
    while not stop_event.is_set():
        if clicking_event.is_set():
            mouse.click(Button.left, 1)
            time.sleep(0.01)  # 10ms delay between clicks
        else:
            time.sleep(0.1)  # Reduce CPU usage when not clicking

# Function to monitor keyboard inputs
def monitor_keys():
    global f6_pressed
    while not stop_event.is_set():
        # Handle F6 key toggling
        if keyboard.is_pressed('F6'):
            if not f6_pressed:
                toggle_clicking()
                f6_pressed = True  # Mark F6 as pressed
        else:
            f6_pressed = False  # Reset when F6 is released
        
        # Handle ESC key to exit
        if keyboard.is_pressed('esc'):
            stop_autoclicker()  # Gracefully exit if ESC is pressed
            break

        time.sleep(0.1)  # Reduce CPU usage

# Function to toggle clicking state
def toggle_clicking():
    if clicking_event.is_set():
        clicking_event.clear()
        update_status("OFF")
        print("Autoclicker OFF")
    else:
        clicking_event.set()
        update_status("ON")
        print("Autoclicker ON")

# Function to start threads
def start_autoclicker():
    if not hasattr(start_autoclicker, "initialized"):
        start_autoclicker.initialized = True
        Thread(target=autoclick, daemon=True).start()
        Thread(target=monitor_keys, daemon=True).start()
        print("Autoclicker threads started.")
    toggle_clicking()  # Also toggle clicking when pressing Start

# Function to stop threads and exit application
def stop_autoclicker():
    stop_event.set()  # Signal all threads to stop
    clicking_event.clear()
    gui.destroy()
    print("Exiting application...")

# Function to update status label
def update_status(status):
    status_label.config(text=f"Status: {status}")

# GUI Setup
gui = tk.Tk()
gui.geometry("400x300")
gui.resizable(False, False)
gui.title("Auto Clicker")

# Status label
status_label = tk.Label(gui, text="Status: OFF", font=("Arial", 14))
status_label.pack(pady=20)

# Start button
start_button = tk.Button(gui, text="Start (F6)", width=20, command=start_autoclicker)
start_button.pack(pady=10)

# Exit button
exit_button = tk.Button(gui, text="Exit", width=20, command=stop_autoclicker)
exit_button.pack(pady=10)

# Run the GUI event loop
gui.mainloop()
