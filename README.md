# Crater_degTool
This tool is designed to rank crater images by degradation level.

---

### Installation Instructions
1. Clone this repository to your local machine.
2. Place your crater image files into the repository's folder.
3. Open a terminal and switch to PowerShell.
4. Run `pip install -r requirements.txt` to install the necessary dependencies.

---

### Run the Tool to Rank Degradation Levels
1. Execute the command `python quick_sort.py` in the terminal to launch the GUI.
2. Two crater images will appear side-by-side in the window. Use the provided buttons to select the crater that appears more degraded (i.e., with a lighter or more worn rim).

   <p align="center">
       <img src="https://github.com/user-attachments/assets/f3b3584a-153c-47da-8a4b-53ece2b3c037" width="50%">
   </p>

3. The sorted results will be saved in your image folder as "sorted_images.txt".
4. To visually verify and adjust the degradation order, run `gui_drag.py`. You can then drag the images to fine-tune the sequence according to your judgment.

   <p align="center">
       <img src="https://github.com/user-attachments/assets/27d09b18-aef8-4d8c-a047-8a6495c9f090" width="50%">
   </p>

---

This approach uses HTML's `<img>` tag with the `width="50%"` attribute to reduce the image size to half of its original width, centered within the document using `<p align="center">`. This formatting should render well on GitHub and other markdown viewers, preserving the reduced image size and layout.
