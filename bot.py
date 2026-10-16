import telebot
from telebot import types

# ⚙️ НАСТРОЙКИ СИНДИКАТА RISCO RICO
TOKEN = "8639002029:AAGFm-qisYTmnnWt9ULjJsOKFUBw58C1GWI"
ADMIN_ID = "8713500528"

bot = telebot.TeleBot(TOKEN)
user_data = {}

@bot.message_handler(commands=['start'])
def start_message(message):
    user_data[message.chat.id] = {}
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn_start = types.InlineKeyboardButton("Запустить калькулятор РКО", callback_data="st_audit")
    markup.add(btn_start)
    
    text = (
        "<b>RISCO RICO | Добро пожаловать в систему 🐺💼</b>\n\n"
        "На связи основатель независимого финтех-сервиса <b>Risco Rico</b>.\n\n"
        "Мы препарируем мелкий шрифт договоров всех топ-банков РФ под налоги и реальные обороты вашей ниши. Наш бот рассчитает скрытую дань банкирам за 30 секунд.\n\n"
        "🎯 <i>Давайте заберем ваши деньги обратно в оборот.</i>"
    )
    bot.send_message(message.chat.id, text, parse_mode="HTML", reply_markup=markup)

# ШАГ 1: ЮРЛИЦО
@bot.callback_query_handler(func=lambda call: call.data == "st_audit")
def step_1(call):
    chat_id = call.message.chat.id
    bot.delete_message(chat_id, call.message.message_id)
    
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("Да, есть ИП / ООО", callback_data="u_yes"),
        types.InlineKeyboardButton("Нет, хочу открыть бесплатно 0₽", callback_data="u_no")
    )
    bot.send_message(chat_id, "<b>📈 Шаг 1 из 5. У вас уже открыто юрлицо?</b>", parse_mode="HTML", reply_markup=markup)

# ШАГ 2: НИША
@bot.callback_query_handler(func=lambda call: call.data in ["u_yes", "u_no"])
def step_2(call):
    chat_id = call.message.chat.id
    user_data[chat_id] = {}
    user_data[chat_id]['reg'] = "ИП уже открыто" if call.data == "u_yes" else "Требуется открытие с нуля"
    
    bot.delete_message(chat_id, call.message.message_id)
    
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("Маркетплейсы (WB / Ozon)", callback_data="n_mp"),
        types.InlineKeyboardButton("Розница (Магазин, Автосервис)", callback_data="n_rt"),
        types.InlineKeyboardButton("Оптовая торговля / B2B", callback_data="n_op")
    )
    bot.send_message(chat_id, "<b>💼 Шаг 2 из 5. Выберите ваше направление:</b>", parse_mode="HTML", reply_markup=markup)

# ШАГ 3: ПЛАТЕЖКИ
@bot.callback_query_handler(func=lambda call: call.data in ["n_mp", "n_rt", "n_op"])
def step_3(call):
    chat_id = call.message.chat.id
    niche_map = {"n_mp": "Маркетплейсы", "n_rt": "Розница", "n_op": "Опт / B2B"}
    user_data[chat_id]['niche'] = niche_map[call.data]
    
    bot.delete_message(chat_id, call.message.message_id)
    
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("До 10 платежек в месяц", callback_data="p_10"),
        types.InlineKeyboardButton("От 11 до 50 платежек", callback_data="p_50"),
        types.InlineKeyboardButton("Более 50 платежек (Активный бизнес)", callback_data="p_max")
    )
    bot.send_message(chat_id, "<b>🧾 Шаг 3 из 5. Сколько платежных поручений поставщикам отправляете в месяц?</b>", parse_mode="HTML", reply_markup=markup)

# ШАГ 4: ВЫРУЧКА
@bot.callback_query_handler(func=lambda call: call.data in ["p_10", "p_50", "p_max"])
def step_4(call):
    chat_id = call.message.chat.id
    p_map = {"p_10": "До 10 шт", "p_50": "11-50 шт", "p_max": "Более 50 шт"}
    user_data[chat_id]['payments'] = p_map[call.data]
    user_data[chat_id]['p_raw'] = call.data
    
    bot.delete_message(chat_id, call.message.message_id)
    
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("До 300 000 ₽", callback_data="o_300"),
        types.InlineKeyboardButton("От 300 000 ₽ до 1 млн ₽", callback_data="o_1m"),
        types.InlineKeyboardButton("Более 1 млн ₽ (Big Money)", callback_data="o_max")
    )
    bot.send_message(chat_id, "<b>💵 Шаг 4 из 5. Какой планируемый оборот (выручка) в месяц?</b>", parse_mode="HTML", reply_markup=markup)

