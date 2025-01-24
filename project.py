import tkinter as tk
from tkinter import messagebox
import yt_dlp
import os

# Function to append status messages to the status box
def append_status(message: str) -> None:
    """
    Appends the provided message to the status box with auto-scrolling.
    """
    status_box.insert(tk.END, message + "\n")
    status_box.see(tk.END)  # Auto-scroll to the bottom
    canvas.update_idletasks()

# Function to handle video download
def download_video() -> None:
    """
    Downloads the video from the URL entered by the user.
    """
    video_url = textField.get()  # Get the URL from the text field

    # Validation: Ensure the URL is not empty
    if not video_url.strip():
        messagebox.showerror("Error", "Please enter a valid video URL!")
        return

    try:
        # Ensure the Downloads directory exists
        create_downloads_directory()

        # yt-dlp options for video download
        ydl_opts = {
            'outtmpl': './Downloads/%(title)s.%(ext)s',  # Save video in Downloads folder
            'format': 'bestvideo+bestaudio/best',  # Download the best quality
            'progress_hooks': [progress_hook],  # Hook to track progress
        }

        append_status("Starting download...")

        # Download the video
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

        append_status("Download completed!")
        textField.delete(0, tk.END)  # Clear the input field after download
        messagebox.showinfo("Success", "Video downloaded successfully!")

    except Exception as e:
        append_status("An error occurred.")
        messagebox.showerror("Error", f"An error occurred: {e}")

# Function to track download progress
def progress_hook(d: dict) -> None:
    """
    Callback function to display download progress (percentage, speed, ETA).
    """
    if d['status'] == 'downloading':
        downloaded = d.get('_percent_str', '').strip()
        speed = d.get('_speed_str', '').strip()
        eta = d.get('eta', 'Unknown')
        append_status(f"Downloading... {downloaded} completed")
        append_status(f"Speed: {speed}")
        append_status(f"ETA: {eta} seconds")
    elif d['status'] == 'finished':
        append_status("Download finished. Writing file to disk...")

# Function to create the Downloads directory if it doesn't exist
def create_downloads_directory() -> None:
    """
    Creates the Downloads directory if it doesn't already exist.
    """
    if not os.path.exists("Downloads"):
        os.makedirs("Downloads")

# Function to handle button hover effect
def on_enter(e: tk.Event) -> None:
    download_button.config(bg="#3E77C4")

def on_leave(e: tk.Event) -> None:
    download_button.config(bg="black")

# Setting up the Tkinter window and UI components
def setup_gui() -> None:
    """
    Sets up the GUI components for the video downloader application.
    """
    global canvas, textField, download_button, status_box
    
    canvas = tk.Tk()
    canvas.geometry("600x500")
    canvas.title("Video Downloader")

    # Create gradient background
    gradient = tk.Canvas(canvas, width=600, height=500)
    gradient.pack(fill="both", expand=True)
    gradient.create_rectangle(0, 0, 600, 500, fill="#5D9CEC", outline="")
    gradient.create_rectangle(0, 250, 600, 500, fill="#4A90E2", outline="")

    # Fonts for UI components
    title_font = ("Helvetica", 20, "bold")
    button_font = ("Helvetica", 15, "bold")
    entry_font = ("Helvetica", 13)
    status_font = ("Helvetica", 11)

    # Title Label
    title_label = tk.Label(canvas, text="Video Downloader", font=title_font, bg="#5D9CEC", fg="white")
    title_label.place(relx=0.5, rely=0.1, anchor="center")

    # Input text field
    textField = tk.Entry(canvas, justify='center', width=40, font=entry_font, bg="white", relief="solid", bd=1)
    textField.place(relx=0.5, rely=0.3, anchor="center")
    textField.focus()

    # Download button
    download_button = tk.Button(
        canvas,
        text="Download",
        font=button_font,
        bg="black",
        fg="white",
        width=12,
        height=1,
        relief="flat",
        command=download_video
    )
    download_button.place(relx=0.5, rely=0.4, anchor="center")
    download_button.bind("<Enter>", on_enter)
    download_button.bind("<Leave>", on_leave)

    # Status text box for live updates
    status_box = tk.Text(canvas, height=10, width=50, font=status_font, bg="white", fg="black", wrap="word", relief="solid", bd=1)
    status_box.place(relx=0.5, rely=0.7, anchor="center")

    canvas.mainloop()

# Entry point of the program
if __name__ == "__main__":
    setup_gui()
