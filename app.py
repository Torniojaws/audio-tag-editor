import tkinter as tk
from tkinter.filedialog import askopenfilename
import eyed3
from tkinterdnd2 import DND_FILES, TkinterDnD


class ResizableWindow(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()

        # Set the default window size
        self.geometry('640x480')

        # Set the minimum window size
        self.minsize(320, 240)

        # Allow the window to be resizable
        self.resizable(True, True)

        # Set the window title
        self.title('Audio Tag Editor')

        # Add instructions
        self.instructions = tk.Label(
            self,
            text='Drag and drop a file to populate the tag data'
        )
        self.instructions.pack()

        # Add a label to display the artist and title
        self.artist_label = tk.Label(self, text='Artist: ')
        self.artist_label.pack()
        self.title_label = tk.Label(self, text='Title: ')
        self.title_label.pack()

        # Enable dropping files onto the window
        self.drop_target_register(DND_FILES)
        self.dnd_bind('<<Drop>>', self.handle_drop)

    def handle_drag_enter(self, event):
        self.configure(bg='#cccccc')

    def handle_drag_leave(self, event):
        self.configure(bg='white')

    def handle_drop(self, event):
        file_path = event.data.replace('{', '').replace('}', '')
        print('Handling drop, event data', event.data)

        if file_path.endswith('.mp3'):
            audiofile = eyed3.load(file_path)
            print('Dropped file in eyed3 has data:', audiofile)

            if audiofile.tag is not None:
                artist = audiofile.tag.artist
                title = audiofile.tag.title

                if artist is not None:
                    self.artist_label.config(text='Artist: ' + artist)

                if title is not None:
                    self.title_label.config(text='Title: ' + title)
        else:
            print('filepath', file_path, 'did not end with .mp3')

        self.configure(bg='white')

    def ask_for_file(self):
        file_path = askopenfilename(filetypes=[('MP3 files', '*.mp3')])
        if file_path:
            audiofile = eyed3.load(file_path)

            if audiofile.tag is not None:
                artist = audiofile.tag.artist
                title = audiofile.tag.title

                if artist is not None:
                    self.artist_label.config(text='Artist: ' + artist)

                if title is not None:
                    self.title_label.config(text='Title: ' + title)


if __name__ == '__main__':
    # Create an instance of the ResizableWindow class
    window = ResizableWindow()

    # Start the Tkinter event loop
    window.mainloop()
