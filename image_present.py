import matplotlib.pyplot as plt
import os
from PIL import Image

# Set the folder where images are stored
image_folder = '100_images'

# Path to the sorted images text file
sorted_images_file = os.path.join(image_folder, "sorted_images.txt")

# Read the sorted image filenames from the text file
with open(sorted_images_file, "r") as file:
    sorted_filenames = [line.strip() for line in file if line.strip()]

# Get the full paths for each filename in the specified order
sorted_images = [os.path.join(image_folder, filename) for filename in sorted_filenames]

# Define grid dimensions
n_images = len(sorted_images)
n_rows = 4  # Number of rows
n_cols = (n_images + n_rows - 1) // n_rows  # Calculate columns per row based on total images

# Set up the plot grid
fig, axes = plt.subplots(n_rows, n_cols, figsize=(2 * n_cols, 8))  # Adjusted figure size for better visibility

# Plot each image in the grid
for i, image_path in enumerate(sorted_images):
    row, col = divmod(i, n_cols)
    ax = axes[row, col]
    img = Image.open(image_path).convert('L')  # Convert to grayscale
    ax.imshow(img, cmap='gray')  # Display as grayscale
    
    # Extract and display the degradation level from the filename
    degradation_level = image_path.split('_')[0]  # Adjust this if degradation is not first
    ax.set_title(f"{degradation_level}", fontsize=10)
    ax.axis('off')

# Hide any unused subplots
for j in range(i + 1, n_rows * n_cols):
    row, col = divmod(j, n_cols)
    axes[row, col].axis('off')

plt.suptitle("Crater Images by Degradation Level (Ordered by sorted_images.txt)", fontsize=16, y=1.05)
plt.tight_layout()
plt.subplots_adjust(left=0.01, right=0.99, top=0.9, bottom=0.01, wspace=0.1, hspace=0.1)  # Adjust layout spacing
plt.show()
