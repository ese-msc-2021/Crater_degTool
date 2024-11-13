import tkinter as tk
from PIL import Image, ImageTk
import os
from glob import glob
import random

# Load all crater images from the specified folder and convert paths to absolute
image_folder = '10_images'
crater_images = [os.path.abspath(path) for path in glob(os.path.join(image_folder, "*.jpg"))]
print('Crater images list:', crater_images)

# Paths to demonstration images for degradation levels 1 to 4
demo_image_paths = [
    os.path.abspath(r"C:/Users/jamil/OneDrive/desktop/PhD/Phase_2/gui/classification/demonstration_img/1.jpg"),
    os.path.abspath(r"C:/Users/jamil/OneDrive/desktop/PhD/Phase_2/gui/classification/demonstration_img/2.jpg"),
    os.path.abspath(r"C:/Users/jamil/OneDrive/desktop/PhD/Phase_2/gui/classification/demonstration_img/3.jpg"),
    os.path.abspath(r"C:/Users/jamil/OneDrive/desktop/PhD/Phase_2/gui/classification/demonstration_img/4.jpg")
]

# Global variables for the main window, image labels, and counters
window = tk.Tk()
window.title("Crater Comparison")
button_press_count = 0  # Counter to track the number of button presses
current_left_image = None
current_right_image = None
sort_index = 0  # Index for the sorting algorithm
min_index = 0  # Index of the minimum element

# Initialize points dictionary to track scores for each image
image_scores = {image: 0 for image in crater_images}  # Tracks wins in comparisons

# File path to save intermediate results
intermediate_file = os.path.join(image_folder, "intermediate_scores.txt")

# Function to load existing scores and sorting indices from the intermediate file
def load_existing_scores():
    global button_press_count, current_left_image, current_right_image, sort_index, min_index
    if os.path.exists(intermediate_file):
        with open(intermediate_file, "r") as file:
            for line in file:
                if "Total Button Presses:" in line:
                    button_press_count = int(line.strip().split(": ")[1])
                elif "Last Comparison:" in line:
                    parts = line.strip().split("Last Comparison: ")[1].split(", ")
                    if len(parts) == 2:
                        last_left_image, last_right_image = parts
                        for image_path in crater_images:
                            if os.path.basename(image_path) == last_left_image:
                                current_left_image = image_path
                            if os.path.basename(image_path) == last_right_image:
                                current_right_image = image_path
                elif "Sort Index:" in line:
                    sort_index = int(line.strip().split(": ")[1])
                elif "Min Index:" in line:
                    min_index = int(line.strip().split(": ")[1])
                elif " - Score: " in line:
                    parts = line.strip().split(" - Score: ")
                    image_name, score = parts[0], int(parts[1])
                    for image_path in crater_images:
                        if os.path.basename(image_path) == image_name:
                            image_scores[image_path] = score
    print("Loaded existing scores and indices:", image_scores, sort_index, min_index)

# Function to save intermediate scores and sorting indices
def save_intermediate_scores():
    with open(intermediate_file, "w") as file:
        file.write(f"Total Button Presses: {button_press_count}\n")
        if current_left_image and current_right_image:
            file.write(f"Last Comparison: {os.path.basename(current_left_image)}, {os.path.basename(current_right_image)}\n")
        file.write(f"Sort Index: {sort_index}\n")
        file.write(f"Min Index: {min_index}\n")
        for image_path, score in image_scores.items():
            file.write(f"{os.path.basename(image_path)} - Score: {score}\n")
    print("Intermediate scores saved.")

