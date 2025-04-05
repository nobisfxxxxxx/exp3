from instagrapi import Client

cl = Client()

# 🔒 Replace with new IG credentials
username = "qtbaby96"
password = "rudra123"

try:
    cl.login(username, password)
    cl.dump_settings("session.json")  # Save session
    print("✅ Session saved to session.json")
except Exception as e:
    print("❌ Error:", e)
