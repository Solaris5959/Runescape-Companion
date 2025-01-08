import atexit
import os
from GUI import RS3Helper

# Function to delete the images when the program exits
def delete_images():
    delete_image("data/nemi_map.png")
    delete_image("data/merchant_stock.png")
    print("Images deleted.")

def delete_image(path):
    try:
        os.remove(path)
        print(f"{path} deleted successfully.")
    except FileNotFoundError as e:
        print(f"{e}: Couldn't locate {path}")

# Register the delete_images function to run when the program exits
atexit.register(delete_images)

# Start the event loop.
if __name__ == "__main__":
    RS3Helper()