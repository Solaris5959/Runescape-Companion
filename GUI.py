import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from NemiForest import NemiForestScript
from TravellingMerchant import TravellingMerchantScript

class RS3Helper(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("RS3Helper")
        self.geometry("1088x612")
        self.minsize(1088, 612)

        style = ttk.Style()
        style.theme_use('aqua')

        self.main_viewport = MainViewport(self)
        self.checklist_viewport = ChecklistViewport(self)

        # Create the PageSelectFrame with buttons to control the MainViewport
        self.page_select_frame = PageSelectFrame(self,
                                                 self.main_viewport.nemi_forest,
                                                 self.main_viewport.travelling_merchant,
                                                 self.main_viewport.shop_runs,
                                                 self.main_viewport.penguin_tracker,
                                                 self.checklist_viewport.daily,
                                                 self.checklist_viewport.weekly,
                                                 self.checklist_viewport.monthly)

        # Initially hide all frames in the MainViewport
        self.page_select_frame.show_nemi_forest()
        self.page_select_frame.show_daily()

        self.mainloop()

class MainViewport(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Set the size and position of the main viewport
        self.place(x=0, y=0, relwidth=0.625, relheight=0.9)

        # Create the frames to be toggled
        self.nemi_forest = NemiForest(self)
        self.travelling_merchant = TravellingMerchant(self)
        self.shop_runs = ShopRuns(self)
        self.penguin_tracker = PenguinTracker(self)

        # Initially hide all frames
        self.hide_all_frames()

    def hide_all_frames(self):
        """Hide all frames."""
        for child in self.winfo_children():
            child.place_forget()

    def show_frame(self, frame):
        """Show a specific frame."""
        self.hide_all_frames()
        frame.place(x=0, y=0, relwidth=1, relheight=1)

class ChecklistViewport(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Set the size and position of the checklist viewport
        self.place(relx=0.625, rely=0.1, relwidth=0.375, relheight=0.9)

        # Create the frames to be toggled
        self.daily = Daily(self)
        self.weekly = Weekly(self)
        self.monthly = Monthly(self)

        # Initially hide all frames
        self.hide_all_frames()

    def hide_all_frames(self):
        """Hide all frames."""
        for child in self.winfo_children():
            child.place_forget()

    def show_frame(self, frame):
        """Show a specific frame."""
        self.hide_all_frames()
        frame.place(x=0, y=0, relwidth=1, relheight=1)


class NemiForest(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        try:
            date = NemiForestScript()
            self.map_image = load_image("data/nemi_map.png", (572, 433))
            ttk.Label(self, image=self.map_image, anchor="center").place(x=0, rely=0.05, relwidth=1, relheight=0.9)
            ttk.Label(self, text=f"Last updated: {date}", font=("Arial", 20, "bold")).place(relx=0.1, rely=0.85, relwidth=0.9, relheight=0.1)
        except Exception as e:
            ttk.Label(self, text=f"Error: {e}", justify="center").place(x=0, y=0, relwidth=1, relheight=1)

class TravellingMerchant(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        try:
            TravellingMerchantScript()
            self.stock_image = load_image("data/merchant_stock.png", (572, 433))
            ttk.Label(self, image=self.stock_image, anchor="center").place(x=0, rely=0.05, relwidth=1, relheight=0.9)
        except Exception as e:
            ttk.Label(self, text=f"Error: {e}").place(x=0, y=0, relwidth=1, relheight=1)

class ShopRuns(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        ttk.Label(self, text="Recommended Shop Runs", font=("Arial", 16, "bold")).pack(pady=10)

        # Add some realistic RS3 shop information
        shop_data = [
            ("Shop Name", "Location", "Recommended Items"),
            ("Lowe's Archery Emporium", "Varrock", "Bronze arrows, Shortbow"),
            ("Zaff's Superior Staffs!", "Varrock", "Battle staffs"),
            ("Aubury's Rune Shop", "Varrock", "Air runes, Earth runes"),
            ("Wydin's Food Store", "Port Sarim", "Chocolate bars, Pot of flour"),
            ("Herquin's Gems", "Falador", "Uncut gems"),
        ]

        # Create a table-like display
        for shop in shop_data:
            ttk.Label(self, text=f"{shop[0]:<20} | {shop[1]:<15} | {shop[2]}").pack(anchor="w", padx=10)

        ttk.Label(self, text="Tip: Focus on shops with limited stock to maximize profit margins!", font=("Arial", 12, "italic")).pack(pady=10)

class PenguinTracker(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        ttk.Label(self, text="Penguin Hide and Seek Tracker", font=("Arial", 16, "bold")).pack(pady=10)

        # Placeholder for penguin tracking info
        ttk.Label(self, text="This widget will display penguin locations and hints for the current week.", wraplength=500, justify="center").pack(pady=20)

        ttk.Label(self, text="Penguins Spotted:", font=("Arial", 14)).pack(pady=10)
        ttk.Label(self, text="1. Draynor Village - Near the market", font=("Arial", 12)).pack(anchor="w", padx=20)
        ttk.Label(self, text="2. Ardougne - Hiding in the zoo", font=("Arial", 12)).pack(anchor="w", padx=20)
        ttk.Label(self, text="3. Taverley - Near the crystal chest", font=("Arial", 12)).pack(anchor="w", padx=20)

        ttk.Label(self, text="Tip: Use the Penguin Spy Device to locate penguins more efficiently!", font=("Arial", 12, "italic")).pack(pady=10)


class Daily(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        ttk.Label(self, text="Daily Activities", font=("Arial", 16, "bold")).pack(pady=10, anchor="w")

        daily_activities = [
            "Visit Guthixian Caches for Divination experience.",
            "Claim daily Wicked Hood runes and teleport charges.",
            "Complete Warbands for bonus experience and supplies.",
            "Harvest Player-Owned Farm animals.",
            "Check and replenish Anachronia Base Camp resources.",
            "Claim the daily reward from the Traveling Merchant (if available).",
            "Complete the Motherlode Maw roll (if eligible).",
            "Collect Daily Challenges rewards.",
            "Buy Battlestaves from Zaff in Varrock.",
            "Purchase limited stock items from shops (e.g., chocolate bars, feathers).",
            "Collect runes from Magic shops (Aubury, Betty, etc.).",
            "Claim daily Treasure Hunter keys.",
        ]

        for activity in daily_activities:
            var = tk.BooleanVar()
            tk.Checkbutton(self, text=activity, variable=var, font=("Arial", 12), anchor="w", justify="left").pack(fill="x", padx=10, pady=2)


class Weekly(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        ttk.Label(self, text="Weekly Activities", font=("Arial", 16, "bold")).pack(pady=10, anchor="w")

        weekly_activities = [
            "Complete the Troll Invasion D&D for bonus experience.",
            "Participate in Penguin Hide and Seek for points.",
            "Claim rewards from the Circus for performance skill experience.",
            "Collect resources from Managing Miscellania.",
            "Complete the Tears of Guthix minigame for experience in your lowest skill.",
            "Do the Big Chinchompa D&D for Hunter experience.",
            "Fight the Skeletal Horror for Slayer experience.",
            "Complete the Agoroth boss fight for Slayer experience.",
            "Check Anachronia's Totem of Treasure for a weekly roll.",
            "Harvest the Giant Oyster for clue scroll rewards.",
            "Complete Player-Owned Slayer Dungeon tasks.",
        ]

        for activity in weekly_activities:
            var = tk.BooleanVar()
            tk.Checkbutton(self, text=activity, variable=var, font=("Arial", 12), anchor="w", justify="left").pack(fill="x", padx=10, pady=2)


class Monthly(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        ttk.Label(self, text="Monthly Activities", font=("Arial", 16, "bold")).pack(pady=10, anchor="w")

        monthly_activities = [
            "Complete the God Statues D&D (Prayer XP).",
            "Participate in the Troll Invasion (Combat).",
            "Check the Giant Oyster for Clue Scroll rewards.",
            "Use your Monthly D&D token (Effigy Incubator > Oyster > Troll Invasion > Statues).",
            "Claim your Premier Club reward (if eligible).",
        ]

        for activity in monthly_activities:
            var = tk.BooleanVar()
            tk.Checkbutton(self, text=activity, variable=var, font=("Arial", 12), anchor="w", justify="left").pack(fill="x", padx=10, pady=2)

class PageSelectFrame(ttk.Frame):
    def __init__(self, parent, nemi_forest, travelling_merchant, shop_runs, penguin_tracker, daily, weekly, monthly):
        super().__init__(parent)

        self.nemi_forest = nemi_forest
        self.travelling_merchant = travelling_merchant
        self.shop_runs = shop_runs
        self.penguin_tracker = penguin_tracker

        self.daily = daily
        self.weekly = weekly
        self.monthly = monthly

        # Buttons for MainViewport
        ttk.Button(self, text="Nemi Forest", command=lambda: nemi_forest.master.show_frame(nemi_forest)).place(relx=0, rely=0.25, relwidth=0.123, relheight=0.9)
        ttk.Button(self, text="Travelling Merchant", command=lambda: travelling_merchant.master.show_frame(travelling_merchant)).place(relx=0.125, rely=0.25, relwidth=0.123, relheight=0.9)
        ttk.Button(self, text="Shop Runs", command=lambda: shop_runs.master.show_frame(shop_runs)).place(relx=0.25, rely=0.25, relwidth=0.123, relheight=0.9)
        ttk.Button(self, text="Penguins", command=lambda: penguin_tracker.master.show_frame(penguin_tracker)).place(relx=0.375, rely=0.25, relwidth=0.123, relheight=0.9)

        # Buttons for ChecklistViewport
        ttk.Button(self, text="Daily", command=lambda: daily.master.show_frame(daily)).place(relx=0.625, rely=0.25, relwidth=0.123, relheight=0.9)
        ttk.Button(self, text="Weekly", command=lambda: weekly.master.show_frame(weekly)).place(relx=0.75, rely=0.25, relwidth=0.123, relheight=0.9)
        ttk.Button(self, text="Monthly", command=lambda: monthly.master.show_frame(monthly)).place(relx=0.875, rely=0.25, relwidth=0.123, relheight=0.9)

        self.place(x=0, y=0, relwidth=1, relheight=0.1)


    def hide_all_main_frames(self):
        """Hide all frames."""
        self.nemi_forest.place_forget()
        self.travelling_merchant.place_forget()
        self.shop_runs.place_forget()
        self.penguin_tracker.place_forget()

    def show_nemi_forest(self):
        """Show Nemi Forest frame."""
        self.hide_all_main_frames()
        self.nemi_forest.place(x=0, y=0, relwidth=0.625, relheight=1)

    def show_travelling_merchant(self):
        """Show Travelling Merchant frame."""
        self.hide_all_main_frames()
        self.travelling_merchant.place(x=0, y=0, relwidth=0.625, relheight=1)

    def show_shop_runs(self):
        """Show Shop Runs frame."""
        self.hide_all_main_frames()
        self.shop_runs.place(x=0, y=0, relwidth=0.625, relheight=1)

    def show_penguin_tracker(self):
        """Show Penguin Tracker frame."""
        self.hide_all_main_frames()
        self.penguin_tracker.place(x=0, y=0, relwidth=0.625, relheight=1)

    def hide_all_checklist_frames(self):
        """Hide all checklist frames."""
        self.daily.place_forget()
        self.weekly.place_forget()
        self.monthly.place_forget()

    def show_daily(self):
        """Show Daily checklist."""
        self.hide_all_checklist_frames()
        self.daily.place(relx=0, y=0, relwidth=1, relheight=1)

    def show_weekly(self):
        """Show Weekly checklist."""
        self.hide_all_checklist_frames()
        self.weekly.place(relx=0, y=0, relwidth=1, relheight=1)

    def show_monthly(self):
        """Show Monthly checklist."""
        self.hide_all_checklist_frames()
        self.monthly.place(relx=0, y=0, relwidth=1, relheight=1)

def load_image(path, size):
    """Load and resize an image."""
    image = Image.open(path)
    image = image.resize(size)
    return ImageTk.PhotoImage(image)