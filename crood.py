import tkinter as tk
from tkinter import messagebox
import pyautogui
import keyboard

class RegionSelector:
    def __init__(self, root):
        self.root = root
        self.root.title("Region Selector")
        self.root.geometry("400x250")

        self.regions = {
            "question": {"top_left": None, "bottom_right": None},
            "A": {"top_left": None, "bottom_right": None},
            "B": {"top_left": None, "bottom_right": None},
            "C": {"top_left": None, "bottom_right": None},
            "D": {"top_left": None, "bottom_right": None},
        }

        self.label = tk.Label(root, text="Select the regions for the question and answers.")
        self.label.pack(pady=10)

        self.select_question_button = tk.Button(root, text="Select Question Region", command=lambda: self.set_region("question"))
        self.select_question_button.pack(pady=5)

        self.select_A_button = tk.Button(root, text="Select Answer A Region", command=lambda: self.set_region("A"))
        self.select_A_button.pack(pady=5)

        self.select_B_button = tk.Button(root, text="Select Answer B Region", command=lambda: self.set_region("B"))
        self.select_B_button.pack(pady=5)

        self.select_C_button = tk.Button(root, text="Select Answer C Region", command=lambda: self.set_region("C"))
        self.select_C_button.pack(pady=5)

        self.select_D_button = tk.Button(root, text="Select Answer D Region", command=lambda: self.set_region("D"))
        self.select_D_button.pack(pady=5)

        self.done_button = tk.Button(root, text="Done", command=self.finish_selection, state=tk.DISABLED)
        self.done_button.pack(pady=10)

    def set_region(self, region):
        self.root.withdraw()  # Hide the main window
        messagebox.showinfo("Info", f"Move the mouse to the top-left corner of the {region} region and press SPACE.")
        top_left = self.get_mouse_position()
        if top_left:
            messagebox.showinfo("Info", f"Move the mouse to the bottom-right corner of the {region} region and press SPACE.")
            bottom_right = self.get_mouse_position()
            if bottom_right:
                self.regions[region]["top_left"] = top_left
                self.regions[region]["bottom_right"] = bottom_right
        self.root.deiconify()  # Restore the main window
        self.check_selection()

    def get_mouse_position(self):
        print("Press SPACE to capture the mouse position.")
        while True:
            if keyboard.is_pressed('space'):  # Wait for SPACE key press
                return pyautogui.position()
            if keyboard.is_pressed('esc'):  # Allow canceling with ESC key
                return None

    def check_selection(self):
        # Enable the "Done" button only if all regions are selected
        all_selected = all(
            region["top_left"] and region["bottom_right"]
            for region in self.regions.values()
        )
        if all_selected:
            self.done_button.config(state=tk.NORMAL)

    def finish_selection(self):
        # Display the selected regions in a message box
        result = "Selected Regions:\n"
        for region, coords in self.regions.items():
            result += f"{region}: Top-Left={coords['top_left']}, Bottom-Right={coords['bottom_right']}\n"
        messagebox.showinfo("Selection Complete", result)

        # Print the selected regions to the console
        print("Selected Regions:")
        for region, coords in self.regions.items():
            print(f"{region}: Top-Left={coords['top_left']}, Bottom-Right={coords['bottom_right']}")

        self.root.quit()

# Create the main application window and start the program
if __name__ == "__main__":
    root = tk.Tk()
    app = RegionSelector(root)
    root.mainloop()
