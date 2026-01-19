import json
import os
import re
from typing import Optional

def handler(event: dict, context) -> dict:
    '''Telegram бот для автоматических ответов посетителям на основе информации с лендинга'''
    
    method = event.get('httpMethod', 'POST')
    path = event.get('requestContext', {}).get('path', '')
    
    if method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': ''
        }
    
    if method == 'GET' and 'setup' in event.get('queryStringParameters', {}):
        webhook_url = 'https://functions.poehali.dev/8bb85954-50a6-4342-bb36-ed6fdf091dbb'
        result = setup_webhook(webhook_url)
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps(result)
        }
    
    if method == 'POST':
        body = json.loads(event.get('body', '{}'))
        
        if 'callback_query' in body:
            callback = body['callback_query']
            chat_id = callback['message']['chat']['id']
            callback_data = callback['data']
            
            response_text = get_callback_response(callback_data)
            send_telegram_message(chat_id, response_text, False)
            answer_callback_query(callback['id'])
            
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'status': 'ok'})
            }
        
        if 'message' in body:
            message = body['message']
            chat_id = message['chat']['id']
            user_text = message.get('text', '').lower().strip()
            user_name = message.get('from', {}).get('first_name', 'Неизвестный')
            username = message.get('from', {}).get('username', '')
            
            notify_manager(user_name, username, user_text)
            
            response_text = get_response(user_text)
            show_menu = is_greeting(user_text)
            
            send_telegram_message(chat_id, response_text, show_menu)
            
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'status': 'ok'})
            }
    
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps({'status': 'ok'})
    }


