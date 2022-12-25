import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, MessageTemplateAction

from fsm import TocMachine
from utils import send_text_message, send_button_message, send_image_message


load_dotenv()


# FSM圖的state跟transition
machine = TocMachine(
    states=[
        'user',
        'menu',
        'fsm',
        'help',
        'choose_type',
        'teach_or_example',
        'teach',
        'example',
    ],
    transitions=[
        {
            'trigger': 'advance', 
            'source': 'user', 
            'dest': 'menu', 
            'conditions': 'is_going_to_menu'
        },

        {
            'trigger': 'advance', 
            'source': 'user', 
            'dest': 'fsm', 
            'conditions': 'is_going_to_fsm'
        },

        {
            'trigger': 'advance', 
            'source': 'user', 
            'dest': 'help', 
            'conditions': 'is_going_to_help'
        },

        {
            'trigger': 'advance', 
            'source': 'menu', 
            'dest': 'choose_type', 
            'conditions': 'is_going_to_choose_type'
        },

        {
            'trigger': 'advance', 
            'source': 'choose_type', 
            'dest': 'teach_or_example', 
            'conditions': 'is_going_to_teach_or_example'
        },

        {
            'trigger': 'advance', 
            'source': 'teach_or_example', 
            'dest': 'teach', 
            'conditions': 'is_going_to_teach'
        },

        {
            'trigger': 'advance', 
            'source': 'teach_or_example', 
            'dest': 'example', 
            'conditions': 'is_going_to_example'
        },


        {
            'trigger': 'advance', 
            'source': 'teach', 
            'dest': 'teach_or_example', 
            'conditions': 'is_going_to_teach_or_example2'
        },

        {
            'trigger': 'advance', 
            'source': 'example', 
            'dest': 'teach_or_example', 
            'conditions': 'is_going_to_teach_or_example2'
        },

        
        {
            'trigger': 'advance', 
            'source': 'teach_or_example',
            'dest': 'menu', 
            'conditions': 'is_going_to_menu2'
        },

        # go_back
        {
            'trigger': 'go_back',
            'source': [
                'fsm',
                'help',
            ],
            'dest': 'user'
        },
    ],

    initial='user',
    auto_transitions=False,
    show_conditions=True,
)

app = Flask(__name__, static_url_path='')


# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)


@app.route('/callback', methods=['POST'])
def webhook_handler():
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f'Request body: {body}')

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)


    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue
        print(f'\nFSM STATE: {machine.state}')
        print(f'REQUEST BODY: \n{body}')
        response = machine.advance(event) # 從fsm.py的每個on_enter得來
        
        if response == False:
            
            #如果輸入非"start"的指令會一直卡在 user state
            if machine.state == 'user':
                text = '歡迎來到穿搭怪客的教室!\n\t輸入「fsm」: 查看有限狀態機設計圖\n\t輸入「help」: 教你如何使用穿搭怪客\n\t輸入「start」: 開始教學各類風格的髮型、穿搭，讓你一秒變成穿搭怪客!!!'
                send_text_message(event.reply_token, text)
            


    return 'OK'


@app.route('/show-fsm', methods=['GET'])
def show_fsm():
    machine.get_graph().draw('fsm.png', prog='dot', format='png')
    return send_file('fsm.png', mimetype='image/png')


if __name__ == '__main__':
    port = os.environ.get('PORT', 8000)
    app.run(host='0.0.0.0', port=port, debug=True)
