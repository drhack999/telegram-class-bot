import telebot
from telebot import types
import os
import random

# --- НАСТРОЙКИ ---
BOT_TOKEN = "-"  # Вставь сюда свой токен от BotFather
BASE_PATH = r"C:\Users\Admin\Desktop\coding\tempp" # Путь к папке с файлами классов
BUTTONS_PER_ROW = 3 # Сколько кнопок классов отображать в одном ряду на ReplyKeyboard
# --- КОНЕЦ НАСТРОЕК ---

bot = telebot.TeleBot(BOT_TOKEN)

# Глобальный список имен классов для проверки в message_handler
AVAILABLE_CLASSES = []

def update_available_classes():
    """Сканирует папку BASE_PATH и обновляет глобальный список имен классов."""
    global AVAILABLE_CLASSES
    classes = []
    try:
        for filename in os.listdir(BASE_PATH):
            if filename.endswith(".txt"):
                class_name = filename[:-4] # Убираем ".txt"
                classes.append(class_name)
        AVAILABLE_CLASSES = sorted(classes) # Сортируем для единообразия
        return AVAILABLE_CLASSES
    except FileNotFoundError:
        print(f"ОШИБКА: Папка {BASE_PATH} не найдена!")
        AVAILABLE_CLASSES = []
        return []
    except Exception as e:
        print(f"Произошла ошибка при получении списка классов: {e}")
        AVAILABLE_CLASSES = []
        return []

def get_students_from_class(class_name):
    """Читает файл класса и возвращает список учеников."""
    file_path = os.path.join(BASE_PATH, f"{class_name}.txt")
    students = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                student_name = line.strip()
                if student_name: # Пропускаем пустые строки
                    students.append(student_name)
        return students
    except FileNotFoundError:
        print(f"Файл для класса {class_name} не найден: {file_path}")
        return None
    except Exception as e:
        print(f"Ошибка при чтении файла {file_path}: {e}")
        return None

def create_class_keyboard():
    """Создает ReplyKeyboardMarkup с кнопками классов."""
    classes = AVAILABLE_CLASSES
    if not classes:
        return None

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    # one_time_keyboard=False означает, что клавиатура не исчезнет после нажатия

    row_buttons = []
    for i, class_name in enumerate(classes):
        row_buttons.append(types.KeyboardButton(text=class_name))
        if (i + 1) % BUTTONS_PER_ROW == 0 or (i + 1) == len(classes):
            markup.add(*row_buttons)
            row_buttons = []
    return markup

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    """Отправляет приветственное сообщение и кнопки с классами."""
    update_available_classes() # Обновляем список классов при старте
    
    if not AVAILABLE_CLASSES:
        bot.reply_to(message, "Не найдены файлы классов. Проверьте настройки и наличие файлов .txt в папке.")
        return

    markup = create_class_keyboard()
    if markup:
        bot.send_message(message.chat.id,
                         "Привет! Выберите класс, нажав на одну из кнопок ниже, чтобы получить случайного ученика:",
                         reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "Не удалось создать клавиатуру классов. Возможно, список классов пуст.")


# Обработчик для текстовых сообщений, которые совпадают с именами классов
@bot.message_handler(func=lambda message: message.text in AVAILABLE_CLASSES)
def handle_class_selection_text(message):
    """Обрабатывает выбор класса через текстовую кнопку."""
    class_name = message.text
    
    students = get_students_from_class(class_name)

    if students is None: # Файл не найден или ошибка чтения
        bot.send_message(message.chat.id, f"Не удалось загрузить список учеников для класса {class_name}. Проверьте консоль бота для деталей.")
        return
    
    if not students: # Файл найден, но пустой
        bot.send_message(message.chat.id, f"Список учеников для класса {class_name} пуст.")
        return

    random_student = random.choice(students)
    
    bot.send_message(message.chat.id, f"Случайный ученик из класса {class_name}: \n\n✨ **{random_student}** ✨", parse_mode="Markdown")
    
    # Клавиатура ReplyKeyboardMarkup остается видимой по умолчанию, если one_time_keyboard=False

@bot.message_handler(func=lambda message: True) # Обрабатывает любые другие текстовые сообщения
def handle_other_messages(message):
    """Обрабатывает сообщения, не являющиеся командами или выбором класса."""
    if AVAILABLE_CLASSES: # Если классы есть, но пользователь написал что-то другое
        markup = create_class_keyboard()
        bot.send_message(message.chat.id,
                         "Пожалуйста, выберите класс из предложенных кнопок.",
                         reply_markup=markup)
    else: # Если классов нет вообще
        bot.send_message(message.chat.id,
                         "Список классов не загружен. Попробуйте команду /start или обратитесь к администратору бота.")


if __name__ == '__main__':
    print("Бот запускается...")
    if not os.path.exists(BASE_PATH):
        print(f"Критическая ОШИБКА: Директория '{BASE_PATH}' не существует. Создайте ее и поместите туда файлы классов.")
    else:
        update_available_classes() # Первоначальная загрузка классов
        if AVAILABLE_CLASSES:
            print(f"Доступные классы: {AVAILABLE_CLASSES}")
        else:
            print("Файлы классов не найдены или папка пуста.")
        print("Бот запущен! Нажмите Ctrl+C для остановки.")
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            print(f"Ошибка во время работы бота: {e}")
        finally:
            print("Бот остановлен.")