def get_response(user_text: str) -> str:
    '''Возвращает ответ на основе базы знаний лендинга'''
    
    knowledge_base = {
        'приветствие': {
            'keywords': ['привет', 'здравствуй', 'добрый', 'start', 'начать', '/start'],
            'response': '''Привет! 👋 Рад знакомству!

Я ИИ-ассистент по ИИ-маркетингу. Помогу быстро получить информацию о наших услугах и ответить на вопросы.

🎯 Что я умею:
• Рассказать про услуги и цены
• Объяснить процесс работы
• Показать примеры проектов
• Подсказать, как заказать

💼 Наши услуги:
✨ Продающие лендинги
📊 Презентации для бизнеса  
📈 Инфографика
📸 ИИ-фотосессии
🎬 Видео и промо-ролики
🤖 ИИ-ассистенты
👤 ИИ-аватары

❓ Просто напишите вопрос — например:
"Сколько стоит лендинг?"
"Как заказать?"
"Расскажи про процесс работы"

📞 Или сразу свяжитесь с менеджером для консультации:
👉 https://t.me/a_ginn'''
        },
        
        'цены': {
            'keywords': ['цена', 'стоимость', 'сколько стоит', 'тариф', 'пакет', 'прайс'],
            'response': '''💰 Наши пакеты услуг:

🟢 СТАРТ — от 30 тыс. ₽
Лендинг ИЛИ контент-план + инфографика
Срок: 7 дней

🔵 БИЗНЕС — от 75 тыс. ₽  
Лендинг + контент + 3 видео + инфографика
Срок: 10 дней

🟣 ПРО — от 150 тыс. ₽
Полный комплекс + фотосессия + карточки товаров
Срок: 14 дней

⭐ ПРЕМИУМ — от 300 тыс. ₽
Всё включено: лендинг, видео, фото, ассистент, аватар
Срок: 21 день'''
        },
        
        'лендинг': {
            'keywords': ['лендинг', 'сайт', 'страниц', 'landing'],
            'response': '''✨ Продающие ИИ-лендинги

Создаю одностраничные сайты под продажу услуг за 5-7 дней:
• Структура по проверенным схемам
• Убеждающие тексты с УТП
• ИИ-визуал под ваш бренд
• Формы заявок и аналитика
• Средняя конверсия: 5-12%

Экономия: в 5-10 раз дешевле агентств!

От 30 тыс. ₽ (пакет СТАРТ)'''
        },
        
        'видео': {
            'keywords': ['видео', 'ролик', 'промо', 'съемка'],
            'response': '''🎬 Видео и промо-ролики с ИИ

• Сценарий под вашу нишу
• Генерация кадров (Kling 2.6, Freepik)
• Профессиональный монтаж
• Озвучка и музыка
• Конверсия в 3-5 раз выше обычного

Без съёмочной команды и фотографов!

От 75 тыс. ₽ (в пакете БИЗНЕС)'''
        },
        
        'фото': {
            'keywords': ['фото', 'фотосессия', 'снимок', 'изображение'],
            'response': '''📸 ИИ-фотосессия для бизнеса

Генерирую фирменные снимки через Google Nano Banana Pro:
• Вы, команда, продукты
• Любой стиль и фон
• Без реальной съёмки
• Экономия: в 5-10 раз дешевле

Получаете уникальные профессиональные фото без фотографа!

От 150 тыс. ₽ (в пакете ПРО)'''
        },
        
        'бот': {
            'keywords': ['бот', 'ассистент', 'чат-бот', 'автоответ'],
            'response': '''🤖 ИИ-ассистент для бизнеса

Настраиваю персонального ассистента:
• Отвечает на вопросы клиентов 24/7
• Консультирует по вашим услугам
• Помогает менеджерам
• Экономит время на 30-50%

Работает в Telegram, на сайте, в мессенджерах!

От 150 тыс. ₽ (в пакете ПРО)'''
        },
        
        'контент': {
            'keywords': ['контент', 'текст', 'план', 'инстаграм', 'телеграм', 'соцсети'],
            'response': '''✍️ Уникальные тексты + контент-план

Создаю на 30-90 дней:
• Позиционирование бренда
• Рубрики контента
• Готовые посты для Instagram, TikTok, Telegram
• Каждый пост ориентирован на продажи

Вы просто публикуете по графику!

От 30 тыс. ₽ (пакет СТАРТ)'''
        },
        
        'инфографика': {
            'keywords': ['инфографика', 'схема', 'график', 'визуализация'],
            'response': '''📈 Профессиональная инфографика

Превращаю сложное в понятное:
• Данные, процессы, услуги → схемы
• Стиль под ваш бренд
• Для лендингов, контента, обучения

Ваши клиенты сразу понимают ценность!

Включено во все пакеты от 30 тыс. ₽'''
        },
        
        'аватар': {
            'keywords': ['аватар', 'видеоаватар', 'heygen', 'цифровой'],
            'response': '''👤 ИИ-аватар руководителя через HeyGen

Создаю цифровой образ:
• Видеообращения без камеры
• Обучающие курсы
• Прямые эфиры
• Выглядит как настоящее видео

Запишите 1 раз — используйте бесконечно!

От 300 тыс. ₽ (пакет ПРЕМИУМ)'''
        },
        
        'процесс': {
            'keywords': ['как работа', 'процесс', 'этап', 'срок', 'сколько дней'],
            'response': '''🔄 Процесс работы (10-14 дней):

1️⃣ ДИАГНОСТИКА
Разбираю нишу, ставлю метрики, согласуем задачу

2️⃣ КОНЦЕПЦИЯ  
Структура, визуал, тексты → ваша обратная связь

3️⃣ ПРОИЗВОДСТВО
Генерирую всё на ИИ + ручная доработка

4️⃣ ЗАПУСК
Внедрение, аналитика, рекомендации по A/B-тестам

Первые результаты через 2-3 недели!'''
        },
        
        'инструменты': {
            'keywords': ['инструмент', 'нейросеть', 'ai', 'perplexity', 'heygen', 'freepik', 'kling'],
            'response': '''🛠️ Используем передовые ИИ-инструменты:

• Perplexity AI — исследования и анализ
• HeyGen — ИИ-аватары и видео
• Google NotebookLM — обработка текстов
• Freepik — генерация изображений  
• Nano Banana Pro — фотосессии продуктов
• Kling 2.6 — видео высокого качества

Всё самое современное для вашего бизнеса!'''
        },
        
        'преимущества': {
            'keywords': ['преимущество', 'почему', 'отличие', 'зачем'],
            'response': '''🎯 Почему выбирают нас:

⚡ СКОРОСТЬ — дни, а не месяцы
💰 ЭКОНОМИЯ — в 5-10 раз дешевле
🎯 РЕЗУЛЬТАТ — фокус на конверсию
🔄 БЫСТРЫЕ ТЕСТЫ — A/B за часы
📊 ПО СКРИПТУ — проверенные схемы
🤝 ОДИН ИСПОЛНИТЕЛЬ — не нужна армия фрилансеров
🚀 ПЕРЕДОВЫЕ ТЕХНОЛОГИИ
🔒 ПОЛНЫЕ ПРАВА на контент'''
        },
        
        'контакты': {
            'keywords': ['контакт', 'связь', 'телефон', 'почта', 'заявка', 'консультация', 'заказать', 'заказ', 'оформить', 'купить', 'подробн', 'детал'],
            'response': '''📞 Как связаться и заказать?

🎯 Для консультации и заказа напишите напрямую:
👉 https://t.me/a_ginn

✅ Что я предложу:
• Бесплатный аудит вашей ниши
• Персональный план работ
• Расчёт стоимости под ваш проект
• Ответы на все вопросы

⏰ Отвечу в течение 24 часов!

Или продолжайте задавать вопросы здесь — я помогу 😊'''
        }
    }
    
    for category, data in knowledge_base.items():
        for keyword in data['keywords']:
            if keyword in user_text:
                return data['response']
    
    return '''Спасибо за вопрос! 🤔

Я могу рассказать про:
• Цены и тарифы
• Лендинги и сайты
• Видео и промо-ролики
• ИИ-фотосессии
• Контент-планы
• ИИ-ассистентов и ботов
• Процесс работы

Просто напишите, что интересует!

Или оставьте заявку на сайте для персональной консультации 👉'''


