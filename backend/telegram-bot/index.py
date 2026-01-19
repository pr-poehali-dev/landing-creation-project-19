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
        
        if 'message' in body:
            message = body['message']
            chat_id = message['chat']['id']
            user_text = message.get('text', '').lower().strip()
            
            response_text = get_response(user_text)
            
            send_telegram_message(chat_id, response_text)
            
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
            'keywords': ['привет', 'здравствуй', 'добрый', 'start', 'начать'],
            'response': '''Привет! 👋

Я ИИ-ассистент по ИИ-маркетингу. Помогу ответить на вопросы о наших услугах:

✨ Продающие лендинги
📊 Презентации для бизнеса  
📈 Инфографика
📸 ИИ-фотосессии
🎬 Видео и промо-ролики
🤖 ИИ-ассистенты
👤 ИИ-аватары

Просто напишите, что вас интересует!'''
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
            'keywords': ['контакт', 'связь', 'телефон', 'почта', 'заявка', 'консультация'],
            'response': '''📞 Связаться со мной:

Хотите бесплатный аудит и план работ?

1️⃣ Оставьте заявку на сайте
2️⃣ Напишите мне в личку @your_telegram
3️⃣ Email: hello@example.com

Отвечу в течение 24 часов!

Или задайте вопрос прямо здесь — я помогу 😊'''
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


def send_telegram_message(chat_id: int, text: str):
    '''Отправляет сообщение в Telegram через Bot API'''
    import urllib.request
    
    token = os.environ.get('TELEGRAM_BOT_TOKEN')
    if not token:
        return
    
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    
    data = json.dumps({
        'chat_id': chat_id,
        'text': text,
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