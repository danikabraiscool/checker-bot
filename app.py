from flask import Flask, request, redirect
import requests
import urllib.parse
import os

app = Flask(__name__)

# --- НАСТРОЙКИ ---
DISCORD_CLIENT_ID = os.environ.get('CLIENT_ID')
DISCORD_CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
DISCORD_REDIRECT_URI = os.environ.get('REDIRECT_URI')

ROBLOX_CLIENT_ID = os.environ.get('ROBLOX_CLIENT_ID')
ROBLOX_CLIENT_SECRET = os.environ.get('ROBLOX_CLIENT_SECRET')
ROBLOX_REDIRECT_URI = os.environ.get('ROBLOX_REDIRECT_URI')

WEBHOOK_URL = os.environ.get('DISCORD_WEBHOOK_URL')

DISCORD_API = 'https://discord.com/api/v10'
ROBLOX_AUTH_URL = 'https://apis.roblox.com/oauth/v1/authorize'
ROBLOX_TOKEN_URL = 'https://apis.roblox.com/oauth/v1/token'
ROBLOX_USERINFO_URL = 'https://apis.roblox.com/oauth/v1/userinfo'

# ==========================================
#               ГЛАВНАЯ СТРАНИЦА
# ==========================================

@app.route('/')
def home():
    """Главная страница с логотипами, кнопками и документами"""
    return '''
    <div style="font-family: Arial, sans-serif; max-width: 500px; margin: 50px auto; text-align: center;">
        
        <img src="https://raw.githubusercontent.com/danikabraiscool/checker-bot/main/MPDLOGO.png" alt="MPD Logo" style="width: 150px; height: auto; margin-bottom: 20px; border-radius: 15px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
        
        <h2>Авторизация в приложении</h2>
        <p>Выберите удобный способ подтверждения аккаунта:</p>
        
        <div style="margin-top: 30px; display: flex; flex-direction: column; gap: 15px; align-items: center;">
            <a href="/login_discord" style="text-decoration: none;">
                <button style="display: flex; align-items: center; justify-content: center; gap: 12px; padding: 12px 24px; width: 280px; font-size: 16px; font-weight: bold; background-color: #5865F2; color: white; border: none; border-radius: 8px; cursor: pointer; transition: 0.2s; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                    <img src="https://raw.githubusercontent.com/danikabraiscool/checker-bot/main/discord_logo.png" alt="Discord" style="width: 24px; height: 24px;">
                    Войти через Discord
                </button>
            </a>
            
            <a href="/login_roblox" style="text-decoration: none;">
                <button style="display: flex; align-items: center; justify-content: center; gap: 12px; padding: 12px 24px; width: 280px; font-size: 16px; font-weight: bold; background-color: #000000; color: white; border: none; border-radius: 8px; cursor: pointer; transition: 0.2s; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                    <img src="https://raw.githubusercontent.com/danikabraiscool/checker-bot/main/roblox_logo.png" alt="Roblox" style="width: 24px; height: 24px;">
                    Войти через Roblox
                </button>
            </a>
        </div>

        <div style="margin-top: 50px; padding-top: 20px; border-top: 1px solid #eee; font-size: 12px; color: #888;">
            <p style="margin-bottom: 10px;">Продолжая, вы соглашаетесь с правилами сервиса:</p>
            <div style="display: flex; justify-content: center; gap: 15px;">
                <a href="/terms" style="color: #5865F2; text-decoration: none;">Terms of Service</a>
                <span style="color: #ccc;">|</span>
                <a href="/privacy" style="color: #5865F2; text-decoration: none;">Privacy Policy</a>
            </div>
        </div>
        
    </div>
    '''

# ==========================================
#         СТРАНИЦЫ ДОКУМЕНТАЦИИ (НОВОЕ)
# ==========================================