def get_callback_response(callback_data: str) -> str:
    '''Возвращает ответ на нажатие кнопки'''
    responses = {
        'prices': '''💰 Наши пакеты услуг:

🟢 СТАРТ — от 30 тыс. ₽
Лендинг ИЛИ контент-план + инфографика
Срок: 7 дней

🔵 БИЗНЕС — от 75 тыс. ₽  
Лендинг + контент + 3 видео + инфографика
Срок: 10 дней

🟣 ПРО — от 150 тыс. ₽
Полный комплекс + фотосессия + карточки товаров
Срок: 14 дней

⭐ ПРЕМИУМ — от 300 тыс. ₽
Всё включено: лендинг, видео, фото, ассистент, аватар
Срок: 21 день

📞 Для точного расчёта напишите:
👉 https://t.me/a_ginn''',
        
        'services': '''💼 Что я делаю с ИИ для вашего бизнеса:

✨ Продающие ИИ-лендинги (5-7 дней, конверсия 5-12%)
📊 Презентации для бизнеса (питчдеки, видео)
📈 Профессиональная инфографика
📸 ИИ-фотосессия (без фотографа!)
🛍️ Карточки товаров для маркетплейсов
🎵 Песни и гимны компании
✍️ Контент-план на 30-90 дней
🤖 ИИ-ассистент для клиентов 24/7
👤 ИИ-аватар руководителя
🎬 Видео и промо-ролики

Экономия: в 5-10 раз дешевле агентств!''',
        
        'process': '''🔄 Процесс работы (10-14 дней):

1️⃣ ДИАГНОСТИКА
Разбираю нишу, ставлю метрики, согласуем задачу

2️⃣ КОНЦЕПЦИЯ  
Структура, визуал, тексты → ваша обратная связь

3️⃣ ПРОИЗВОДСТВО
Генерирую всё на ИИ + ручная доработка

4️⃣ ЗАПУСК
Внедрение, аналитика, рекомендации по A/B-тестам

⏰ Первые результаты через 2-3 недели!

📞 Готовы начать? Напишите:
👉 https://t.me/a_ginn''',
        
        'tools': '''🛠️ Используем передовые ИИ-инструменты:

• Perplexity AI — исследования и анализ
• HeyGen — ИИ-аватары и видео
• Google NotebookLM — обработка текстов
• Freepik — генерация изображений  
• Nano Banana Pro — фотосессии продуктов
• Kling 2.6 — видео высокого качества

🚀 Всё самое современное для вашего бизнеса!

❓ Есть вопросы? Пишите:
👉 https://t.me/a_ginn'''
    }
    
    return responses.get(callback_data, 'Выберите интересующую тему из меню!')


