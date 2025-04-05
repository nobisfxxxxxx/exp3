# save_session.py

from instagrapi import Client
import json

USERNAME = "rdp_hu_kidde"
PASSWORD = "nobihuiyar@1"

cl = Client()
cl.login(USERNAME, PASSWORD)

# Save session after successful login
cl.dump_settings("session.json")
print("✅ Session saved to session.json")
