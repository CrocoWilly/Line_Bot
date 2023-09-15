# TOC Project 2022 - LineBot 穿搭教科書
## Introduction
穿搭怪客是一個觀察各種髮型、穿搭風格已久的機器人，他會以他最熟悉的三個風格:"**韓系風**", "**日系風**"以及"**8+9系風**"，為使用者進行"**髮型**"與"**穿搭**"上的分析，提供不同類型的**教學指南**並提供**範例圖片**，讓想了解這些風格的人能夠有基本的認識。


## 操作說明

### 初始畫面
首先，使用者需要發送任意訊息，來觸發穿搭怪客發送初始訊息。
![其他作品集_LineBot1](https://github.com/CrocoWilly/Line_Bot/assets/83399014/4231f325-ef47-473e-acf5-2c3863ef7294)

### 輸入「help」，查看如何使用穿搭怪客
在穿搭怪客發送help的訊息後，輸入「back」，穿搭怪客會再次發送初始訊息。
![其他作品集_LineBot2](https://github.com/CrocoWilly/Line_Bot/assets/83399014/b7a3e757-484a-471f-92d4-1b01dae738ba)


### 輸入「fsm」，查看fsm圖
在穿搭怪客發送fsm圖後，輸入「back」，穿搭怪客會再次發送初始訊息。
![其他作品集_LineBot3](https://github.com/CrocoWilly/Line_Bot/assets/83399014/75294bb0-4f79-4bd7-9723-74c6b7d84dbf)



### 輸入「start」，進入主選單
輸入「start」後，進入正式髮型、穿搭教學。
![其他作品集_LineBot4](https://github.com/CrocoWilly/Line_Bot/assets/83399014/595090b2-824b-47e4-9228-6a2e9fcbc072)



### 共三個風格，以韓系風做舉例說明
點選主選單中的「韓系風」按鈕後，會跳出另一個選單，
使用者可以選擇了解「髮型」或「穿搭」。
![其他作品集_LineBot5](https://github.com/CrocoWilly/Line_Bot/assets/83399014/5ead5967-965e-4e31-a059-7b0b0019a97b)



#### 若在"韓系風選單"中點選「髮型」，會出現下面的"髮型風格指南"選單
![其他作品集_LineBot6_8](https://github.com/CrocoWilly/Line_Bot/assets/83399014/e2e4c509-7f66-42cd-a746-9172b21b8bd3)



#### 若在"韓系風選單"中點選「穿搭」，則會出現下面的"穿搭風格指南"選單
![其他作品集_LineBot7](https://github.com/CrocoWilly/Line_Bot/assets/83399014/9d2f5c75-b7f9-4740-a65e-5080e196d018)


------------------------------------------------------------------------

### 以"韓系風選單"中點選「髮型」做舉例:
![其他作品集_LineBot6_8](https://github.com/CrocoWilly/Line_Bot/assets/83399014/f76a1a37-7159-4be6-b277-6312d1585f45)


#### 點選「風格指南」，穿搭怪客會傳送韓系髮型的風格指南
輸入「back」，即可回到上一步驟的選單

![其他作品集_LineBot9](https://github.com/CrocoWilly/Line_Bot/assets/83399014/2d9d4854-f5dd-41ca-b1de-f4012c9457f8)

![其他作品集_LineBot10](https://github.com/CrocoWilly/Line_Bot/assets/83399014/ccac5122-c834-41d3-aa3c-18735e65de09)



#### 點選「圖片範本」，穿搭怪客會傳送韓系髮型的圖片範本
輸入「back」，即可回到上一步驟的選單

![其他作品集_LineBot11](https://github.com/CrocoWilly/Line_Bot/assets/83399014/d36e5e21-eeed-4136-8a4f-c359aac09335)

![其他作品集_LineBot12](https://github.com/CrocoWilly/Line_Bot/assets/83399014/84cde1a3-a583-4196-9e9a-e8f96afbf6c7)


#### 點選「回主選單」，將會跳到"選擇風格的主選單"
![其他作品集_LineBot12](https://github.com/CrocoWilly/Line_Bot/assets/83399014/e85b2a69-f13f-4d33-9248-e97281ad2ab0)



### 韓系風的「穿搭」與韓系風「髮型」的操作雷同，而其他風格(日系風、8+9風)與韓系風的操作類似。
### 以上就是穿搭怪客的操作說明。



## FSM圖
![](https://i.imgur.com/w89wgks.png)



### 設計想法
我把三個不同的風格寫成同一個架構。也就是說，若操作行為相同，不管是何種風格，他們在state的探訪都會是相同路徑。而區分不同的風格的方法是利用讀「button text」，並設立不同的flag來判斷屬於何種風格、是髮型或是穿搭。

### Usage
`user` state: initial state

每次從`user` state "advance"到`help` state或`fsm` state，穿搭怪客都會先產生對應的回應，再"go_back"回到`user` state。而在`help` state的訊息中，穿搭怪客會提示使用者需要輸入「back」，才能讓使用者回到上一步。


* user
	* Input: "help"
		* Reply: "產生help的文字訊息"
	* Input: "fsm"
		* Reply: "產生FSM圖"
    * Input: "start"
        * Reply: "產生主選單menu"
         
* menu 
    * Input: "按選單中的按鈕「韓系風」"
        * Reply: "產生韓系風的選單"
    * Input: "按選單中的按鈕「日系風」"
        * Reply: "產生日系風的選單"
    * Input: "按選單中的按鈕「8+9風」"
        * Reply: "產生8+9風的選單"
    * Input: "按選單中的按鈕「回初始畫面」"
        * Reply: "產生初始畫面的訊息"
        
* choose_type
    * Input: "按選單中的按鈕「髮型」"
        * Reply: "產生「髮型風格指南」選單"
    * Input: "按選單中的按鈕「穿搭」"
        * Reply: "產生「穿搭風格指南」選單"
        
* teach_or_example
    * Input: "按選單中的按鈕「風格指南」"
        * Reply: "產生該風格的教學指南"  e.g.韓系髮型教學指南
    * Input: "按選單中的按鈕「圖片範本」"
        * Reply: "產生該風格的圖片範本"  e.g.韓系髮型圖片範本
    * Input: "按選單中的按鈕「回主選單」"
        * Reply: "產生主選單menu"
        
* teach
    * Input: "back"
        * Reply: "回到上一步驟的選單" e.g.「髮型風格指南」選單

* example
    * Input: "back"
        * Reply: "回到上一步驟的選單" e.g.「髮型風格指南」選單

## Bonus 
- 使用 **Line API**
- 使用不少**image**


## Reference
[Pipenv](https://medium.com/@chihsuan/pipenv-更簡單-更快速的-python-套件管理工具-135a47e504f4) ❤️ [@chihsuan](https://github.com/chihsuan)

[TOC-Project-2019](https://github.com/winonecheng/TOC-Project-2019) ❤️ [@winonecheng](https://github.com/winonecheng)

Flask Architecture ❤️ [@Sirius207](https://github.com/Sirius207)

[Line line-bot-sdk-python](https://github.com/line/line-bot-sdk-python/tree/master/examples/flask-echo)
