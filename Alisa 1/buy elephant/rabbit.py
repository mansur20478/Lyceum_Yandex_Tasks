# импортируем библиотеки
from flask import Flask, request
from flask_ngrok import run_with_ngrok
import logging

import json

app = Flask(__name__)
run_with_ngrok(app)

logging.basicConfig(level=logging.INFO)

sessionStorage = {}
rabbit_time = {}


@app.route('/post', methods=['POST'])
def main():
    need = request.json
    if need['session']['new'] or not rabbit_time[need['session']['user_id']]:
        logging.info(f'Request: {request.json!r}')

        response = {
            'session': request.json['session'],
            'version': request.json['version'],
            'response': {
                'end_session': False
            }
        }
        handle_dialog(request.json, response)

        logging.info(f'Response:  {response!r}')

        return json.dumps(response)
    else:
        logging.info(f'Request: {request.json!r}')

        response = {
            'session': request.json['session'],
            'version': request.json['version'],
            'response': {
                'end_session': False
            }
        }
        handle_dialog_rabbit(request.json, response)

        logging.info(f'Response:  {response!r}')

        return json.dumps(response)


def handle_dialog(req, res):
    user_id = req['session']['user_id']

    if req['session']['new']:

        sessionStorage[user_id] = {
            'suggests': [
                "Не хочу.",
                "Не буду.",
                "Отстань!",
            ]
        }
        res['response']['text'] = 'Привет! Купи слона!'
        rabbit_time[user_id] = False
        res['response']['buttons'] = get_suggests(user_id)
        return

    if req['request']['original_utterance'].lower() in [
        'ладно',
        'куплю',
        'покупаю',
        'хорошо',
        'я покупаю',
        'я куплю'
    ]:
        res['response']['text'] = 'Слона можно найти на Яндекс.Маркете!'
        res['response']['end_session'] = False
        rabbit_time[user_id] = 1
        return

    res['response']['text'] = \
        f"Все говорят '{req['request']['original_utterance']}', а ты купи слона!"
    res['response']['buttons'] = get_suggests(user_id)


def handle_dialog_rabbit(req, res):
    user_id = req['session']['user_id']

    if rabbit_time[user_id] == 1:
        sessionStorage[user_id] = {
            'suggests': [
                "Не хочу.",
                "Не буду.",
                "Отстань!",
            ]
        }
        res['response']['text'] = 'Привет! Купи кролика!'
        res['response']['buttons'] = get_suggests(user_id)
        rabbit_time[user_id] = 2
        return

    if req['request']['original_utterance'].lower() in [
        'ладно',
        'куплю',
        'покупаю',
        'хорошо',
        'Я покупаю',
        'Я покупаю'
    ]:
        res['response']['text'] = 'Кролика можно найти на Яндекс.Маркете!'
        res['response']['end_session'] = True
        return

    res['response']['text'] = \
        f"Все говорят '{req['request']['original_utterance']}', а ты купи кролика!"
    res['response']['buttons'] = get_suggests(user_id)


def get_suggests(user_id):
    session = sessionStorage[user_id]

    suggests = [
        {'title': suggest, 'hide': True}
        for suggest in session['suggests'][:2]
    ]

    session['suggests'] = session['suggests'][1:]
    sessionStorage[user_id] = session

    if len(suggests) < 2:
        suggests.append({
            "title": "Ладно",
            "url": "https://market.yandex.ru/search?text=слон",
            "hide": True
        })

    return suggests


if __name__ == '__main__':
    app.run()
