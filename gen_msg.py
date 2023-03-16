from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage, ButtonsTemplate, MessageTemplateAction, CarouselTemplate, CarouselColumn, PostbackAction, MessageAction
)

import pandas as pd

#------------------------------------------------------------------------------------
#
# class CMsgGen:
# FUNCTION：
#
# DATA MEMBER:
#    path_from: source of preset folder
#    path_to: destination of preset folder
#
# MEMBER FUNCTION:
#    __init__()
#        FUNCTION： Constructor，defince data members
#        IN path_from: source of preset folder
#             path_to: destination of preset folder
#
#    __del__()
#        FUNCTION： Destructor
#
#    _copy_files()
#        FUNCTION： 遍歷所有path_from下的檔案，將相關檔案複制到path_to (*ctc_blob*.bin, *peq_ui_control*.bin, *gpeq_mode*.bin, copy *mode1*.bin to *mode7*.bin)
#        IN (無)
#        RETURN None
#
#    run()
#        FUNCTION： 遍歷所有path_from下的檔案，將相關檔案複制到path_to
#        IN (無)
#        RETURN None
#
#------------------------------------------------------------------------------------
class CGenMsg:

    # ------------------------------------------------------------------------------------
    #    __init__()
    #        FUNCTION： constructor，define data members, generate input and output folder if doesn't exist
    #        IN: None
    #        RETURN: None
    # ------------------------------------------------------------------------------------
    def __init__(self):
        print("constructor CMsgGen")

    # ------------------------------------------------------------------------------------
    #    __del__()
    #        FUNCTION： Destructor
    # ------------------------------------------------------------------------------------
    def __del__(self):
        print("destructor CMsgGen")

    def menu(self):
        print("menu")
        return TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                title='Menu',
                text='Please select',
                actions=[
                    MessageTemplateAction(
                        label='吃啥?',
                        text=':eat_what'
                    ),
                    MessageTemplateAction(
                        label='聊啥?',
                        text=':summarize'
                    )
                ]
            )
        )

    def num_people(self):
        print("num_people")
        return TextSendMessage(text="幾人 (1~10): ")

    def duration(self):
        print("duration")
        return TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                title='吃多久?',
                text=' ',
                actions=[
                    MessageTemplateAction(
                        label='隨便',
                        text='0'
                    ),
                    MessageTemplateAction(
                        label='30分鐘',
                        text='0.5'
                    ),
                    MessageTemplateAction(
                        label='1小時',
                        text='1'
                    ),
                    MessageTemplateAction(
                        label='1.5小時',
                        text='1.5'
                    )
                ]
            )
        )

    def food_type(self):
        print("food_type")
        return TemplateSendMessage(
            alt_text='Carousel template',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        title='想吃啥?',
                        text=' ',
                        actions=[
                            # PostbackAction(label='Buy', data='action=buy&itemid=1'),
                            MessageAction(label='隨便', text='0'),
                            MessageAction(label='飯', text='1'),
                            MessageAction(label='麵', text='2')
                        ]
                    ),
                    CarouselColumn(
                        title=' ',
                        text=' ',
                        actions=[
                            # PostbackAction(label='Buy', data='action=buy&itemid=2'),
                            MessageAction(label='餃子', text='3'),
                            MessageAction(label='台式', text='4'),
                            MessageAction(label='中式', text='5')
                        ]
                    ),
                    CarouselColumn(
                        title=' ',
                        text=' ',
                        actions=[
                            # PostbackAction(label='Buy', data='action=buy&itemid=2'),
                            MessageAction(label='越式', text='6'),
                            MessageAction(label='日式', text='7'),
                            MessageAction(label='美式', text='8')
                        ]
                    )
                ]
            )
        )

    def location(self):
        print("location")
        return TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                title='去哪吃?',
                text=' ',
                actions=[
                    MessageTemplateAction(
                        label='隨便',
                        text='0'
                    ),
                    MessageTemplateAction(
                        label='附近',
                        text='1'
                    ),
                    MessageTemplateAction(
                        label='散步',
                        text='2'
                    ),
                    MessageTemplateAction(
                        label='坐捷運',
                        text='3'
                    )
                ]
            )
        )

    def suggestions(self, data_frame):
        print("suggestions")
        # 算出總共有幾個'地點'
        # print("地點個數： ", data_frame['地點'].nunique())
        # 列出有哪幾種'地點'
        # print("地點： ", data_frame['地點'].unique())
        location = data_frame['地點'].unique()
        message = ""
        # 列出每個location的店名
        for i in range(len(location)):
            print("[", location[i], "]\n", data_frame.loc[data_frame['地點'] == location[i], '店名'].to_string(index=False).replace(" ", ""))
            message += "[" + location[i] + "]\n" + data_frame.loc[data_frame['地點'] == location[i], '店名'].to_string(index=False).replace(" ", "") + "\n\n"

        # return data_frame['店名'].to_string(index=False).replace(" ", "")
        return message

    def random_choice(self):
        print("random_choice")
        return TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                title='隨便選一個?',
                text=' ',
                actions=[
                    MessageTemplateAction(
                        label='好的',
                        text='y'
                    ),
                    MessageTemplateAction(
                        label='不用',
                        text='n'
                    )
                ]
            )
        )

    def random_one(self, data_frame):
        print("random_one")
        selected_row = data_frame.sample()

        message = selected_row['店名'].to_string(index=False).replace(" ", "") + "\n" + "https://www.google.com/maps/search/?api=1&query=" + selected_row['店名'].to_string(index=False).replace(" ", "") + "\n"
        # print(selected_row['link'])
        print(message)
        return message

