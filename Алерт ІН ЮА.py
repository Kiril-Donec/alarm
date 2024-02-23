import os
import time
from alerts_in_ua import Client as AlertsClient
import telebot

# Отримуємо шлях до файлу, який виконується
dir_path = os.path.dirname(os.path.realpath(__file__))

# Читаємо токен з файлу
with open(os.path.join(dir_path, 'токен.txt'), 'r') as file:
    token = file.read().strip()

# Читаємо токен бота з файлу
with open(os.path.join(dir_path, 'токенбот.txt'), 'r') as file:
    bot_token = file.read().strip()

alerts_client = AlertsClient(token=token)
bot = telebot.TeleBot(bot_token)

previous_alerts = {}

# Зберігаємо поточний стан тривоги при запуску
active_alerts = alerts_client.get_active_alerts()
previous_alerts = {alert.location_oblast: alert for alert in active_alerts}

while True:
    time.sleep(15)
    active_alerts = alerts_client.get_active_alerts()
    current_alerts = {alert.location_oblast: alert for alert in active_alerts}

    # Перевіряємо нові тривоги
    for oblast, alert in current_alerts.items():
        if oblast not in previous_alerts:
            message = f"🔴 {alert.location_oblast} - повітряна тривога.\n"
            if alert.notes:
                message += f"Примітка: {alert.notes}"
            bot.send_message(-1002060861111, message)

    # Перевіряємо відбій тривоги
    for oblast, alert in list(previous_alerts.items()):
        if oblast not in current_alerts and not any(a.location_oblast == oblast for a in active_alerts):
            message = f"🟢 {alert.location_oblast} - відбій тривоги.\n"
            if alert.notes:
                message += f"Примітка: {alert.notes}"
            bot.send_message(-1002060861111, message)
            del previous_alerts[oblast]

    previous_alerts.update(current_alerts)
