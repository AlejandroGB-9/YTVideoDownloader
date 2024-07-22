from pytubefix import YouTube, exceptions
import tkinter as tk
from tkinter import filedialog, messagebox
from moviepy.editor import VideoFileClip, AudioFileClip
import os
import shutil

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("YTVideo Downloader")
        self.root.geometry("300x200")

        self.main_frame = tk.Frame(self.root)
        self.create_main_screen()

    def create_main_screen(self):
        self.clear_frame(self.main_frame)
        
        tk.Label(self.main_frame, text="Select an option:").pack(pady=20)
        
        button_frame = tk.Frame(self.main_frame)
        button_frame.pack(pady=10)
        
        video_button = tk.Button(button_frame, text="Video", command=lambda: self.create_option_screen("Video"))
        video_button.pack(side="left", padx=10)
        
        mp3_button = tk.Button(button_frame, text="MP3", command=lambda: self.create_option_screen("MP3"))
        mp3_button.pack(side="left", padx=10)

        self.main_frame.pack(fill="both", expand=True)

    def create_option_screen(self, option):
        self.clear_frame(self.main_frame)
        self.download_option = option
        
        tk.Label(self.main_frame, text=f"Download {option}").pack(pady=10)
        
        self.url_entry = tk.Entry(self.main_frame, width=30)
        self.url_entry.pack(pady=5)
        self.url_entry.insert(0, "Enter URL here")
        
        choose_dir_button = tk.Button(self.main_frame, text="Choose Directory", command=self.choose_directory)
        choose_dir_button.pack(pady=5)
        
        self.selected_dir = tk.Label(self.main_frame, text="No directory selected")
        self.selected_dir.pack(pady=5)
        
        button_frame_2 = tk.Frame(self.main_frame)
        button_frame_2.pack(pady=10)
        
        download_button = tk.Button(button_frame_2, text="Download", command=self.download_video)
        download_button.pack(side="right", padx=10)
        
        back_button = tk.Button(button_frame_2, text="Back", command=self.create_main_screen)
        back_button.pack(side="left", padx=5)

    def clear_frame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def choose_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.selected_dir.config(text=directory)
        else:
            self.selected_dir.config(text="No directory selected")
            
    def download_video(self):
        url = self.url_entry.get()
        directory = self.selected_dir.cget("text")
        option = self.download_option
        
        if directory == "No directory selected":
            messagebox.showerror("Error", "Please select a directory")
            return
        
        try:
            yt = YouTube(url)
                    
            if option == "MP3":
                audio = yt.streams.filter(only_audio=True).first()
                audio.download(directory, filename=yt.title+".mp3")
            else:
                video = yt.streams.filter(file_extension="mp4")
                audio = yt.streams.filter(only_audio=True).first()
                skip = 1 # Skip the first stream (360p is always first)
                for i in video:
                    if skip == 0:
                        stream = i
                        break
                    else:
                        skip -= 1
                        
                stream.download(filename= "video.mp4")
                audio.download(filename= "audio.mp3")
                audio = AudioFileClip("audio.mp3")
                video = VideoFileClip("video.mp4")
                result = video.set_audio(audio)
                result.write_videofile(yt.title+".mp4")
                os.remove("video.mp4")
                os.remove("audio.mp3")
                shutil.move(yt.title+".mp4", directory)
            messagebox.showinfo("Success", "Download complete")
        except exceptions.PytubeFixError as e:
            messagebox.showerror("Error", f"Failed to download video: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
