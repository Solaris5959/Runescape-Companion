from config import KEY, CLIENT, USER_AGENT
from datetime import datetime, timezone
import praw, requests, re

# ------------------- Initialize Requests -------------------
reddit = praw.Reddit(
    client_id=CLIENT,
    client_secret=KEY,
    user_agent = USER_AGENT,
)

subreddit_name = "NemiForest"
subreddit = reddit.subreddit(subreddit_name)

# ---------------- Get Most Recent Map Post -----------------

recent_posts = subreddit.new(limit=3)

# Matches pattern: W[world num] [num]/[num][anything], i.e. "W82 10/9 *Extra flower not mapped*""
post_title_regex = r"^W.* .*/.*"

for post in recent_posts:
    if re.match(post_title_regex, post.title):
        daily_nemi_post = post # Get first post with matching title
        break

# --- Save Image (Nemi Forest Map) to "data/nemi_map.jpg" ---
# Get the Unix timestamp for the daily reset (midnight UTC)
daily_reset_utc = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0).timestamp()

# Check creation date to be Today
if (daily_nemi_post.created >= daily_reset_utc):
    # Check for image existing in post
    if hasattr(daily_nemi_post, "url") and daily_nemi_post.url.endswith((".jpg", ".png")):
        image_url = daily_nemi_post.url

        # Download the map (.png usually)
        response = requests.get(image_url)
        if response.status_code == 200:
            with open("data/nemi_map.png", "wb") as file:
                file.write(response.content)
            print("Nemi Forest Map Saved")
    else:
        print("No image found")
else:
    print("Today's Nemi Forest Map has not been posted")