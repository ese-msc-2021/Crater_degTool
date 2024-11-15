import os
import tkinter as tk
from tkinter import messagebox, Scrollbar, Canvas, Frame
from PIL import Image, ImageTk

class ImageReorderApp:
    def __init__(self, root, image_folder, sorted_images_file):
        self.root = root
        self.root.title("Image Reorder GUI")
        
        self.image_folder = image_folder
        self.sorted_images_file = sorted_images_file

        # Load images
        with open(self.sorted_images_file, "r") as file:
            self.sorted_filenames = [line.strip() for line in file if line.strip()]
        
        self.image_paths = [os.path.join(self.image_folder, filename) for filename in self.sorted_filenames]
        self.images = [Image.open(path).resize((100, 100)) for path in self.image_paths]  # Resize images for display
        self.tk_images = [ImageTk.PhotoImage(img) for img in self.images]

        # Set up scrollable canvas
        self.canvas = Canvas(self.root, width=800, height=400)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar configuration
        scrollbar = Scrollbar(self.root, command=self.canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.config(yscrollcommand=scrollbar.set)

        # Frame inside canvas to hold images
        self.frame = Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")
        self.frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # Initialize image positions
        self.image_labels = []
        self.init_positions()

        # Save button
        save_button = tk.Button(self.root, text="Save Order", command=self.save_order)
        save_button.pack(pady=10)

        # Drag variables
        self.dragged_label = None
        self.original_index = None

    def init_positions(self):
        # Create image labels in a grid layout
        for i, img in enumerate(self.tk_images):
            label = tk.Label(self.frame, image=img)
            label.grid(row=i // 10, column=i % 10, padx=5, pady=5)
            label.bind("<Button-1>", self.start_drag)  # Bind left-click for drag start
            label.image_name = self.sorted_filenames[i]  # Attach filename to label for tracking
            self.image_labels.append(label)

    def start_drag(self, event):
        # Find the clicked label and store its index
        self.dragged_label = event.widget
        self.original_index = self.image_labels.index(self.dragged_label)

        # Lift the label to bring it to the top of the display
        self.dragged_label.lift()

        # Bind mouse movement and release to complete the drag-and-drop
        self.dragged_label.bind("<B1-Motion>", self.drag)
        self.dragged_label.bind("<ButtonRelease-1>", self.drop)

    def drag(self, event):
        # Move the label with the cursor
        self.dragged_label.place(x=event.x_root - self.frame.winfo_rootx(), y=event.y_root - self.frame.winfo_rooty())

    def drop(self, event):
        # Calculate the target position in the grid
        x, y = event.x_root - self.frame.winfo_rootx(), event.y_root - self.frame.winfo_rooty()
        row, col = y // 110, x // 110
        target_index = row * 10 + col

        # Place dragged label in target position and shift other labels
        if target_index < len(self.image_labels):
            self.image_labels.insert(target_index, self.image_labels.pop(self.original_index))
            self.update_grid()
        
        # Unbind drag and drop events for the current label
        self.dragged_label.unbind("<B1-Motion>")
        self.dragged_label.unbind("<ButtonRelease-1>")
        self.dragged_label = None

    def update_grid(self):
        # Update the position of all labels in the grid based on current order
        for i, label in enumerate(self.image_labels):
            label.grid(row=i // 10, column=i % 10, padx=5, pady=5)
            label.place_forget()  # Reset position to grid layout

    def save_order(self):
        # Retrieve the filenames from the reordered image labels
        new_order = [label.image_name for label in self.image_labels]

        # Specify a new filename for saving the reordered list
        new_sorted_images_file = os.path.join(self.image_folder, "new_sorted_images.txt")

        # Save the new order of filenames to the new file
        with open(new_sorted_images_file, "w") as file:
            file.write("\n".join(new_order))

        messagebox.showinfo("Saved", f"Image order has been saved to {new_sorted_images_file}.")

if __name__ == "__main__":
    # Folder and sorted images file
    image_folder = '100_images_select'
    sorted_images_file = os.path.join(image_folder, "sorted_images.txt")

    root = tk.Tk()
    app = ImageReorderApp(root, image_folder, sorted_images_file)
    root.mainloop()
