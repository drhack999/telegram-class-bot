````markdown
# Telegram Class Bot

Бот выбирает случайного ученика из указанного класса.

## Установка и запуск

1. Склонируйте репозиторий:
   ```bash
   git clone https://github.com/ВАШ_НИК/telegram-class-bot.git
   cd telegram-class-bot
````

2. Откройте `bot.py` и замените строку

   ```python
   BOT_TOKEN = "—"
   ```

   на ваш токен от BotFather.
3. Установите зависимости:

   ```bash
   pip install pyTelegramBotAPI
   ```
4. Запустите бота:

   ```bash
   python bot.py
   ```