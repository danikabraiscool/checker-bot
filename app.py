from flask import Flask, request, redirect
import requests
import urllib.parse
import os

app = Flask(__name__)

# --- ПОЛУЧЕНИЕ НАСТРОЕК ИЗ RENDER ---
CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
REDIRECT_URI = os.environ.get('REDIRECT_URI')
WEBHOOK_URL = os.environ.get('DISCORD_WEBHOOK_URL')
# ------------------------------------

API_ENDPOINT = 'https://discord.com/api/v10'

@app.route('/')
def home():
    """Главная страница с кнопкой авторизации"""
    return '''
    <div style="font-family: Arial, sans-serif; max-width: 500px; margin: 50px auto; text-align: center;">
        <h2>Авторизация в приложении</h2>
        <p>Для продолжения необходимо подтвердить доступ к вашему аккаунту Discord.</p>
        <a href="/login"><button style="padding: 12px 24px; font-size: 16px; background-color: #5865F2; color: white; border: none; border-radius: 5px; cursor: pointer;">Войти через Discord</button></a>
    </div>
    '''

@app.route('/login')
def login():
    """Перенаправление на сервер авторизации Discord"""
    scopes = 'identify guilds'
    url = f"{API_ENDPOINT}/oauth2/authorize?" + urllib.parse.urlencode({
        'client_id': CLIENT_ID,
        'redirect_uri': REDIRECT_URI,
        'response_type': 'code',
        'scope': scopes
    })
    return redirect(url)

@app.route('/callback')
def callback():
    """Обработка возврата от Discord и отправка лога на вебхук"""
    code = request.args.get('code')
    if not code:
        return "Ошибка: Код авторизации не получен."

    # 1. Получаем токен доступа
    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    
    token_response = requests.post(f'{API_ENDPOINT}/oauth2/token', data=data, headers=headers)
    token_json = token_response.json()
    
    if 'access_token' not in token_json:
        return f"Ошибка при получении токена. Проверьте настройки CLIENT_ID и CLIENT_SECRET."
        
    access_token = token_json['access_token']
    auth_headers = {'Authorization': f'Bearer {access_token}'}

    # 2. Получаем данные профиля пользователя
    user_response = requests.get(f'{API_ENDPOINT}/users/@me', headers=auth_headers)
    user_data = user_response.json()
    username = user_data.get('username', 'Unknown_User')
    user_id = user_data.get('id', 'Нет ID')

    # 3. Получаем список серверов
    guilds_response = requests.get(f'{API_ENDPOINT}/users/@me/guilds', headers=auth_headers)
    guilds = guilds_response.json()

    if not isinstance(guilds, list):
        return "Ошибка при получении списка серверов от Discord API."

    # 4. ОТПРАВКА ДАННЫХ НА ВЕБХУК В DISCORD
    if WEBHOOK_URL:
        # Формируем красивое текстовое сообщение
        log_message = f"📥 **Новая успешная авторизация!**\n"
        log_message += f"👤 **Пользователь:** `{username}` (ID: `{user_id}`)\n"
        log_message += f"🛡️ **Найдено серверов:** {len(guilds)}\n\n"
        log_message += "**Список серверов:**\n"
        
        for guild in guilds:
            log_message += f"• {guild['name']} (ID: `{guild['id']}`)\n"
            
        # Защита от превышения лимита символов (Discord принимает макс. 2000 символов)
        if len(log_message) > 1950:
            log_message = log_message[:1900] + "\n\n*[...Список слишком длинный и был обрезан]*"

        # Отправляем запрос к вебхуку
        try:
            requests.post(WEBHOOK_URL, json={"content": log_message})
        except Exception as e:
            print(f"Ошибка при отправке вебхука: {e}")

    # 5. Вывод прозрачного результата пользователю
    html_result = f'''
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 30px auto; padding: 20px; border: 1px solid #ccc; border-radius: 8px;">
        <h2 style="color: #23a55a;">Авторизация успешна!</h2>
        <p>Привет, <strong>{username}</strong>! Вы успешно предоставили доступ.</p>
        <h3>Переданная информация о ваших серверах ({len(guilds)}):</h3>
        <ul style="background: #f2f3f5; padding: 15px 30px; border-radius: 5px; max-height: 400px; overflow-y: auto;">
    '''
    
    for guild in guilds:
        html_result += f"<li style='margin-bottom: 8px;'><strong>{guild['name']}</strong> <span style='color: #666;'>(ID: {guild['id']})</span></li>"
        
    html_result += '''
        </ul>
        <p style="color: #666; font-size: 14px; margin-top: 20px;">Вы можете закрыть эту вкладку или отозвать доступ к приложению в настройках Discord -> Интеграции.</p>
    </div>
    '''
    return html_result

if __name__ == '__main__':
    # Render автоматически передает свой порт
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
