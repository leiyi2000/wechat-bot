<div align="center">
<img src="https://raw.githubusercontent.com/leiyi2000/wechat-bot/main/docs/resources/image/logo.jpeg" style="width:200px; height:200px; border-radius:50%;"/>
</div>

![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/leiyi2000/wechat-bot/main.yml)

# wechat-bot
这是一个关于微信BOT
***
此项目基于 [wechatbot-webhook](https://github.com/danni-cool/wechatbot-webhook)+FastAPI+tortoise-orm开发，以 sqlite 作为数据库的微信BOT
***


### 功能

<details>
<summary>色图</summary>
<table>
  <tr>
    <th>指令</th>
    <th>结果</th>
  </tr>
  <tr>
    <td>st</td>
    <td><img src="https://raw.githubusercontent.com/leiyi2000/wechat-bot/main/docs/resources/image/st.webp" style="width:200px; height:100px;"></td>
  </tr>
    <tr>
    <td>sts</td>
    <td>保存最近发的st到alist(如果开启了alist)</td>
  </tr>
</table>
</details>

<details>
<summary>喜加一</summary>
<table>
  <tr>
    <th>指令</th>
    <th>结果</th>
  </tr>
  <tr>
    <td>喜加一</td>
    <td><p>    <br>游戏:	《Circus Electrique》
    <br>描述:	《Circus Electrique》融入了多种元素，包括故事驱动的角色扮演、战术、马戏团管理，极具吸引力。就在普普通通的伦敦市民神秘地变为冷酷无情的杀手之际，只有 Circus <br>Electrique 天赋异禀的艺人们拥有拯救这座城市所需的能力。 
    <br>价格:	0
    <br>时间:	2024-05-09 ~ 2024-05-16
    <br>领取:	https://store.epicgames.com/zh-CN/p/circus-electrique</p></td>
  </tr>
</table>
</details>

<details>
<summary>查天气</summary>
<table>
  <tr>
    <th>指令</th>
    <th>结果</th>
  </tr>
  <tr>
    <td>天气&nbsp;成都</td>
    <td><img src="https://raw.githubusercontent.com/leiyi2000/wechat-bot/main/docs/resources/image/weather.jpg"></td>
  </tr>
</table>
</details>

<details>
<summary>KFC文案</summary>
<table>
  <tr>
    <th>指令</th>
    <th>结果</th>
  </tr>
  <tr>
    <td><p>kfc</p></td>
    <td><p>CRAZY-THURSDAY，周期性发作，需要一种叫V- ME 50的特殊药物靶向治疗</p></td>
  </tr>
</table>
</details>

<details>
<summary>leetcode每日一题</summary>
<table>
  <tr>
    <th>指令</th>
    <th>结果</th>
  </tr>
  <tr>
    <td><p>每日一题</p></td>
    <td><img src="https://raw.githubusercontent.com/leiyi2000/wechat-bot/main/docs/resources/image/leetcode.png"></td>
  </tr>
</table>
</details>


### 部署

**启动**

    git clone git@github.com:leiyi2000/wechat-bot.git && cd wechat-bot && docker compose up

### 配置
  
  **天气密钥**

      curl -X 'POST' \
      'http://127.0.0.1:3002/config' \
      -H 'accept: application/json' \
      -H 'Content-Type: application/json' \
      -d '{
        "key": "weather",
        "value": "高德的天气密钥"
      }'

  **ALIST-(配置此项可存储图片)**

      curl -X 'POST' \
        'http://127.0.0.1:8000/config' \
        -H 'accept: application/json' \
        -H 'Content-Type: application/json' \
        -d '{
        "key": "alist",
        "value": "{\"api\":\"http://公网:xxxx\",\"api_key\":\"AList接口密钥\",\"path\":\"AList上的保存路径\"}"
      }'
