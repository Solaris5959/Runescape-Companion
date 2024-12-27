import atexit
import os
from GUI import RS3Helper

# Function to delete the images when the program exits
def delete_images():
    try:
        os.remove("data/nemi_map.png")
        os.remove("data/merchant_stock.png")
        print("Images deleted successfully.")
    except FileNotFoundError:
        print("No images found to delete.")

# Register the delete_images function to run when the program exits
atexit.register(delete_images)

# Start the event loop.
if __name__ == "__main__":
    RS3Helper()
