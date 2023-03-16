import glob
import pandas as pd

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage, ButtonsTemplate, MessageTemplateAction, CarouselTemplate, CarouselColumn, PostbackAction, MessageAction
)

from gen_msg import CGenMsg
gen_msg = CGenMsg()

app = Flask(__name__)

line_bot_api = LineBotApi('259KhHhK9JkcNBApp5AN49wK2f4mjHOSonztVEOlZ4qExdCwZrEhXJxvYjiee0T+adOuVDseVzZesGdKSopsxraMRjmY47XLaX0booeyplmG7WHgJ4zr8PE0/72Bq5GLWim3Nop+yAMKPAWVVO2IYgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('ccd99ccd0896fd6354b57eec2dad677f')

xlsm_name = None
data_frame = None


def check_and_select_xlsm():
    print("check_and_select_xlsm")

    # Check if .xlsm exists, ignore the .xlsm name start with ~
    xlsm_files = [f for f in glob.glob("*.xlsm") if not f.startswith('~')]
    # xlsm_files = glob.glob("*.xlsm")
    if len(xlsm_files) == 0:
        print("[Notice] .xlsm not found. Please put this .exe with .xlsm file(s).")
        input("Press [Enter] to continue.")
        sys.exit()
    elif len(xlsm_files) == 1:
        xlsm_name = xlsm_files[0]
        print('[Notice] Found single .xlsm. "{}" will be used.\n'.format(xlsm_name))
    else:
        # Select .xlsm
        print("STEP #1 Select .xlsm with Abbreviation")

        for i, item in enumerate(xlsm_files):
            print(f"{i + 1}: {item}")

        index_xlsm = input(">>> ")
        # check if user input is valid
        if index_xlsm == '' or int(index_xlsm) > len(xlsm_files):
            print("Invalid input. Program will exit.")
            sys.exit()

        xlsm_name = xlsm_files[int(index_xlsm) - 1]
        print("{} selected.".format(xlsm_name))

    return xlsm_name

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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


# declair a static variable and assign it to 0
my_step = 0
# global xlsm_name
xlsm_name = check_and_select_xlsm()
# global data_frame
data_frame = pd.read_excel(xlsm_name, usecols="A:I")

def similar(target, order, threshold=0.6):
    target_set = set(target)
    order_set = set(order)

    intersect = target_set & order_set
    return (len(intersect) / len(target_set)) >= threshold


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    global my_step
    global data_frame
    # switch case for state
    print("{}",my_step)

    # translate event.message.text to lower case, and remove space

    if event.message.text.lower().replace(" ", "") == "menu":
        line_bot_api.reply_message(
            event.reply_token,
            gen_msg.menu()
        )

    if my_step == 0:
        # if input is "吃啥?" or "eat what?"
        if similar(":eat_what", event.message.text): # or similar("eat what?", event.message.text):
            data_frame = pd.read_excel(xlsm_name, usecols="A:I")

            line_bot_api.reply_message(
                event.reply_token,
                gen_msg.num_people()
            )

            my_step = 1
    elif my_step == 1:
        # if user input is not a number between 1~10
        if not event.message.text.isdigit() or int(event.message.text) < 1 or int(event.message.text) > 10:

            message_list = [TextSendMessage(text="賣鬧!"), gen_msg.num_people()]
            line_bot_api.reply_message(
                event.reply_token,
                message_list
            )

        else:
            # filter data_frame by "人數"
            # global data_frame
            data_frame = data_frame[data_frame['人數'] >= int(event.message.text)]

            line_bot_api.reply_message(
                event.reply_token,
                gen_msg.duration()
            )

            my_step = 2
    elif my_step == 2:
        # if user input is not a number between 0.5~2
        if float(event.message.text) < 0 or float(event.message.text) > 2:
            message_list = [TextSendMessage(text="賣鬧!"), gen_msg.duration()]
            line_bot_api.reply_message(
                event.reply_token,
                message_list)
        else:
            # filter data_frame by "時間"
            # global data_frame
            # skip if user input is 0
            if float(event.message.text) != 0:
                data_frame = data_frame[data_frame['時長'] <= float(event.message.text)]

            line_bot_api.reply_message(event.reply_token, gen_msg.food_type())
            my_step = 3
    elif my_step == 3:
        # if user input is not a number between 1~8
        if not event.message.text.isdigit() or int(event.message.text) < 0 or int(event.message.text) > 9:

            message_list = [TextSendMessage(text="賣鬧!"), gen_msg.food_type()]
            line_bot_api.reply_message(event.reply_token, message_list)
        else:
            # filter data_frame by "類型"
            # global data_frame
            food = event.message.text
            if int(food) == 1:
                data_frame = data_frame[data_frame['類型'].str.contains("飯")]
            elif int(food) == 2:
                data_frame = data_frame[data_frame['類型'].str.contains("麵")]
            elif int(food) == 3:
                data_frame = data_frame[data_frame['類型'].str.contains("餃")]
            elif int(food) == 4:
                data_frame = data_frame[data_frame['類型'].str.contains("台式")]
            elif int(food) == 5:
                data_frame = data_frame[data_frame['類型'].str.contains("中式")]
            elif int(food) == 6:
                data_frame = data_frame[data_frame['類型'].str.contains("越式")]
            elif int(food) == 7:
                data_frame = data_frame[data_frame['類型'].str.contains("日式")]
            elif int(food) == 8:
                data_frame = data_frame[data_frame['類型'].str.contains("美式")]
            else:
                pass

            line_bot_api.reply_message(
                event.reply_token,
                gen_msg.location())
            my_step = 4
    elif my_step == 4:
        # if user input is not a number between 1~4
        if not event.message.text.isdigit() or int(event.message.text) < 0 or int(event.message.text) > 3:
            message_list = [TextSendMessage(text="賣鬧!"), gen_msg.location()]
            line_bot_api.reply_message(
                event.reply_token,
                message_list)
        else:
            # filter data_frame by "地點"
            # global data_frame
            place = event.message.text
            if int(place) == 1:
                data_frame = data_frame[data_frame['地點'].str.contains("南港")]
            # if input is 2, remove the rows except for the column "地點" is "南港車站" or "南港展覽館"
            elif int(place) == 2:
                data_frame = data_frame[data_frame['地點'].str.contains("南港|南港展覽館")]
            # if input is 3, remove the rows which column "地點" is "南港車站"
            elif int(place) == 3:
                data_frame = data_frame[~data_frame['地點'].str.contains("南港")]
            else:
                pass

            # if data_frame is empty
            if data_frame.empty:
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text="沒有符合的店家，請重新輸入！"))
                my_step = 0
                return

            # if data_frame is not empty

            message_list = [TextSendMessage(text="我找到了 {} 家店家，以下是我推薦的店家:".format(len(data_frame))), TextSendMessage(text=gen_msg.suggestions(data_frame)), gen_msg.random_choice()]
            # message_list.append(gen_msg.suggestions(data_frame))
            # message_list.append(gen_msg.random_choice())
            line_bot_api.reply_message(
                event.reply_token,
                message_list)

            my_step = 5

            # msg = "好的，我想一下！\n".format(event.message.text)
            # add the column "店名" of data_frame to msg, 每個店名占一行，並且靠左對齊, 並且把"連結"作為超連結加到店名上
            # msg += data_frame['店名'].to_string(index=False).replace(" ", "")
            # msg += gen_msg.suggestions(data_frame)
            # msg += "\n需要幫你選一個嗎? (y/n): "

            # line_bot_api.reply_message(
            #     event.reply_token,
            #     TextSendMessage(text=msg))

    elif my_step == 5:
        # if input is not "y" or "n"
        if event.message.text != "y" and event.message.text != "n":
            message_list = [TextSendMessage(text="賣鬧!"), gen_msg.random_choice()]
            line_bot_api.reply_message(
                event.reply_token,
                message_list)
        else:
            # if input is "y"
            if event.message.text == "y":
                # randomly select a row from data_frame
                # selected_row = data_frame.sample()
                # # add the column "店名" of selected_row to msg, 每個店名占一行，並且靠左對齊
                # msg = selected_row['店名'].to_string(index=False).replace(" ", "")
                message_list = [TextSendMessage(text=gen_msg.random_one(data_frame)), gen_msg.random_choice()]
                # msg += "\n需要再幫你選一個嗎? (y/n): "
                line_bot_api.reply_message(
                    event.reply_token,
                    message_list)
                my_step = 5
            # if input is "n"
            else:
                msg = "好的，祝你用餐愉快！"
                my_step = 0
                data_frame = pd.read_excel(xlsm_name, usecols="A:I")
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text=msg))

if __name__ == "__main__":
    app.run()