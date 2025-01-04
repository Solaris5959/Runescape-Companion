import webview

def penguin_webview():
    # Create the webview window with a callback to handle closure
    webview.create_window('World60Pengs', 'https://jq.world60pengs.com', confirm_close=True)

    # Start the webview without blocking the main thread
    webview.start()