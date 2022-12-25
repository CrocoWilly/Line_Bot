from transitions.extensions import GraphMachine
from utils import send_text_message, send_button_message, send_image_message, send_image_carousel_message
import requests
from linebot.models import MessageTemplateAction
import pandas as pd

# global variable
korean_flag = False
japan_flag = False
taiwan_flag = False
hairstyle_flag = False
clothing_flag = False


class TocMachine(GraphMachine):

    ###############           TRANSITION          ###############

    # 畫FSM
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    ### 往前走的路 ###
    def is_going_to_fsm(self, event):
        text = event.message.text
        if text == 'fsm':
            return True
        return False

    def is_going_to_help(self, event):
        text = event.message.text
        if text == 'help':
            return True
        return False

    # user start
    def is_going_to_menu(self, event):
        text = event.message.text
        if text == 'start':
            return True
        return False

    def is_going_to_choose_type(self, event):
        global korean_flag, japan_flag, taiwan_flag
        text = event.message.text
        if text == '韓系風':
            korean_flag = True
            return True
        elif text == '日系風':
            japan_flag = True
            return True
        elif text == '8+9風':
            taiwan_flag = True
            return True
        return False

    def is_going_to_teach_or_example(self, event):
        global hairstyle_flag, clothing_flag
        text = event.message.text
        if text == '髮型':
            hairstyle_flag = True
            return True
        elif text == '穿搭':
            clothing_flag = True
            return True
        return False
    

    def is_going_to_teach(self, event):
        text = event.message.text
        if text == '風格指南':
            return True
        return False

    def is_going_to_example(self, event):
        text = event.message.text
        if text == '圖片範本':
            return True
        return False

    
    
    ### 往回走的路 ###
    def is_going_to_teach_or_example2(self, event):
        text = event.message.text
        if text == 'back':
            return True
        return False

    def is_going_to_menu2(self, event):
        text = event.message.text
        if text == '回主選單':    # 從teach_or_example state吃到"back"回到menu state
            return True
        return False

    def is_going_to_user(self, event):
        text = event.message.text
        if text == '回初始畫面':    # 在menu中點擊「回初始畫面」button
            return True
        return False
    

    
    ###############           STATE          ###############
    def on_enter_fsm(self, event):
        url = 'https://img.onl/VzTSfv'
        send_image_message(event.reply_token, url)
        self.go_back(event)


    def on_enter_help(self, event):
        text = '--- 如何使用穿搭怪客 ---\n1.當接收到圖片訊息後，輸入「back」即可回到上一頁。\n2.點擊選單中的按鈕，即可執行對應的操作。\n3.根據穿搭怪客給你的指示操作，就可以順利地學習唷!\n4.帶著一顆愉悅的心來體驗!\n\n--> 輸入「back」回到上一頁'
        send_text_message(event.reply_token, text)
        self.go_back(event)

    # 主線
    def on_enter_menu(self, event):
        global korean_flag, japan_flag, taiwan_flag, hairstyle_flag, clothing_flag
        # 初始化所有flag
        korean_flag = False
        japan_flag = False
        taiwan_flag = False
        hairstyle_flag = False
        clothing_flag = False

        # 設定Line bot UI
        title = '風格'
        text = '選擇你想了解的風格'
        url = 'https://hips.hearstapps.com/hmg-prod.s3.amazonaws.com/images/%E8%BB%8A%E9%8A%80%E5%84%AA-1665138646.jpg?crop=0.503xw:1.00xh;0,0&resize=640:*'
        option1 = MessageTemplateAction(label = '韓系風', text = '韓系風')
        option2 = MessageTemplateAction(label = '日系風', text = '日系風')
        option3 = MessageTemplateAction(label = '8+9風', text = '8+9風')
        option4 = MessageTemplateAction(label = '回初始畫面', text = '回初始畫面')
        buttons = [option1, option2, option3, option4]
        send_button_message(event.reply_token, title, text, buttons, url)


    def on_enter_choose_type(self, event):
        # 設定Line bot UI
        if(korean_flag == True):
            title = '韓系風'
            url = 'https://pica.zhimg.com/v2-d7eb61fc2aa90e29b0c16869b7ca93f0_b.jpeg'
        elif(japan_flag == True):
            title = '日系風'
            url = 'https://www.xiziwang.net/uploads/allimg/200511/725_200511215049_1.jpg'
        elif(taiwan_flag == True):
            title = '8+9風'
            url = 'https://i0.wp.com/imgur.dcard.tw/tKZeMy4.jpg'
        
        text = '選擇髮型或穿搭'
        option1 = MessageTemplateAction(label = '髮型', text = '髮型')
        option2 = MessageTemplateAction(label = '穿搭', text = '穿搭')
        buttons = [option1, option2]
        send_button_message(event.reply_token, title, text, buttons, url)


    def on_enter_teach_or_example(self, event):
        global korean_flag, japan_flag, taiwan_flag, hairstyle_flag, clothing_flag
        # 設定Line bot UI
        title = ''
        url = ''

        if(korean_flag == True):    
            if(hairstyle_flag == True):
                title = '髮型風格指南'
                url = 'https://asa-alliance.com/wp-content/uploads/2021/04/136384389_438813660635860_6639791291143614174_n-1-1024x1024.jpg'
            elif(clothing_flag == True):
                title = '穿搭風格指南'
                url = 'https://images.dappei.com/uploads/article_image/image/110170/medium_4d081ef11eecc581.jpg'

        elif(japan_flag == True):
            if(hairstyle_flag == True):
                title = '髮型風格指南'
                url = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS6RJY7vIgK5ybt2kUsYEdyhSUjJi0tNuoA_w&usqp=CAU'
            elif(clothing_flag == True):
                title = '穿搭風格指南'
                url = 'https://cdn2.ettoday.net/images/5843/5843121.jpg'

        elif(taiwan_flag == True):
            if(hairstyle_flag == True):
                title = '髮型風格指南'
                url = 'https://obs.line-scdn.net/0h3CApm1MvbGx8CUbYtxsTO0ZfbwNPZX9vGD89bz9nMlgDbCloR2onWVBZM15WaysyEjokAlgJd10BOHxuFW0n/w644'
            elif(clothing_flag == True):
                title = '穿搭風格指南'
                url = 'https://i.imgur.com/f9zLBNK.jpg'


        text = '選擇風格指南或圖片範本'
        option1 = MessageTemplateAction(label = '風格指南', text = '風格指南')
        option2 = MessageTemplateAction(label = '圖片範本', text = '圖片範本')
        option3 = MessageTemplateAction(label = '回主選單', text = '回主選單')
        buttons = [option1, option2, option3]
        send_button_message(event.reply_token, title, text, buttons, url)


    def on_enter_teach(self, event):
        global korean_flag, japan_flag, taiwan_flag, hairstyle_flag, clothing_flag
        text = ''

        if(korean_flag == True):    
            if(hairstyle_flag == True):
                text = '風格指南:\n\t一、最近流行的髮型:\n\t\t1.蘑菇頭\n\t\t2.中分逗號頭(或六四分、三七分)\n\t\t3.栗子頭\n\t二、韓系髮型通則:\n\t\t1.瀏海要在眉毛跟眼睛之間\n\t\t2.髮型要有一體感，不能分層\n\n'
                text += '--> 輸入「back」回到上一頁'
            elif(clothing_flag == True):
                text = '風格指南:\n\t一、上衣:\n\t\t1.小高領衛衣\n\t\t2.落肩款大學T、帽T\n\t\t3.微落肩襯衫或polo衫\n\t二、褲子:\n\t\t1.休閒西裝褲(落地、九分)\n\t\t2.寬版棉褲\n\t\t3.冰絲垂墜感長褲\n\t三、穿搭通則:\n\t\t要就很挺拔、不然就很慵懶\n\n'
                text += '--> 輸入「back」回到上一頁'

        elif(japan_flag == True):
            if(hairstyle_flag == True):
                text = '風格指南:\n\t一、最近流行的髮型:\n\t\t1.中長度微捲中分\n\t\t2.自然感螺絲燙\n\t\t3.螺旋燙\n\t\t4.鬆軟扭紋燙\n\t二、日系髮型通則:\n\t\t1.瀏海長度在眼眉之間或是過眼睛\n\t\t2.髮型要有蓬鬆感、凌亂感，不能太貼\n\n'
                text += '--> 輸入「back」回到上一頁'
            elif(clothing_flag == True):
                text = '風格指南:\n\t一、上衣:\n\t\t1.寬版素色襯衫、針織衫、大學T、帽T\n\t\t2.機能外套\n\t\t3.針織背心\n\t二、褲子:\n\t\t1.八、九分不修身直筒寬褲\n\t\t2.寬版落地西裝褲或牛仔褲\n\t\t3.氣球褲\n\t三、穿搭通則:\n\t\t就是寬、就是素\n\n'
                text += '--> 輸入「back」回到上一頁'

        elif(taiwan_flag == True):
            if(hairstyle_flag == True):
                text = '風格指南:\n\t一、流行的髮型:\n\t\t1.刷子頭\n\t\t2.蛋頭\n\t\t3.寸頭、平頭\n\t二、8+9髮型通則:\n\t\t1.髮型要分層，旁邊頭髮剃越光越台\n\t\t2.刷子頭瀏海一定要很齊\n\n'
                text += '--> 輸入「back」回到上一頁'
            elif(clothing_flag == True):
                text = '風格指南:\n\t一、上衣:\n\t\t1.黑色有牌短T e.g.鬼洗、CK、EA7、GUCCI\n\t\t2.有龍、蛇圖案的襯衫或合身花襯衫\n\t\t3.吊嘎或直接不穿上衣，為了露半甲\n\t二、褲子:\n\t\t1.緊身牛仔褲(通常會配GUCCI皮帶)\n\t\t2.adidas三線褲\n\t\t3.其他有牌運動褲\n\t三、鞋子:\n\t\t1.假的Yeezy 350\n\t\t2.夜市買的懶人鞋、拖鞋\n\t\t3.跟風買的流行球鞋 e.g.Vans經典款\n\t四、穿搭通則:\n\t\t就是緊、就是要有牌(管他真還假)\n\n'
                text += '--> 輸入「back」回到上一頁'
        
        send_text_message(event.reply_token, text)


    def on_enter_example(self, event):
        global korean_flag, japan_flag, taiwan_flag, hairstyle_flag, clothing_flag

        if(korean_flag == True):    
            if(hairstyle_flag == True):
                url1 = "https://media-proc-wowm.bastillepost.com/wp-content/uploads/hongkong/2021/10/20211006_en_%E9%87%91%E7%A7%80%E8%B3%A2_5.jpg"
                url2 = "https://api.harpersbazaar.com.hk/var/site/storage/images/_aliases/img_748_w/celebrity/men-hairstyle-2021/2021-1/2619977-1-chi-HK/2021-1.jpg"
                url3 = "https://www.faxingzhan.com/uploads/190527/52_183254_4.jpg"
                url4 = "https://beauty-upgrade.tw/wp-content/uploads/2019/03/%E9%80%97%E8%99%9F%E7%80%8F%E6%B5%B712.jpg"
                url5 = "https://hips.hearstapps.com/hmg-prod.s3.amazonaws.com/images/c2-1650622325.jpg?crop=0.491xw:0.980xh;0.00489xw,0.0195xh&resize=640:*"

                labels = ["蘑菇頭", "中分逗號頭", "六四分逗號頭", "三七分逗號頭", "栗子頭"]
                text = ["蘑菇頭", "中分逗號頭", "六四分逗號頭", "三七分逗號頭", "栗子頭"]
                image_links = [url1, url2, url3, url4, url5]

            elif(clothing_flag == True):
                url1 = "https://images.dappei.com/uploads/article_image/image/110175/medium_e04397b49162ffe7.jpg"
                url2 = "https://i.pinimg.com/564x/e3/18/b1/e318b18c02007b22c511d14a3de7db20.jpg"
                url3 = "https://cf.shopee.tw/file/5e00189b213438910d7f8751e30c1ea0"
                url4 = "https://i.pinimg.com/564x/0b/50/b1/0b50b126663a00332da3edad04d24a98.jpg"
                url5 = "https://cf.shopee.tw/file/5e10039a6302f16d746a440185f3e75e"
                url6 = "https://cf.shopee.tw/file/da8162b4ee84742c064d710bb5c672ae"

                labels = ["polo衫 休閒西裝褲", "微落肩襯衫 休閒西裝褲", "小高領衛衣", "落肩款大學T 落地西裝褲", "微寬棉褲", "冰絲褲"]
                text = ["polo衫 休閒西裝褲", "微落肩襯衫 休閒西裝褲", "小高領衛衣", "落肩款大學T 落地西裝褲", "微寬棉褲", "冰絲褲"]
                image_links = [url1, url2, url3, url4, url5, url6]

        elif(japan_flag == True):
            if(hairstyle_flag == True):
                url1 = 'https://www.faxingzhan.com/uploads/210621/77_144344_5.png'
                url2 = 'https://asa-alliance.com/wp-content/uploads/2021/03/3-1024x1024.jpg'
                url3 = 'https://asa-alliance.com/wp-content/uploads/2021/03/5-1024x1024.jpg'
                url4 = 'https://beauty-upgrade.tw/wp-content/uploads/2019/06/%E7%94%B7%E7%94%9F%E9%AB%AE%E5%9E%8B2.jpg'

                labels = ["中長度微捲中分", "自然感螺絲燙", "螺旋燙", "鬆軟扭紋燙"]
                text = ["中長度微捲中分", "自然感螺絲燙", "螺旋燙", "鬆軟扭紋燙"]
                image_links = [url1, url2, url3, url4]
                
            elif(clothing_flag == True):
                url1 = 'https://s.yimg.com/ny/api/res/1.2/d3qkX.VnO.mim.DnlAtq9Q--/YXBwaWQ9aGlnaGxhbmRlcjt3PTY0MDtoPTcxOA--/https://s.yimg.com/os/creatr-uploaded-images/2021-07/988362b0-e486-11eb-bfac-0d9a129a5bf8'
                url2 = 'https://assets.juksy.com/files/articles/107257/800x_100_w-61a12ebebc33d.jpg'
                url3 = 'https://blog.plain-me.com/wp-content/uploads/2019/06/20190611_widepants-blog000-16.jpg'
                url4 = 'https://ct.yimg.com/xd/api/res/1.2/caDyNzT61FQfaYUeTME.pw--/YXBwaWQ9eXR3YXVjdGlvbnNlcnZpY2U7aD00MDA7cT04NTtyb3RhdGU9YXV0bzt3PTQwMA--/https://s.yimg.com/ob/image/44ac4a5a-f1de-4784-bf90-e585dbb91b0a.jpg'
                url5 = 'https://images.dappei.com/uploads/article_image/image/79465/medium_8166839fbb660a8a.jpg'
                url6 = 'https://assets.juksy.com/files/articles/105394/800x_100_w-61a2b8f960ebc.jpg'
                
                labels = ["寬版襯衫 素T 寬褲", "寬版襯衫 寬落地西裝褲", "寬版素針織衫 九分直筒褲", "寬版落地牛仔褲", "針織背心 寬版襯衫 寬褲", "氣球褲"]
                text = ["寬版襯衫 素T 寬褲", "寬版襯衫 寬落地西裝褲", "寬版素針織衫 九分直筒褲", "寬版落地牛仔褲", "針織背心 寬版襯衫 寬褲", "氣球褲"]
                image_links = [url1, url2, url3, url4, url5, url6]

        elif(taiwan_flag == True):
            if(hairstyle_flag == True):
                url1 = 'https://scontent.ftpe7-1.fna.fbcdn.net/v/t39.30808-6/279952520_5682110305137019_1488794826106543562_n.jpg?_nc_cat=106&ccb=1-7&_nc_sid=a26aad&_nc_ohc=maWfk2ZW5jkAX-RwDvK&_nc_ht=scontent.ftpe7-1.fna&oh=00_AfBFsB0apS3vqkJYTX4iYPaTpq7cVReAb6Q2zdW3-6V83w&oe=63ADEC54'
                url2 = 'https://i.ytimg.com/vi/zqp0vvoU5Yk/maxresdefault.jpg'
                url3 = 'https://cdn.style-map.com/post/photo/normal/516346.jpg'
                
                labels = ["刷子頭", "蛋頭", "寸頭"]
                text = ["刷子頭", "蛋頭", "寸頭"]
                image_links = [url1, url2, url3]
            
            elif(clothing_flag == True):
                url1 = 'https://cf.shopee.tw/file/e9a8fd42c1f41184c5de82829c270293'
                url2 = 'https://cf.shopee.tw/file/594a2f06669a05e1cad372d9c716be2c'
                url3 = 'https://cf.shopee.tw/file/f951473b749ef376b43414c4b84880a7'
                url4 = 'https://cf.shopee.tw/file/b6801ec8b14a46d78c95d0989f21b588'
                url5 = 'https://plusheart.com.tw/wp-content/uploads/2019/03/zzzzzzzzzzzzzzzzzzzzzzzzzzz26-1.jpg'

                labels = ["黑色有牌短T", "合身花襯衫", "三線褲 假350", "緊身牛仔褲", "GUCCI皮帶"]
                text = ["黑色有牌短T", "合身花襯衫", "三線褲 假350", "緊身牛仔褲", "GUCCI皮帶"]
                image_links = [url1, url2, url3, url4, url5]


        send_image_carousel_message(event.reply_token, labels, text, image_links)
        #self.go_back(event)