@app.route('/terms')
def terms():
    """Страница Пользовательского соглашения"""
    return '''
    <div style="max-width: 800px; margin: 0 auto; padding: 30px 20px; font-family: Arial, sans-serif; color: #333; line-height: 1.6;">
        <div style="margin-bottom: 30px;">
            <a href="/" style="text-decoration: none; color: #333; font-weight: bold; display: inline-flex; align-items: center; gap: 8px; padding: 10px 18px; background: #f2f3f5; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
                <span style="font-size: 20px;">🏠</span> Back to Home
            </a>
        </div>
        
        <h1 style="border-bottom: 2px solid #5865F2; padding-bottom: 10px;">Terms of Service</h1>
        <p style="color: #666;"><strong>Last Updated:</strong> July 13, 2026</p>
        
        <p>By using the <strong>MPD VERIFICATION</strong> application for authorization, you automatically agree to these terms. If you do not agree with any of these terms, please do not use this application.</p>
        
        <h3 style="color: #222; margin-top: 25px;">1. Use of the Application</h3>
        <p>The application provides a secure mechanism to transfer your profile data (Discord/Roblox) to community administrators for verification purposes. You voluntarily grant access to the requested data by clicking the "Authorize" button on the official Discord and Roblox authorization pages.</p>
        
        <h3 style="color: #222; margin-top: 25px;">2. Disclaimer of Warranties</h3>
        <p>The application is provided on an "AS IS" basis. The developer is not responsible for any direct or indirect damages, platform malfunctions, or account suspensions resulting from the use of the application.</p>
        
        <h3 style="color: #222; margin-top: 25px;">3. Fair Use</h3>
        <p>It is strictly prohibited to use the application for:</p>
        <ul style="background: #f9f9f9; padding: 15px 35px; border-radius: 5px;">
            <li>Attempting to hack or bypass security systems.</li>
            <li>Automated spamming of requests (DDoS).</li>
        </ul>
        
        <h3 style="color: #222; margin-top: 25px;">4. Changes to the Terms</h3>
        <p>The developer reserves the right to modify these Terms at any time. Changes become effective immediately upon their publication on this platform.</p>
    </div>
    '''

@app.route('/privacy')
def privacy():
    """Страница Политики конфиденциальности"""
    return '''
    <div style="max-width: 800px; margin: 0 auto; padding: 30px 20px; font-family: Arial, sans-serif; color: #333; line-height: 1.6;">
        <div style="margin-bottom: 30px;">
            <a href="/" style="text-decoration: none; color: #333; font-weight: bold; display: inline-flex; align-items: center; gap: 8px; padding: 10px 18px; background: #f2f3f5; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
                <span style="font-size: 20px;">🏠</span> Back to Home
            </a>
        </div>
        
        <h1 style="border-bottom: 2px solid #5865F2; padding-bottom: 10px;">Privacy Policy</h1>
        <p style="color: #666;"><strong>Last Updated:</strong> July 13, 2026</p>
        
        <p>This Privacy Policy describes how the <strong>MPD VERIFICATION</strong> application collects, uses, and protects your information when you use our authorization services (OAuth2).</p>
        
        <h3 style="color: #222; margin-top: 25px;">1. Information We Collect</h3>
        <p>When you authorize through our application, we may request access to the following data:</p>
        <ul style="background: #f9f9f9; padding: 15px 35px; border-radius: 5px;">
            <li><strong>Discord:</strong> Basic profile information (Username, ID) and the list of servers (Guilds) you are a member of.</li>
            <li><strong>Roblox:</strong> Basic profile information (Username, Account ID, public profile link).</li>
        </ul>
        
        <h3 style="color: #222; margin-top: 25px;">2. How We Use Your Information</h3>
        <p>The collected data is used strictly for verifying your identity to grant access to closed communities or servers, and logging the successful completion of the verification process.</p>
        
        <h3 style="color: #222; margin-top: 25px;">3. Data Storage</h3>
        <p>We do <strong>not</strong> store your data in databases or local files permanently. The collected information is transmitted directly to the project administrator into a secure, private Discord channel via Webhook technology.</p>
        
        <h3 style="color: #222; margin-top: 25px;">4. Third-Party Sharing</h3>
        <p>We do not sell, trade, or transfer your personal information to outside companies or third parties.</p>
        
        <h3 style="color: #222; margin-top: 25px;">5. Your Control Over Data</h3>
        <p>You can revoke our application's access to your data at any time through your Discord (Integrations) or Roblox (App Permissions) settings.</p>
    </div>
    '''

# ==========================================
#               ЛОГИКА DISCORD
# ==========================================

@app.route('/login_discord')
def login_discord():
    scopes = 'identify guilds'
    url = f"{DISCORD_API}/oauth2/authorize?" + urllib.parse.urlencode({
        'client_id': DISCORD_CLIENT_ID,
        'redirect_uri': DISCORD_REDIRECT_URI,
        'response_type': 'code',
        'scope': scopes
    })
    return redirect(url)

