import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image
import os
import math


canvas_size = (1200, 1200) # Default canvas size


def create_photo_collage(image_folder, output_path):
    image_paths = [os.path.join(image_folder, f) for f in os.listdir(
        image_folder) if f.endswith(('jpg', 'jpeg', 'png'))]
    num_images = len(image_paths)

    if num_images == 0:
        messagebox.showerror(
            "Error", "No images found in the selected folder.")
        return

    grid_size = round(math.sqrt(num_images))
    while grid_size * grid_size < num_images:
        grid_size += 1

    thumb_size = canvas_size[0] // grid_size
    collage = Image.new('RGBA', canvas_size, (255, 255, 255, 0))

    x, y = 0, 0
    for img_path in image_paths:
        img = Image.open(img_path)
        img = img.resize((thumb_size, thumb_size), Image.LANCZOS)
        collage.paste(img, (x * thumb_size, y * thumb_size))

        x += 1
        if x >= grid_size:
            x = 0
            y += 1

    if y < grid_size:
        for fill_y in range(y, grid_size):
            for fill_x in range(grid_size):
                if fill_y * grid_size + fill_x >= num_images:
                    repeat_img = Image.open(
                        image_paths[(fill_y * grid_size + fill_x) % num_images])
                    repeat_img = repeat_img.resize(
                        (thumb_size, thumb_size), Image.LANCZOS)
                    collage.paste(
                        repeat_img, (fill_x * thumb_size, fill_y * thumb_size))

    collage.save(output_path, format='PNG')
    output_label.configure(text=f"Collage saved to: {output_path}")


def select_folder():
    global folder_selected
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        folder_label.configure(text=f"Selected: {folder_selected}")


def confirm_action():
    if folder_selected:
        output_path = os.path.join(os.getcwd(), "collage_output.png")
        create_photo_collage(folder_selected, output_path)
    else:
        messagebox.showerror("Error", "No folder selected.")


if __name__ == "__main__":
    # GUI Setup
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    app = ctk.CTk()
    app.title("Photo Collage Maker")
    app.geometry("400x300")

    label = ctk.CTkLabel(
        app, text="Select an image folder:", font=("Arial", 14))
    label.pack(pady=10)

    button_select = ctk.CTkButton(
        app, text="Select Folder", command=select_folder)
    button_select.pack(pady=5)

    folder_label = ctk.CTkLabel(
        app, text="No folder selected", font=("Arial", 12), wraplength=380)
    folder_label.pack(pady=5)

    button_confirm = ctk.CTkButton(
        app, text="Create Collage", command=confirm_action)
    button_confirm.pack(pady=10)

    output_label = ctk.CTkLabel(
        app, text="", font=("Arial", 12), wraplength=380)
    output_label.pack(pady=5)

    app.mainloop()
