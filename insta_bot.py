import time
import json
import os
from instagrapi import Client

# --------- LOGIN INFO ---------
USERNAME = "qtbaby96"
PASSWORD = "rudra123"

# --------- MESSAGE TO SEND ---------
REPLY_TEMPLATE = " oiii chamar @{username}! wapasss masssage kiya toh lynx kii maa sach me shod dunga."

# --------- FILES ---------
SEEN_FILE = "seen.json"
SESSION_FILE = "session.json"

# --------- INIT CLIENT ---------
cl = Client()

# Set device like a real Android phone
cl.set_locale('en_US')
cl.set_device({
    "manufacturer": "Samsung",
    "model": "Galaxy S21",
    "android_version": 30,
    "android_release": "11.0"
})

# Try loading saved session to avoid repeat login
if os.path.exists(SESSION_FILE):
    try:
        cl.load_settings(SESSION_FILE)
        cl.login(USERNAME, PASSWORD)
        print("✅ Logged in using saved session.")
    except Exception as e:
        print(f"⚠️ Session failed: {e}")
        cl.login(USERNAME, PASSWORD)
        cl.dump_settings(SESSION_FILE)
        print("✅ Fresh login and session saved.")
else:
    cl.login(USERNAME, PASSWORD)
    cl.dump_settings(SESSION_FILE)
    print("✅ Logged in and session saved.")

# --------- LOAD SEEN MESSAGES ---------
try:
    with open(SEEN_FILE, "r") as f:
        seen_messages = set(json.load(f))
except:
    seen_messages = set()

# --------- MAIN LOOP ---------
while True:
    try:
        print("🔁 Checking group chats...")
        threads = cl.direct_threads(amount=10)

        for thread in threads:
            if len(thread.users) > 1:  # Only group chats
                messages = cl.direct_messages(thread.id, amount=30)

                for message in reversed(messages):
                    if message.id in seen_messages or message.user_id == cl.user_id:
                        continue

                    user = cl.user_info_by_user_id(message.user_id)
                    reply = REPLY_TEMPLATE.format(username=user.username)

                    cl.direct_send(reply, thread_ids=[thread.id])
                    print(f"✅ Replied to @{user.username}: {message.text}")

                    seen_messages.add(message.id)
                    with open(SEEN_FILE, "w") as f:
                        json.dump(list(seen_messages), f)

                    time.sleep(5)  # small delay per message

    except Exception as e:
        print(f"⚠️ Error: {e}")

    time.sleep(20)  # delay before checking again
