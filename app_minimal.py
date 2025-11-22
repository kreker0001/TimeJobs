# app_minimal.py
from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Time Jobs - Тест</title>
            <script src="https://cdn.tailwindcss.com"></script>
        </head>
        <body class="bg-gray-900 text-white min-h-screen flex items-center justify-center">
            <div class="text-center">
                <h1 class="text-4xl font-bold mb-4">Time Jobs</h1>
                <p class="text-xl text-green-400">Flask работает успешно!</p>
                <p class="mt-4">Сервер запущен и готов к работе</p>
                <div class="mt-6">
                    <a href="/login" class="bg-green-500 text-black px-6 py-2 rounded-lg mr-2">Войти</a>
                    <a href="/register" class="bg-gray-700 px-6 py-2 rounded-lg">Регистрация</a>
                </div>
            </div>
        </body>
        </html>
    ''')

@app.route('/login')
def login():
    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Вход - Time Jobs</title>
            <script src="https://cdn.tailwindcss.com"></script>
        </head>
        <body class="bg-gray-900 text-white min-h-screen flex items-center justify-center">
            <div class="bg-gray-800 p-8 rounded-lg w-96">
                <h2 class="text-2xl font-bold mb-6 text-center">Вход</h2>
                <form>
                    <input type="email" placeholder="Email" class="w-full p-3 mb-4 bg-gray-700 rounded border border-gray-600">
                    <input type="password" placeholder="Пароль" class="w-full p-3 mb-4 bg-gray-700 rounded border border-gray-600">
                    <button class="w-full bg-green-500 text-black p-3 rounded font-semibold">Войти</button>
                </form>
            </div>
        </body>
        </html>
    ''')

@app.route('/register')
def register():
    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Регистрация - Time Jobs</title>
            <script src="https://cdn.tailwindcss.com"></script>
        </head>
        <body class="bg-gray-900 text-white min-h-screen flex items-center justify-center">
            <div class="bg-gray-800 p-8 rounded-lg w-96">
                <h2 class="text-2xl font-bold mb-6 text-center">Регистрация</h2>
                <form>
                    <input type="text" placeholder="Имя" class="w-full p-3 mb-4 bg-gray-700 rounded border border-gray-600">
                    <input type="email" placeholder="Email" class="w-full p-3 mb-4 bg-gray-700 rounded border border-gray-600">
                    <input type="password" placeholder="Пароль" class="w-full p-3 mb-4 bg-gray-700 rounded border border-gray-600">
                    <div class="grid grid-cols-2 gap-2 mb-4">
                        <button type="button" class="p-2 bg-gray-700 rounded border border-gray-600">Соискатель</button>
                        <button type="button" class="p-2 bg-gray-700 rounded border border-gray-600">Работодатель</button>
                    </div>
                    <button class="w-full bg-green-500 text-black p-3 rounded font-semibold">Создать аккаунт</button>
                </form>
            </div>
        </body>
        </html>
    ''')

if __name__ == '__main__':
    print("Запуск сервера Time Jobs...")
    print("Откройте: http://localhost:5000")
    app.run(debug=True, port=5000)