# ШАГ 5: ВЫВОД НА КАРТУ
@bot.callback_query_handler(func=lambda call: call.data in ["o_300", "o_1m", "o_max"])
def step_5(call):
    chat_id = call.message.chat.id
    o_map = {"o_300": "До 300к", "o_1m": "300к - 1млн", "o_max": "Более 1млн"}
    user_data[chat_id]['volume'] = o_map[call.data]
    user_data[chat_id]['o_raw'] = call.data
    
    bot.delete_message(chat_id, call.message.message_id)
    
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("До 150 000 ₽", callback_data="w_150"),
        types.InlineKeyboardButton("От 150 000 ₽ до 500 000 ₽", callback_data="w_500"),
        types.InlineKeyboardButton("Более 500 000 ₽", callback_data="w_max")
    )
    bot.send_message(chat_id, "<b>💸 Шаг 5 из 5. Сколько из этой суммы нужно выводить себе на личную карту каждый месяц?</b>", parse_mode="HTML", reply_markup=markup)

# ФИНАЛ И ПЕРЕХВАТ ЛИДА К CEO RR
@bot.callback_query_handler(func=lambda call: call.data in ["w_150", "w_500", "w_max"])
def final_step(call):
    chat_id = call.message.chat.id
    bot.delete_message(chat_id, call.message.message_id)
    
    loss_p = 0 if user_data[chat_id].get('p_raw') == "p_10" else (2500 if user_data[chat_id].get('p_raw') == "p_50" else 6000)
    loss_w = 0 if call.data == "w_150" else (4500 if call.data == "w_500" else 15000)
    total_loss = loss_p + loss_w + (5000 if user_data[chat_id].get('o_raw') == "o_max" else 1500)
    
    w_map = {"w_150": "До 150к", "w_500": "150к-500к", "w_max": "Более 500к"}
    user_data[chat_id]['withdraw'] = w_map[call.data]
    
    username = f"@{call.from_user.username}" if call.from_user.username else "Скрыт"
    
    admin_text = (
        "<b>🔥 CEO RR, У КОНКУРЕНТОВ НЕТ ШАНСОВ! ПОЛНЫЙ АУДИТ ГОТОВ:</b>\n\n"
        f"👤 <b>Лид:</b> {call.from_user.first_name} ({username})\n"
        f"📋 <b>Юрлицо:</b> {user_data[chat_id]['reg']}\n"
        f"🎯 <b>Ниша:</b> {user_data[chat_id]['niche']}\n"
        f"🧾 <b>Платежки:</b> {user_data[chat_id]['payments']}\n"
        f"💰 <b>Выручка:</b> {user_data[chat_id]['volume']}\n"
        f"💸 <b>Вывод себе:</b> {user_data[chat_id]['withdraw']}\n"
        f"📉 <b>Прогноз скрытых потерь:</b> ~{total_loss} ₽/мес\n\n"
        "⚡️ <i>Данные полные. Копируй юзернейм, открывай таблицу банков и пиши наш скрипт перехвата в ЛС. Время забирать этот кэш!</i>"
    )
    try:
        bot.send_message(ADMIN_ID, admin_text, parse_mode="HTML")
    except Exception as e:
        print(f"Ошибка админа: {e}")

    client_text = (
        f"<b>🎯 Интерактивный анонимный аудит Risco Rico завершен!</b>\n\n"
        f"По нашей базе ТОП-15 банков РФ, при ваших оборотах (<b>{user_data[chat_id]['volume']}</b>) и объеме платежек, скрытые комиссии могут обходиться вам примерно в <b>{total_loss} ₽ в месяц</b> за пустые услуги.\n\n"
        "⏱ <b>В течение 5 минут</b> команда Risco Rico изучит эти цифры и пришлет вам в личку независимую раскладку: в каком банке вам дадут максимальные лимиты без комиссий.\n\n"
        "<i>Вы в системе. Хватит переплачивать банкирам за воздух!</i>"
    )
    bot.send_message(chat_id, client_text, parse_mode="HTML")

print("🚀 Бот RISCO RICO успешно запущен и караулит лиды!")
bot.remove_webhook()
bot.infinity_polling()
