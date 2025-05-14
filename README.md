# Telegram Class Bot

Бот выбирает случайного ученика из указанного класса.

## Установка и запуск

1. Склонируйте репозиторий:
   ```bash
   git clone https://github.com/ВАШ_НИК/telegram-class-bot.git
   cd telegram-class-bot
   ```
2. Откройте `bot.py` и замените строку
   ```python
   BOT_TOKEN = "—"
   ```
   на [ваш токен от BotFather](https://chatlabs.ru/botfather-instrukcziya-komandy-nastrojki/);
   так же, замените строку 
      ```python
   BASE_PATH = "—"
   ```
    на нужную директорию, где будут тектовые файлы с ФИО учеников.

3. Установите зависимости:
   ```bash
   pip install pyTelegramBotAPI
   ```

4. Запустите бота:
   ```bash
   python bot.py
   ```

## Структура проекта

- `bot.py` — код бота  
- `classes/` — текстовые файлы с учениками (по одному имени в строке)  
- `.gitignore` — исключает служебные файлы (`__pycache__/`, `*.pyc`)  
- `README.md` — это описание проекта и инструкция по установке  
