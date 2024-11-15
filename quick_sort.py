import tkinter as tk
from PIL import Image, ImageTk
import os
from glob import glob
import json

# ==============================
# Global Variables and Settings
# ==============================

# Load all crater images from the specified folder and convert paths to absolute
image_folder = '100_images_select'  # Update this to your image folder
crater_images = [os.path.abspath(path) for path in glob(os.path.join(image_folder, "*.jpg"))]
print('Crater images list:', crater_images)

# Paths to demonstration images for degradation levels 1 to 4
demo_image_paths = [
    os.path.abspath(r"demonstration_img/1.jpg"),  # Update these paths accordingly
    os.path.abspath(r"demonstration_img/2.jpg"),
    os.path.abspath(r"demonstration_img/3.jpg"),
    os.path.abspath(r"demonstration_img/4.jpg")
]

# File paths to save intermediate results
state_file = os.path.join(image_folder, "merge_sort_state.json")
comparison_cache_file = os.path.join(image_folder, "comparison_cache.json")
sorted_images_file = os.path.join(image_folder, "sorted_images.txt")

# Initialize variables for sorting state and logging
image_scores = {image: 0 for image in crater_images}
merge_counter = 0
total_comparisons = 0

# ==============================
# Tkinter GUI Setup
# ==============================

window = tk.Tk()
window.title("Crater Comparison")
button_press_count = 0

# Global variables for GUI elements
label1, label2, btn1, btn2, btn3 = None, None, None, None, None
current_left_image, current_right_image = None, None

# ==============================
# State Management Functions
# ==============================

def load_sorting_state():
    """Load existing sorting state from the state file."""
    global image_scores, merge_counter, total_comparisons
    if os.path.exists(state_file):
        with open(state_file, "r") as file:
            state = json.load(file)
            image_scores.update({os.path.abspath(k): v for k, v in state.get('image_scores', {}).items()})
            merge_counter = state.get('merge_counter', 0)
            total_comparisons = state.get('total_comparisons', 0)
        print("Loaded existing sorting state.")
    else:
        print("No existing sorting state found.")

def save_sorting_state():
    """Save the current sorting state to the state file."""
    state = {
        'image_scores': image_scores,
        'merge_counter': merge_counter,
        'total_comparisons': total_comparisons
    }
    with open(state_file, "w") as file:
        json.dump(state, file, indent=4)
    print("Sorting state saved.")

def save_sorted_images():
    """Save the sorted images list to a text file."""
    with open(sorted_images_file, "w") as file:
        for img in sorted_images:
            file.write(f"{os.path.basename(img)}\n")
    print("Sorted images saved to", sorted_images_file)

# ==============================
# GUI Initialization Functions
# ==============================

def initialize_interface():
    """Initialize the main comparison window."""
    window.columnconfigure([0, 1, 2, 3], weight=1)
    window.rowconfigure([0, 1, 2, 3, 4], weight=1, minsize=100)

    # Display demonstration images with degradation levels
    for i, path in enumerate(demo_image_paths):
        demo_image = ImageTk.PhotoImage(Image.open(path).resize((100, 100)))
        demo_label = tk.Label(window, image=demo_image)
        demo_label.grid(row=0, column=i, padx=10, pady=10)
        label_text = tk.Label(window, text=f"Level {i + 1}")
        label_text.grid(row=1, column=i, padx=10, pady=5)
        demo_label.image = demo_image  # Keep a reference to avoid garbage collection

    # Set up labels and buttons for comparison
    global label1, label2, btn1, btn2, btn3
    label1 = tk.Label(window)
    label1.grid(row=2, column=0, columnspan=2, padx=20, pady=10, sticky='e')
    label2 = tk.Label(window)
    label2.grid(row=2, column=2, columnspan=2, padx=20, pady=10, sticky='w')
    btn1 = tk.Button(window, text="Left is More Degraded", command=lambda: select_image("left"))
    btn1.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky='e')
    btn2 = tk.Button(window, text="Right is More Degraded", command=lambda: select_image("right"))
    btn2.grid(row=3, column=2, columnspan=2, padx=10, pady=10, sticky='w')
    btn3 = tk.Button(window, text="Similar Degradation", command=lambda: select_image("similar"))
    btn3.grid(row=4, column=1, columnspan=2, padx=10, pady=10)

def update_comparison(img1, img2):
    """Update the images displayed for comparison."""
    global current_left_image, current_right_image
    current_left_image = img1
    current_right_image = img2
    image1 = ImageTk.PhotoImage(Image.open(current_left_image).resize((200, 200)))
    image2 = ImageTk.PhotoImage(Image.open(current_right_image).resize((200, 200)))
    label1.config(image=image1)
    label2.config(image=image2)
    label1.image = image1
    label2.image = image2

# ==============================
# User Interaction Functions
# ==============================

def select_image(choice):
    """Handle the user's decision and store the comparison result."""
    global button_press_count, comparison_result
    button_press_count += 1
    if choice == "left":
        comparison_result = 1
    elif choice == "right":
        comparison_result = -1
    elif choice == "similar":
        comparison_result = 0
    save_sorting_state()
    window.quit()

def compare_images(img1, img2):
    """Compare two images with or without user input."""
    global total_comparisons
    total_comparisons += 1
    update_comparison(img1, img2)
    window.mainloop()
    return comparison_result

# ==============================
# Merge Sort Implementation
# ==============================

def merge_sort(images):
    """Perform merge sort on the list of images."""
    if len(images) <= 1:
        return images
    mid = len(images) // 2
    left_sorted = merge_sort(images[:mid])
    right_sorted = merge_sort(images[mid:])
    return merge(left_sorted, right_sorted)
def merge(left, right):
    """Merge two sorted lists into one sorted list."""
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if compare_images(left[i], right[j]) == 1:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
        save_sorting_state()  # Keep saving the state for progress tracking

    result.extend(left[i:])
    result.extend(right[j:])
    return result


def log_merge_sequence(result, step):
    """Log the current merge sequence to a file."""
    sequence_file = os.path.join(image_folder, f"sequence_step_{step}.txt")
    with open(sequence_file, "w") as file:
        for img in result:
            file.write(f"{os.path.basename(img)}\n")
    print(f"Merge Step {step}: {[os.path.basename(img) for img in result]}")
    print(f"Sequence saved to {sequence_file}")

# ==============================
# Main Execution Flow
# ==============================

if __name__ == "__main__":
    load_sorting_state()
    initialize_interface()
    sorted_images = merge_sort(crater_images)
    print("Sorting complete.")
    save_sorting_state()
    save_sorted_images()
    window.destroy()