# Function to initialize the main comparison window
def initialize_interface():
    # Configure grid to evenly distribute space
    window.columnconfigure([0, 1, 2, 3], weight=1)
    window.rowconfigure([0, 1], weight=1, minsize=100)

    # Load and display demonstration images with degradation levels
    for i, path in enumerate(demo_image_paths):
        demo_image = ImageTk.PhotoImage(Image.open(path).resize((100, 100)))
        demo_label = tk.Label(window, image=demo_image)
        demo_label.grid(row=0, column=i, padx=10, pady=10)
        label_text = tk.Label(window, text=f"Level {i + 1}")
        label_text.grid(row=1, column=i, padx=10, pady=5)
        demo_label.image = demo_image  # Keep a reference to avoid garbage collection

    # Create labels for the comparison images
    global label1, label2, btn1, btn2, btn3
    label1 = tk.Label(window)
    label1.grid(row=2, column=0, columnspan=2, padx=20, pady=10, sticky='e')
    label2 = tk.Label(window)
    label2.grid(row=2, column=2, columnspan=2, padx=20, pady=10, sticky='w')

    # Create buttons for selecting which image is more degraded or if they are similar
    btn1 = tk.Button(window, text="Left is More Degraded", command=lambda: select_image("left"))
    btn1.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky='e')
    btn2 = tk.Button(window, text="Right is More Degraded", command=lambda: select_image("right"))
    btn2.grid(row=3, column=2, columnspan=2, padx=10, pady=10, sticky='w')
    btn3 = tk.Button(window, text="Similar Degradation", command=lambda: select_image("similar"))
    btn3.grid(row=4, column=1, columnspan=2, padx=10, pady=10)

# Function to update the images for comparison
def update_comparison(img1, img2):
    global current_left_image, current_right_image
    current_left_image = os.path.abspath(img1)
    current_right_image = os.path.abspath(img2)

    # Load and display images
    image1 = ImageTk.PhotoImage(Image.open(current_left_image).resize((200, 200)))
    image2 = ImageTk.PhotoImage(Image.open(current_right_image).resize((200, 200)))
    label1.config(image=image1)
    label2.config(image=image2)
    label1.image = image1  # Keep a reference to avoid garbage collection
    label2.image = image2  # Keep a reference to avoid garbage collection

# Function to handle the user’s decision and proceed with the next comparison
def select_image(choice):
    global image_scores, current_left_image, current_right_image, button_press_count
    button_press_count += 1  # Increment the button press counter

    # Update scores based on user selection
    if choice == "left":
        image_scores[current_left_image] += 1  # Add 1 point to the left image
    elif choice == "right":
        image_scores[current_right_image] += 1  # Add 1 point to the right image
    elif choice == "similar":
        image_scores[current_left_image] += 1  # Add 1 point to both images
        image_scores[current_right_image] += 1

    print(f"Scores updated: {current_left_image} (Score: {image_scores[current_left_image]}), "
          f"{current_right_image} (Score: {image_scores[current_right_image]})")

    # Save progress and quit the window to continue
    save_intermediate_scores()
    window.quit()

# Function to compare images and prompt user for input
def user_compare(img1, img2):
    update_comparison(img1, img2)
    window.mainloop()
    # After user input, compare scores
    return image_scores[img1] > image_scores[img2]

# Function to perform selection sort with user input for comparison
def selection_sort(arr):
    global sort_index, min_index
    n = len(arr)
    while sort_index < n - 1:
        min_idx = sort_index
        min_index = sort_index + 1 if min_index <= sort_index else min_index
        while min_index < n:
            # Compare arr[min_idx] and arr[min_index]
            if user_compare(arr[min_idx], arr[min_index]):
                min_idx = min_index
            # Save after each comparison
            save_intermediate_scores()
            min_index += 1
        # Swap the found minimum element with the first element
        arr[sort_index], arr[min_idx] = arr[min_idx], arr[sort_index]
        sort_index += 1
        min_index = sort_index  # Reset min_index for the next iteration
        save_intermediate_scores()

# Load existing scores and last comparison, initialize the interface, and start sorting
load_existing_scores()  # Load scores and last viewed images if they exist
initialize_interface()

# Start sorting from the saved indices
selection_sort(crater_images)
save_intermediate_scores()  # Final save of the scores
print("Sorted crater images by degradation level and score:",
      [f"{os.path.basename(img)} (Score: {image_scores[img]})" for img in crater_images])
