from retico_vision.vision import ImageIU
from retico_core.abstract import AbstractConsumingModule

import threading
from collections import deque
import tkinter as tk
from tkinter import Label
from PIL import Image, ImageTk

class ScreenModule(AbstractConsumingModule):
    """
    A module that displays images on the screen.
    """
    
    @staticmethod
    def name():
        return "ScreenModule"
    
    @staticmethod
    def description():
        return "A module that displays images on the screen."
    
    @staticmethod
    def input_ius():
        return [ImageIU]
    
    def __init__(self, fps=30):
        """
        Initialize the ScreenModule with a specified frames per second (fps).
        Note that the fps parameter is an upper limit for the display refresh rate.
        
        Args:
            fps (int): The desired frames per second for the display. Default is 30.
        """
        super().__init__()
        self._image = None
        self._running = False
        self.fps = fps
        self.queue = deque(maxlen=1)
        self.display_thread = None
        self.root = None
        self.label = None
    
    def setup(self):
        """
        Set up the module, e.g., initialize display settings.
        """
        self._running = True
          # Start the display thread
        self.display_thread = threading.Thread(target=self._display_loop, daemon=True)
        self.display_thread.start()
    
    def shutdown(self):
        """
        Clean up the module, e.g., close display windows.
        """
        self._running = False
        if self.display_thread and self.display_thread.is_alive():
            self.display_thread.join(timeout=1.0)
          # Close tkinter window if it exists
        if self.root:
            try:
                self.root.quit()
                self.root.destroy()
            except:
                pass
    
    def _display_loop(self):
        """
        Main display loop that runs in a separate thread.
        """
        # Create tkinter window
        self.root = tk.Tk()
        self.root.title("Screen Module")
        
        # Create label to hold the image
        self.label = Label(self.root)
        self.label.pack(expand=True, fill='both')
        
        # Start the update loop
        self._update_display()
        
        # Start the tkinter main loop
        self.root.mainloop()
    
    def _update_display(self):
        """
        Update the display with new images from the queue.
        """
        if self._running and len(self.queue) > 0:
            try:
                image = self.queue.popleft()
                if image is not None:
                    # Resize image if necessary
                    if hasattr(image, 'size'):
                        # If it's already a PIL Image
                        pil_image = image
                    else:
                        # Convert numpy array to PIL Image if needed
                        pil_image = Image.fromarray(image)
                    
                    # Convert to tkinter PhotoImage
                    photo = ImageTk.PhotoImage(pil_image)
                    
                    # Update the label with new image
                    self.label.configure(image=photo)
                    self.label.image = photo  # Keep a reference
                    
            except Exception as e:
                print(f"Error updating display: {e}")
        
        # Schedule next update
        if self._running and self.root:
            self.root.after(int(1000 / self.fps), self._update_display)
    
    def display_image(self, image):
        """
        Queue the given image for display in a thread-safe manner.
        """
        if self._running and image is not None:
            self.queue.append(image)
    
    def process_update(self, update_message):
        for iu, um in update_message:
            if isinstance(iu, ImageIU):
                self._image = iu.image
                self.display_image(self._image)
