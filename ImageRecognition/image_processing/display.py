import os
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk

def display_duplicates(duplicates):
    fig, axes = plt.subplots(1, 2, figsize=(15, 5))
    index = 0

    def update_display():
        for ax in axes:
            ax.clear()
        if duplicates:
            for ax, img_path in zip(axes, duplicates[index]):
                img = Image.open(img_path)
                ax.imshow(img)
                ax.set_title(os.path.basename(img_path))
                ax.axis('off')
        fig.canvas.draw_idle()

    def custom_forward(*args):
        nonlocal index
        index = (index + 1) % len(duplicates)
        update_display()

    def custom_back(*args):
        nonlocal index
        index = (index - 1) % len(duplicates)
        update_display()

    NavigationToolbar2Tk.forward = custom_forward
    NavigationToolbar2Tk.back = custom_back

    update_display()
    plt.show()