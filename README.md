# MPD VERIFICATION

A transparent OAuth2 verification tool for Discord and Roblox. Perfect for access management and member verification in gaming communities, roleplay projects, and faction groups.

## 🚀 Features
* **Discord OAuth2:** Secure retrieval of basic profile information (ID, Username) and the user's server list (Guilds).
* **Roblox OAuth2:** OpenID Connect integration to verify Roblox account ownership (retrieves ID, username, and public profile link).
* **Webhook Logging:** Instant delivery of authorization results directly to a private Discord channel via Webhook (data is not stored on the server).
* **Transparency:** The user sees all transmitted information directly on the successful authorization screen.

## 🛠 Installation and Setup
1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`
3. Set the Environment Variables:
   * `CLIENT_ID`, `CLIENT_SECRET`, `REDIRECT_URI` (for Discord)
   * `ROBLOX_CLIENT_ID`, `ROBLOX_CLIENT_SECRET`, `ROBLOX_REDIRECT_URI` (for Roblox)
   * `DISCORD_WEBHOOK_URL` (for receiving logs)
4. Run the application: `python app.py` (or use Gunicorn for cloud hosting).
