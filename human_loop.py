import os
import shutil  # Import for copying files
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# Directories for main images and comparison images
main_image_folder = "loop1_regression"  # Update to the correct path for main images
comparison_image_folder = "renamed_100_images"  # Update to the correct path for comparison images
verification_folder = "human_verification_loop1"  # Folder for saving verified images

# Ensure the verification folder exists
if not os.path.exists(verification_folder):
    os.makedirs(verification_folder)

# Load images from a specified folder and extract degradation levels
def load_images(folder):
    images = []
    try:
        files = os.listdir(folder)
        for filename in files:
            if filename.lower().endswith((".jpg", ".png")):
                try:
                    # Extract the degradation level from the part before the first underscore
                    degradation_level = float(filename.split('_')[0])
                    images.append((degradation_level, filename))
                except ValueError:
                    continue
    except FileNotFoundError:
        messagebox.showerror("Error", f"Folder not found: {folder}")
    return sorted(images, key=lambda x: x[0])

# GUI class
class CraterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Crater Degradation Level Review")
        
        # Load images from both folders
        self.main_images = load_images(main_image_folder)
        self.comparison_images = load_images(comparison_image_folder)
        self.current_index = 0

        # Check if main images were loaded
        if not self.main_images:
            messagebox.showerror("Error", "No images found in the main images folder.")
            self.root.quit()
            return
        
        # Main crater image and label
        self.main_image_label = tk.Label(self.root)
        self.main_image_label.pack()

        self.degradation_label = tk.Label(self.root, font=("Arial", 16))
        self.degradation_label.pack()

        # Comparison images display
        self.similar_images_frame = tk.Frame(self.root)
        self.similar_images_frame.pack()

        # Buttons
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack()

        self.tick_button = tk.Button(self.button_frame, text="✔", command=self.save_selection, font=("Arial", 16))
        self.tick_button.grid(row=0, column=0, padx=5)

        self.cross_button = tk.Button(self.button_frame, text="✘", command=self.next_image, font=("Arial", 16))
        self.cross_button.grid(row=0, column=1, padx=5)

        self.show_image()

    def show_image(self):
        # Check if there are any more images
        if self.current_index >= len(self.main_images):
            messagebox.showinfo("End", "No more images to review.")
            self.root.quit()
            return

        # Clear similar images
        for widget in self.similar_images_frame.winfo_children():
            widget.destroy()
        
        # Display main image
        degradation_level, filename = self.main_images[self.current_index]
        image_path = os.path.join(main_image_folder, filename)
        self.display_main_image(image_path, degradation_level)
        
        # Display similar images
        self.display_similar_images(degradation_level)
        
    def display_main_image(self, image_path, degradation_level):
        # Enlarge main image to 300x300
        image = Image.open(image_path)
        image = image.resize((300, 300), Image.LANCZOS)
        self.main_image = ImageTk.PhotoImage(image)
        self.main_image_label.config(image=self.main_image)
        # Display the degradation level with two decimal places
        self.degradation_label.config(text=f"Degradation Level: {degradation_level:.2f}")

    def display_similar_images(self, main_degradation_level):
        # Set the range for comparison images to ±0.1 of the main degradation level
        lower_bound = main_degradation_level - 0.2
        upper_bound = main_degradation_level + 0.2

        # Collect images within the specified range
        filtered_images = [
            (degradation_level, filename)
            for degradation_level, filename in self.comparison_images
            if lower_bound <= degradation_level <= upper_bound
        ]
        
        # If the number of images is odd, add a placeholder to make the count even
        if len(filtered_images) % 2 != 0:
            filtered_images.append((None, None))  # Placeholder

        # Divide the images into two equal rows
        half = len(filtered_images) // 2
        rows = [filtered_images[:half], filtered_images[half:]]

        # Display images in a 2-row grid layout
        for row_index, row_images in enumerate(rows):
            for col_index, (degradation_level, filename) in enumerate(row_images):
                if filename:
                    image_path = os.path.join(comparison_image_folder, filename)
                    image = Image.open(image_path)
                    image = image.resize((100, 100), Image.LANCZOS)
                    img = ImageTk.PhotoImage(image)

                    img_frame = tk.Frame(self.similar_images_frame)
                    img_frame.grid(row=row_index, column=col_index, padx=5, pady=5)

                    img_label = tk.Label(img_frame, image=img)
                    img_label.image = img  # Keep a reference to avoid garbage collection
                    img_label.pack()

                    level_label = tk.Label(img_frame, text=f"Level: {degradation_level:.2f}", font=("Arial", 10))
                    level_label.pack()
                else:
                    # If a placeholder, leave the cell empty
                    img_frame = tk.Frame(self.similar_images_frame, width=100, height=120)
                    img_frame.grid(row=row_index, column=col_index, padx=5, pady=5)
                    img_frame.pack_propagate(False)

    def save_selection(self):
        # Save the current image to the verification folder
        degradation_level, filename = self.main_images[self.current_index]
        source_path = os.path.join(main_image_folder, filename)
        destination_path = os.path.join(verification_folder, filename)

        # Copy the file to the verification folder
        try:
            shutil.copy(source_path, destination_path)
            messagebox.showinfo("Saved", f"Image saved to verification folder: {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save image: {e}")

        # Move to the next image
        self.next_image()

    def next_image(self):
        # Move to the next image
        self.current_index += 1
        self.show_image()

# Run the application
root = tk.Tk()
app = CraterApp(root)
root.mainloop()
