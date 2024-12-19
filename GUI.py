from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import threading
from NemiForest import NemiForest
#from TravellingMerchant import TravellingMerchant  # Assuming this function exists


class Window(Tk):
    def __init__(self):
        super().__init__()
        s = ttk.Style()
        s.theme_names()
        s.theme_use('clam')

        # Configure window
        self.title("RS3Helper")
        self.geometry("1000x600")  # Increased resolution
        self.configure(bg="#091021")

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

        self.init_checklist()

        # Image frame
        self.image_frame = Frame(self, bg="#192134")
        self.image_frame.pack(side="left", fill="both", expand=True)

        # Dropdown menu for image selection
        self.image_options = ["NemiForest", "TravellingMerchant"]
        self.selected_image = StringVar(value=self.image_options[0])
        self.image_menu = OptionMenu(self.image_frame, self.selected_image, *self.image_options, command=self.refresh_image)
        self.image_menu.pack(side="top", anchor="nw", padx=5, pady=5)

        # Refresh button in the viewport
        refresh_icon = PhotoImage(file="data/refresh_icon.png")
        self.refresh_button = Button(
            self.image_frame,
            image=refresh_icon,
            command=self.refresh_image,
            bg="#192134",  # Ensure this matches the frame background
            activebackground="#192134",  # Ensure hover background matches as well
            relief="flat",  # Remove the 3D border
            borderwidth=0,  # Remove any border
            highlightthickness=0  # Remove focus outline
        )
        self.refresh_button.image = refresh_icon  # Keep a reference to prevent garbage collection
        self.refresh_button.pack(side="top", anchor="ne", padx=5, pady=5)


        # Placeholder for the image
        self.image_label = Label(self.image_frame, text="Image will appear here", bg="#192134")
        self.image_label.pack(expand=True)

        self.refresh_image()  # Load the initial image

    def init_checklist(self):
        checklist = [
            "Nemi Forest", "Travelling Merchant", "Daily Challenges", "Edgeville Slayer Shop",
            "Burthorpe Slayer Shop", "Vis Wax", "Rune Shops", "Reaper Task", "PoF", "Ports",
            "Ooglog Mining/Meat", "Prifddinas Mining", "Um Diary Supplies", "Bucket of Slime",
            "Soul Obelisk"
        ]

        # Checklist frame
        self.checklist_frame = Frame(self, bg="#343e57", width=250)
        self.checklist_frame.pack(side="right", fill="y")
        self.checklist_frame.pack_propagate(False)  # Prevent the frame from resizing to fit its contents

        # Checklist title
        self.checklist_title = Label(self.checklist_frame, text="Dailies", bg="#343e57", font=("Arial", 20, "bold"))
        self.checklist_title.pack(pady=10)

        # Checklist items
        self.checklist_vars = [IntVar() for _ in range(len(checklist))]
        self.checklist_items = checklist
        for i, item in enumerate(self.checklist_items):
            check = Checkbutton(self.checklist_frame, text=item, variable=self.checklist_vars[i], bg="#465375", width=25, anchor="w")
            check.pack(anchor="w", padx=10, pady=5)

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