@app.route('/callback')
def callback_discord():
    code = request.args.get('code')
    if not code: return "Ошибка: Код Discord не получен."

    data = {
        'client_id': DISCORD_CLIENT_ID,
        'client_secret': DISCORD_CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': DISCORD_REDIRECT_URI
    }
    
    token_resp = requests.post(f'{DISCORD_API}/oauth2/token', data=data, headers={'Content-Type': 'application/x-www-form-urlencoded'})
    token_json = token_resp.json()
    if 'access_token' not in token_json: return "Ошибка получения токена Discord."
        
    auth_headers = {'Authorization': f"Bearer {token_json['access_token']}"}

    user_data = requests.get(f'{DISCORD_API}/users/@me', headers=auth_headers).json()
    guilds = requests.get(f'{DISCORD_API}/users/@me/guilds', headers=auth_headers).json()

    username = user_data.get('username', 'Unknown')
    user_id = user_data.get('id', '0')
    avatar_hash = user_data.get('avatar')

    if avatar_hash:
        avatar_url = f"https://cdn.discordapp.com/avatars/{user_id}/{avatar_hash}.png"
    else:
        avatar_url = f"https://cdn.discordapp.com/embed/avatars/{(int(user_id) >> 22) % 6}.png"

    if WEBHOOK_URL:
        try:
            main_embed = {
                "title": "🔵 Новая Discord Авторизация!",
                "color": 5793266,
                "thumbnail": {"url": avatar_url},
                "fields": [
                    {"name": "Пользователь", "value": f"`{username}`", "inline": True},
                    {"name": "ID", "value": f"`{user_id}`", "inline": True},
                    {"name": "Всего серверов", "value": str(len(guilds)), "inline": True}
                ]
            }
            requests.post(WEBHOOK_URL, json={"embeds": [main_embed]})

            chunk_size = 25
            for i in range(0, len(guilds), chunk_size):
                chunk = guilds[i:i + chunk_size]
                desc = "\n".join([f"• {g['name']} (ID: `{g['id']}`)" for g in chunk])
                
                chunk_embed = {
                    "author": {"name": f"Продолжение списка: {username}"}, 
                    "title": f"🛡️ Часть {i//chunk_size + 1}",
                    "description": desc,
                    "color": 2829617
                }
                requests.post(WEBHOOK_URL, json={"embeds": [chunk_embed]})
        except Exception as e:
            print(f"Ошибка при отправке эмбедов: {e}")

    return f"<h2 style='text-align:center; font-family:Arial; margin-top:50px;'>Discord авторизация успешна, {username}! Можете закрыть вкладку.</h2>"

# ==========================================
#               ЛОГИКА ROBLOX
# ==========================================

@app.route('/login_roblox')
def login_roblox():
    url = f"{ROBLOX_AUTH_URL}?" + urllib.parse.urlencode({
        'client_id': ROBLOX_CLIENT_ID,
        'redirect_uri': ROBLOX_REDIRECT_URI,
        'response_type': 'code',
        'scope': 'openid profile',
    })
    return redirect(url)

@app.route('/callback_roblox')
def callback_roblox():
    code = request.args.get('code')
    if not code: return "Ошибка: Код Roblox не получен."

    data = {
        'client_id': ROBLOX_CLIENT_ID,
        'client_secret': ROBLOX_CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': ROBLOX_REDIRECT_URI
    }
    
    token_resp = requests.post(ROBLOX_TOKEN_URL, data=data, headers={'Content-Type': 'application/x-www-form-urlencoded'})
    token_json = token_resp.json()
    
    if 'access_token' not in token_json:
        return f"Ошибка получения токена Roblox."

    auth_headers = {'Authorization': f"Bearer {token_json['access_token']}"}
    
    user_resp = requests.get(ROBLOX_USERINFO_URL, headers=auth_headers)
    user_data = user_resp.json()
    
    roblox_id = user_data.get('sub', 'Unknown')
    roblox_name = user_data.get('preferred_username', 'Unknown')
    roblox_profile = user_data.get('profile', f'https://www.roblox.com/users/{roblox_id}/profile')
    roblox_avatar = user_data.get('picture', '') 

    if WEBHOOK_URL:
        roblox_embed = {
            "title": "🟥 Новая Roblox Авторизация!",
            "color": 16711680,
            "thumbnail": {"url": roblox_avatar} if roblox_avatar else {},
            "fields": [
                {"name": "Никнейм", "value": f"[{roblox_name}]({roblox_profile})", "inline": True},
                {"name": "ID", "value": f"`{roblox_id}`", "inline": True}
            ]
        }
        try:
            requests.post(WEBHOOK_URL, json={"embeds": [roblox_embed]})
        except Exception as e:
            print(f"Ошибка вебхука Roblox: {e}")

    return f"<h2 style='text-align:center; font-family:Arial; margin-top:50px;'>Roblox авторизация успешна, {roblox_name}! Можете закрыть вкладку.</h2>"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
