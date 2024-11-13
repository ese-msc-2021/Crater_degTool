import os
import shutil

# Define paths
source_folder = '100_images_select'  # Folder containing original images
text_file = os.path.join(source_folder, 'new_sorted_images_with_levels.txt')  # Text file with new image names
destination_folder = '100_images_with_rank'  # New folder for images with ranks

# Create destination folder if it doesn't exist
if not os.path.exists(destination_folder):
    os.makedirs(destination_folder)

# Read image filenames from text file
with open(text_file, 'r') as file:
    image_filenames = [line.strip() for line in file if line.strip()]

# Copy and rename images based on the new names from the text file
for filename in image_filenames:
    # Extract the original filename (remove the rank prefix)
    original_filename = '_'.join(filename.split('_')[1:])  # This removes the prefix rank (e.g., 1_, 2_, etc.)

    # Construct source and destination paths
    source_path = os.path.join(source_folder, original_filename)
    destination_path = os.path.join(destination_folder, filename)  # Use the full filename with rank prefix

    # Copy image with new name to the destination folder
    if os.path.exists(source_path):
        shutil.copy(source_path, destination_path)
        print(f"Copied {source_path} to {destination_path}")
    else:
        print(f"File {source_path} does not exist and was skipped.")

print("All images have been copied and renamed based on the new list.")
