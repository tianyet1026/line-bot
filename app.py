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
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()