def is_greeting(user_text: str) -> bool:
    '''Проверяет, является ли сообщение приветствием'''
    greetings = ['привет', 'здравствуй', 'добрый', 'start', 'начать', '/start']
    return any(keyword in user_text for keyword in greetings)


def send_telegram_message(chat_id: int, text: str, show_menu: bool = False):
    '''Отправляет сообщение в Telegram через Bot API с интерактивными кнопками'''
    import urllib.request
    
    token = os.environ.get('TELEGRAM_BOT_TOKEN')
    if not token:
        return
    
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    
    payload = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': 'HTML'
    }
    
    if show_menu:
        payload['reply_markup'] = {
            'inline_keyboard': [
                [
                    {'text': '💰 Цены и тарифы', 'callback_data': 'prices'},
                    {'text': '📋 Услуги', 'callback_data': 'services'}
                ],
                [
                    {'text': '🔄 Процесс работы', 'callback_data': 'process'},
                    {'text': '🛠️ ИИ-инструменты', 'callback_data': 'tools'}
                ],
                [
                    {'text': '📞 Связаться с менеджером', 'url': 'https://t.me/shipuchka_show'}
                ]
            ]
        }
    
    data = json.dumps(payload).encode('utf-8')
    
    req = urllib.request.Request(
        url,
        data=data,
        headers={'Content-Type': 'application/json'}
    )
    
    try:
        urllib.request.urlopen(req)
    except Exception:
        pass


def answer_callback_query(callback_query_id: str):
    '''Отвечает на callback запрос (убирает "часики" на кнопке)'''
    import urllib.request
    
    token = os.environ.get('TELEGRAM_BOT_TOKEN')
    if not token:
        return
    
    url = f'https://api.telegram.org/bot{token}/answerCallbackQuery'
    
    data = json.dumps({
        'callback_query_id': callback_query_id
    }).encode('utf-8')
    
    req = urllib.request.Request(
        url,
        data=data,
        headers={'Content-Type': 'application/json'}
    )
    
    try:
        urllib.request.urlopen(req)
    except Exception:
        pass


def notify_manager(user_name: str, username: str, message: str):
    '''Отправляет уведомление менеджеру о новом сообщении от клиента'''
    import urllib.request
    
    manager_chat_id = os.environ.get('MANAGER_CHAT_ID')
    if not manager_chat_id:
        return
    
    token = os.environ.get('TELEGRAM_BOT_TOKEN')
    if not token:
        return
    
    username_text = f'(@{username})' if username else ''
    notification = f'''🔔 Новое сообщение от клиента!

👤 {user_name} {username_text}
💬 "{message}"

📞 Ответьте клиенту: https://t.me/{username if username else 'Aginnvl_bot'}'''
    
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    
    data = json.dumps({
        'chat_id': manager_chat_id,
        'text': notification,
        'parse_mode': 'HTML'
    }).encode('utf-8')
    
    req = urllib.request.Request(
        url,
        data=data,
        headers={'Content-Type': 'application/json'}
    )
    
    try:
        urllib.request.urlopen(req)
    except Exception:
        pass


def setup_webhook(webhook_url: str) -> dict:
    '''Устанавливает webhook для Telegram бота'''
    import urllib.request
    
    token = os.environ.get('TELEGRAM_BOT_TOKEN')
    if not token:
        return {'error': 'TELEGRAM_BOT_TOKEN not found'}
    
    url = f'https://api.telegram.org/bot{token}/setWebhook'
    
    data = json.dumps({
        'url': webhook_url
    }).encode('utf-8')
    
    req = urllib.request.Request(
        url,
        data=data,
        headers={'Content-Type': 'application/json'}
    )
    
    try:
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode('utf-8'))
        return result
    except Exception as e:
        return {'error': str(e)}