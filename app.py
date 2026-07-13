from flask import Flask, request, redirect
import requests
import urllib.parse
import os

app = Flask(__name__)

# --- ВАШИ ДАННЫЕ ИЗ DISCORD DEVELOPER PORTAL ---
CLIENT_ID = 'YOUR_CLIENT_ID'          # Вставь свой ID
CLIENT_SECRET = 'YOUR_CLIENT_SECRET'  # Вставь свой Secret
# Эту ссылку мы поменяем на ту, которую выдаст Render + /callback
REDIRECT_URI = 'https://tvoy-sayt.onrender.com/callback'
# -----------------------------------------------

API_ENDPOINT = 'https://discord.com/api/v10'

@app.route('/')
def home():
    return '''
    <div style="font-family: Arial, sans-serif; max-width: 500px; margin: 50px auto; text-align: center;">
        <h2>Авторизация в приложении</h2>
        <p>Для продолжения необходимо подтвердить доступ к вашему аккаунту Discord.</p>
        <a href="/login"><button style="padding: 12px 24px; font-size: 16px; background-color: #5865F2; color: white; border: none; border-radius: 5px; cursor: pointer;">Войти через Discord</button></a>
    </div>
    '''

@app.route('/login')
def login():
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
    code = request.args.get('code')
    if not code:
        return "Ошибка: Код авторизации не получен."

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
        return f"Ошибка при получении токена: {token_json}"
        
    access_token = token_json['access_token']
    auth_headers = {'Authorization': f'Bearer {access_token}'}

    user_response = requests.get(f'{API_ENDPOINT}/users/@me', headers=auth_headers)
    user_data = user_response.json()
    username = user_data.get('username', 'Unknown_User')
    user_id = user_data.get('id', '0000000000000000')

    guilds_response = requests.get(f'{API_ENDPOINT}/users/@me/guilds', headers=auth_headers)
    guilds = guilds_response.json()

    if not isinstance(guilds, list):
        return "Ошибка при получении списка серверов."

    # Сохраняем в локальный файл на сервере Render
    try:
        with open('authorized_servers.txt', 'a', encoding='utf-8') as file:
            file.write(f"Пользователь: {username} (ID: {user_id})\n")
            file.write("Список серверов:\n")
            for guild in guilds:
                file.write(f"  - {guild['name']} (ID: {guild['id']})\n")
            file.write("\n" + "="*50 + "\n\n")
    except Exception as e:
        print(f"Ошибка записи в файл: {e}")

    html_result = f'''
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 30px auto; padding: 20px; border: 1px solid #ccc; border-radius: 8px;">
        <h2 style="color: #23a55a;">Авторизация успешна!</h2>
        <p>Привет, <strong>{username}</strong>. Вы успешно предоставили доступ к приложению.</p>
        <h3>Переданная информация о ваших серверах ({len(guilds)}):</h3>
        <ul style="background: #f2f3f5; padding: 15px 30px; border-radius: 5px; max-height: 400px; overflow-y: auto;">
    '''
    for guild in guilds:
        html_result += f"<li style='margin-bottom: 8px;'><strong>{guild['name']}</strong> <span style='color: #666;'>(ID: {guild['id']})</span></li>"
    html_result += '''
        </ul>
    </div>
    '''
    return html_result

# Для локального тестирования (Render запустит код через gunicorn)
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
