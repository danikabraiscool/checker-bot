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
        <p>The application provides a secure mechanism to transfer your profile data (Discord/Roblox) to community administrators for verification purposes. You voluntarily grant access to the requested data by clicking the "
