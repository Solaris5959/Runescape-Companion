import os
from tkinter import ttk
import customtkinter as ctk
import webbrowser
from PIL import Image
from NemiForest import nemiForestScript
from TravellingMerchant import travellingMerchantScript

class RS3Helper(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("RS3Helper")
        self.geometry("1088x612")
        self.minsize(1088, 612)

        # Set theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

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

class MainViewport(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        # Set the size and position of the main viewport
        self.place(x=0, rely=0.1, relwidth=0.625, relheight=0.9)

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
        frame.run_script()

class ChecklistViewport(ctk.CTkFrame):
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

class NemiForest(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        ctk.CTkLabel(self, text="Nemi Forest Map", font=("Arial", 16, "bold")).pack(pady=10)

        try:
            date = nemiForestScript()
            print(date)
            self.map_image = load_image("data/nemi_map.png", 0.55)
            ctk.CTkLabel(self, image=self.map_image, text="", anchor="center").place(x=0, rely=0.1, relwidth=1, relheight=0.8)
            ctk.CTkLabel(self, text=f"Last updated: {date}", font=("Arial", 20, "bold")).place(x=0, rely=0.9, relwidth=0.9, relheight=0.1)
        except Exception as e:
            ctk.CTkLabel(self, text=f"Error: {e}", justify="right", anchor="center").place(x=0, rely=0.1, relwidth=1, relheight=0.9)

    def run_script(self):
        pass

class TravellingMerchant(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        ctk.CTkLabel(self, text="Travelling Merchant's Shop", font=("Arial", 16, "bold")).pack(pady=10)

    def run_script(self):
        try:
            if not os.path.exists("data/merchant_stock.png"):
                travellingMerchantScript()
            self.stock_image = load_image("data/merchant_stock.png", 1.0)
            ctk.CTkLabel(self, image=self.stock_image, text="", anchor="n").place(x=0, rely=0.1, relwidth=1, relheight=0.8)
        except Exception as e:
            ctk.CTkLabel(self, text=f"Error: {e}", justify="center").place(x=0, y=0, relwidth=1, relheight=1)

class ShopRuns(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        ctk.CTkLabel(self, text="Recommended Shop Runs", font=("Arial", 16, "bold")).pack(pady=10)

        # First table: Shop information
        shop_data = [
            ("Shop Name", "Location", "Recommended Items"),
            ("Morvan's Slayer Equipment", "Prifddinas", "Enchanted gem pack, Insulated boots"),
            ("Turael/Spiria's Slayer Equipment", "Burthorpe", "Enchanted gem pack, Insulated boots"),
            ("Sophanem Slayer Supplies", "Sophanem", "Feather of Ma'at"),
            ("Fresh Meat", "Oo'glog", "Raw rabbit pack, Raw beef pack, Raw bird meat pack"),
        ]

        columns = ("shop_name", "location", "recommended_items")
        tree = ttk.Treeview(self, columns=columns, show="headings", height=5)
        tree.heading("shop_name", text="Shop Name")
        tree.heading("location", text="Location")
        tree.heading("recommended_items", text="Recommended Items")
        tree.column("shop_name", width=210)
        tree.column("location", width=110)
        tree.column("recommended_items", width=360)

        for shop in shop_data:
            tree.insert("", "end", values=shop)

        tree.pack(fill="x", padx=10, pady=10)

        # Second table: Steps with checkboxes
        ctk.CTkLabel(self, text="Basic Daily Run Steps", font=("Arial", 14, "bold")).pack(pady=10)

        steps_frame = ctk.CTkFrame(self)
        steps_frame.pack(fill="x", padx=10)

        # Define daily run steps
        daily_steps = [
            "Start in Prifddinas, mine the Crystal Sandstone in Ithell",
            "Visit Morvan's Slayer Equipment in Iowerth",
            "Teleport to Burthorpem visit Turael/Spiria's Slayer Equipment",
            "Teleport to Oo'glog, mine the Red Sandstone",
            "Buy raw meat packs from Chargurr across from the bank",
            "Teleport to Menaphos, cross the bridge and visit Sophanem Slayer Supplies",
            "Use the Wicked Hood teleport to the Runecrafting Guild, do daily Vis Wax"
        ]

        self.step_vars = []  # To store the BooleanVar for each step

        # Create a table-like layout for steps with checkboxes
        for step in daily_steps:
            var = ctk.BooleanVar()
            checkbox = ctk.CTkCheckBox(steps_frame, text=step, variable=var)
            checkbox.pack(anchor="w", pady=2)
            self.step_vars.append(var)

        # Optionally, add a button to mark all steps as completed
        ctk.CTkButton(self, text="Mark All as Completed", command=self.mark_all_completed).pack(pady=10)

    def mark_all_completed(self):
        for var in self.step_vars:
            var.set(True)

    def run_script(self):
        pass  # No script to run for ShopRuns

class PenguinTracker(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        ctk.CTkLabel(self, text="Penguin Hide and Seek Tracker", font=("Arial", 16, "bold")).pack(pady=10)

    def run_script(self):
        webbrowser.open("https://jq.world60pengs.com", new=1)

class Daily(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        ctk.CTkLabel(self, text="Daily Activities", font=("Arial", 16, "bold")).pack(padx=10, pady=10, anchor="w")

        # Create a frame to hold the scrollable content
        container = ctk.CTkFrame(self)
        container.pack(fill="both", expand=True, padx=10, pady=10)

        # Create a canvas and scrollbar
        canvas = ctk.CTkCanvas(container)
        scrollbar = ctk.CTkScrollbar(container, orientation="vertical", command=canvas.yview)
        scrollable_frame = ctk.CTkFrame(canvas)

        # Configure the canvas
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Pack the canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Add the activities with checkboxes
        daily_activities = sorted(list(set([
            "Play Wilderness Warbands",
            "Buy Port Resources from Black Marketeer",
            "Run Mazcab Supply run",
            "Play Fish Flingers.",
            "Mine Shooting Star.",
            "Enter Sinkholes.",
            "Kill 2 Evil Trees.",
            "Participate in Big Chinchompa 2 times.",
            "Play Guthixian Cache 2 times.",
            "Hand in 1k rune dust.",
            "Train at Serenity posts.",
            "Harvest Crystal tree blossoms.",
            "Collect from Divine locations.",
            "Use Jack of Trades aura.",
            "Assist players using Assist System.",
            "Complete Soul Reaper tasks.",
            "Slay or prune Jade vine.",
            "Kill Bork in Chaos Tunnels.",
            "Kill Phoenix in lair.",
            "Mine red sandstone.",
            "Mine crystal-flecked sandstone.",
            "Collect Gorajo card from Gorajo dungeon.",
            "Collect 8,000 Tokkul from TzHaar-Hur-Zuh.",
            "Train using Book of Char.",
            "Teleport 5 times to slime pit.",
            "Buy items from shops.",
            "Collect flax from Geoffrey.",
            "Get sand from Bert in Yanille.",
            "Collect pure essence from Wizard Cromperty.",
            "Daily bag of lost items from Rug Merchants.",
            "Use Explorer’s ring to cast alchemy.",
            "Turn soda ash into molten glass.",
            "Operate Rune Goldberg Machine.",
            "Utilize Wicked hood.",
            "Convert bones into bonemeal and slime.",
            "Collect food hamper from Lumbridge Castle.",
            "Collect item from Motherlode Maw.",
            "Exchange crystal shards with Wythien.",
            "Collect soft clay from artisan’s bandana.",
            "Collect spirit shards from shaman’s headdress.",
            "Collect coal from blacksmith’s helmet.",
            "Collect vials of water from botanist’s mask.",
            "Collect nests from farmer’s hat.",
            "Collect dragon bones from first age tiara.",
            "Collect pie shells from sous chef’s toque.",
            "Collect chronicle fragments from diviner’s headwear.",
            "Collect from PoH Aquarium Decorations.",
            "Free logs from Coeden.",
            "Do tasks assigned by Trinks.",
            "Do Nemi Forest activities.",
            "Gain reputation from Soul obelisks.",
            "Collect supplies from Rosie.",
            "Complete Arc contracts.",
            "Deplete resources on Uncharted Isles.",
            "Heart of Gielinor bounty.",
            "Use Treasure Hunter keys.",
            "Collect free Necromancy supplies from Lupe."
        ])))


        for activity in daily_activities:
            var = ctk.BooleanVar()
            ctk.CTkCheckBox(
                scrollable_frame,
                text=activity,
                variable=var,
                font=("Arial", 12)
            ).pack(fill="x", padx=10, pady=2)


    def run_script(self):
        pass  # No script to run for Daily

class Weekly(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        ctk.CTkLabel(self, text="Weekly Activities", font=("Arial", 16, "bold")).pack(padx=10, pady=10, anchor="w")

        # Create a frame to hold the scrollable content
        container = ctk.CTkFrame(self)
        container.pack(fill="both", expand=True, padx=10, pady=10)

        # Create a canvas and scrollbar
        canvas = ctk.CTkCanvas(container)
        scrollbar = ctk.CTkScrollbar(container, orientation="vertical", command=canvas.yview)
        scrollable_frame = ctk.CTkFrame(canvas)

        # Configure the canvas
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Pack the canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Add the activities with checkboxes
        weekly_activities = sorted(list(set([
            "Activate Anachronia Totems for Divination XP and totem benefits.",
            "Cap at the Clan Citadel for XP and resources.",
            "Claim raw bacon or Pig Familiar Pouches from Eli Bacon.",
            "Claim the Weekly Key from Shooting Star, Evil Tree, or Farming.",
            "Clean out the Water Filtration System in Het's Oasis.",
            "Collect from Aquarium Decorations for clue scrolls and planks.",
            "Collect resources from Managing Miscellania & cap Favour.",
            "Complete Player-Owned Slayer Dungeon tasks.",
            "Complete the Agoroth boss fight for Bonus experience.",
            "Complete the Circus D&D for performance experience.",
            "Complete the Familiarisation D&D for Summoning Charm boosts.",
            "Complete the Herby Werby D&D for Herblore experience.",
            "Complete the Tears of Guthix D&D for XP in your lowest skill.",
            "Complete the Wisps of the Grove D&D for Farming & Hunter XP.",
            "Follow up on A Barmaid's Tip at Player-Owned Ports (Thursday).",
            "Help Meg for experience lamps and coins.",
            "Kill Skeletal horror for Slayer and Prayer experience.",
            "Participate in Penguin Hide and Seek for points.",
            "Play Balthazar Beauregard's Circus for performance XP.",
            "Play Rush of Blood for Slayer rewards.",
            "Play Shattered Worlds challenge mode for shattered anima.",
            "Purchase stock from Thalmund (Wednesday Only).",
            "Refight defeated champions for Slayer XP and Constitution XP.",
            "Replay Broken Home for a large or huge prismatic lamp.",
            "Replay Dimension of Disaster for XP lamps and silver pennies.",
            "Replay Memory of Nomad for Constitution and Slayer XP.",
            "Replay Sliske's Endgame for a medium prismatic lamp."
        ])))

        for activity in weekly_activities:
            var = ctk.BooleanVar()
            ctk.CTkCheckBox(
                scrollable_frame,
                text=activity,
                variable=var,
                font=("Arial", 12)
            ).pack(fill="x", padx=10, pady=2)

    def run_script(self):
        pass  # No script to run for Weekly

class Monthly(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        ctk.CTkLabel(self, text="Monthly Activities", font=("Arial", 16, "bold")).pack(padx=10, pady=10, anchor="w")

        container = ctk.CTkFrame(self)
        container.pack(fill="both", expand=True, padx=10, pady=10)

        # Create a canvas and scrollbar
        canvas = ctk.CTkCanvas(container)
        scrollbar = ctk.CTkScrollbar(container, orientation="vertical", command=canvas.yview)
        scrollable_frame = ctk.CTkFrame(canvas)

        # Configure the canvas
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Pack the canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        monthly_activities = [
            "Complete the God Statues D&D (Choose Prayer XP).",
            "Participate in the Troll Invasion (Choose Combat Mode).",
            "Check the Giant Oyster for Clue Scroll rewards.",
            "Use your Monthly D&D token (Effigy Incubator > Oyster).",
            "Complete the Effigy Incubator D&D",
            "Claim your Premier Club reward (if eligible).",
        ]

        for activity in monthly_activities:
            var = ctk.BooleanVar()
            ctk.CTkCheckBox(
                scrollable_frame,
                text=activity,
                variable=var,
                font=("Arial", 12)
            ).pack(fill="x", padx=10, pady=2)

    def run_script(self):
        pass  # No script to run for Monthly

class PageSelectFrame(ctk.CTkFrame):
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
        ctk.CTkButton(self, text="Nemi Forest", command=lambda: nemi_forest.master.show_frame(nemi_forest)).place(relx=0, rely=0.25, relwidth=0.123, relheight=0.9)
        ctk.CTkButton(self, text="Travelling Merchant", command=lambda: travelling_merchant.master.show_frame(travelling_merchant)).place(relx=0.125, rely=0.25, relwidth=0.123, relheight=0.9)
        ctk.CTkButton(self, text="Shop Runs", command=lambda: shop_runs.master.show_frame(shop_runs)).place(relx=0.25, rely=0.25, relwidth=0.123, relheight=0.9)
        ctk.CTkButton(self, text="Penguins", command=lambda: penguin_tracker.master.show_frame(penguin_tracker)).place(relx=0.375, rely=0.25, relwidth=0.123, relheight=0.9)

        # Buttons for ChecklistViewport
        ctk.CTkButton(self, text="Daily", command=lambda: daily.master.show_frame(daily)).place(relx=0.625, rely=0.25, relwidth=0.123, relheight=0.9)
        ctk.CTkButton(self, text="Weekly", command=lambda: weekly.master.show_frame(weekly)).place(relx=0.75, rely=0.25, relwidth=0.123, relheight=0.9)
        ctk.CTkButton(self, text="Monthly", command=lambda: monthly.master.show_frame(monthly)).place(relx=0.875, rely=0.25, relwidth=0.123, relheight=0.9)

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

def load_image(path, multiplier):
    """Load and resize an image."""
    image = Image.open(path)

    image = image.resize(tuple(int(multiplier * x) for x in image.size)) # Convert to int before creating tuple
    return ctk.CTkImage(image, size=image.size)