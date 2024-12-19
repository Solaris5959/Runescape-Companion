from tkinter import *
from PIL import Image, ImageTk
import threading
from NemiForest import NemiForest
#from TravellingMerchant import TravellingMerchant  # Assuming this function exists


class Window(Tk):
    def __init__(self):
        super().__init__()

        # Configure window
        self.title("RS3Helper")
        self.geometry("1000x600")  # Increased resolution
        self.configure(bg="#192134")

        # Toolbar frame
        self.toolbar = Frame(self, bg="#091021", height=50)
        self.toolbar.pack(side="top", fill="x")

        # Buttons in the toolbar
        self.run_nemi_button = Button(self.toolbar, text="Run NemiForest", command=self.run_nemi_forest)
        self.run_nemi_button.pack(side="left", padx=5, pady=10)

        self.run_merchant_button = Button(self.toolbar, text="Run TravellingMerchant", command=self.run_travelling_merchant)
        self.run_merchant_button.pack(side="left", padx=5, pady=10)

        self.exit_button = Button(self.toolbar, text="Exit", command=self.destroy)
        self.exit_button.pack(side="right", padx=5, pady=10)

        # Checklist frame
        self.checklist_frame = Frame(self, bg="#091021", width=300)
        self.checklist_frame.pack(side="right", fill="y")
        self.checklist_frame.pack_propagate(False)  # Prevent the frame from resizing to fit its contents


        # Checklist title
        self.checklist_title = Label(self.checklist_frame, text="Dailies", bg="#091021", font=("Arial", 14, "bold"))
        self.checklist_title.pack(pady=10)

        # Checklist items
        self.checklist_vars = [IntVar() for _ in range(3)]
        self.checklist_items = ["Nemi Forest", "Travelling Merchant", "Daily Challenges"]
        for i, item in enumerate(self.checklist_items):
            check = Checkbutton(self.checklist_frame, text=item, variable=self.checklist_vars[i], bg="#343e57")
            check.pack(anchor="w", padx=10, pady=5)

        # Image frame
        self.image_frame = Frame(self, bg="#192134")
        self.image_frame.pack(side="left", fill="both", expand=True)

        # Dropdown menu for image selection
        self.image_options = ["NemiForest", "TravellingMerchant"]
        self.selected_image = StringVar(value=self.image_options[0])
        self.image_menu = OptionMenu(self.image_frame, self.selected_image, *self.image_options, command=self.refresh_image)
        self.image_menu.pack(side="top", anchor="nw", padx=5, pady=5)

        # Refresh button in the viewport
        self.refresh_button = Button(self.image_frame, text="Refresh Image", command=self.refresh_image)
        self.refresh_button.pack(side="top", anchor="ne", padx=5, pady=5)

        # Placeholder for the image
        self.image_label = Label(self.image_frame, text="Image will appear here", bg="#192134")
        self.image_label.pack(expand=True)

        self.refresh_image()  # Load the initial image

    def run_nemi_forest(self):
        """Run the NemiForest function and display the image."""
        def task():
            try:
                NemiForest()  # Run the function (assumes it saves the image in data/nemi_map.png)
                self.refresh_image()
            except Exception as e:
                self.image_label.config(text=f"Error: {e}")

        threading.Thread(target=task).start()

    def run_travelling_merchant(self):
        """Run the TravellingMerchant function and display the image."""
        def task():
            try:
                #TravellingMerchant()  # Run the function (assumes it saves the image in data/merchant_map.png)
                self.refresh_image()
            except Exception as e:
                self.image_label.config(text=f"Error: {e}")

        threading.Thread(target=task).start()

    def refresh_image(self, *args):
        """Reload the image based on the selected option."""
        image_paths = {
            "NemiForest": "data/nemi_map.png",
            "TravellingMerchant": "data/merchant_map.png"
        }
        selected_path = image_paths.get(self.selected_image.get(), "")

        def task():
            try:
                self.load_image(selected_path)
            except Exception as e:
                self.image_label.config(text=f"Error: {e}")

        threading.Thread(target=task).start()

    def load_image(self, path):
        """Load and display the image."""
        try:
            # Resize the image
            img = Image.open(path)
            img = img.resize((600, 450), Image.Resampling.LANCZOS)  # Resize to fit the layout
            photo = ImageTk.PhotoImage(img)

            # Update the label with the image
            self.image_label.config(image=photo, text="")  # Clear text
            self.image_label.image = photo  # Keep a reference to prevent garbage collection
        except FileNotFoundError:
            self.image_label.config(text="Image not found. Run the appropriate function first.")
        except Exception as e:
            self.image_label.config(text=f"Error: {e}")


# Start the event loop.
if __name__ == "__main__":
    window = Window()
    window.mainloop()
