#架設伺服器: flask, django
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('Umf+M1rnlT7e7NfMsU+LQPxGnYpkFgEdLr3ru/eLLqk10dYKsomnBMoqYy2jTJyT3NUuh9xdjjvFQ18lhRibjf0VaddEA4/OqdARwZkEL3+YxKGYEg0wxfIN1vT/qoHrNdlty0TN5gUTRBHBZKuKwAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('13fb220cc4b0adc948d81f8c9ef15ec1')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    r = '抱歉,天業沒有教我回復這個問題'
    
    if msg in [hi, Hi, 嗨]:
        r = '嗨'
    elif msg == '你吃飯了嗎':
        r = '還沒,我是機器人,不用吃!'
    elif '劉士華' in msg:
        r = '劉士華背完將進酒了嗎?'
    elif '設計者' in msg:
        r = '天業是我的設計者!'
    #elif [設計者, 天業, 誰設計] in msg:
       
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text= r))


if __name__ == "__main__":
    app.run()