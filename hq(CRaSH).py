import discord
import webbrowser
from termcolor import colored
import datetime
import logging
import os
#import Google_Search
import time
from datetime import datetime
from time import sleep
from pytz import timezone
from lomond import WebSocket
from unidecode import unidecode
import colorama
import requests
import json
import re
from bs4 import BeautifulSoup
from dhooks import Webhook, Embed
import aniso8601
#import keep_alive
#keep_alive.keep_alive()

#RAVE™
webhook_url="https://discordapp.com/api/webhooks/931117026020319232/O1rATKh2gaL3Ehz2AtneHK3GYhGQ_5k5ne7muArflMz6d_t9UD8YoOWVyak61N82wNsp"
#ELITE OP
webhook = "https://discordapp.com/api/webhooks/933226558116724796/ejiTwUnGZe_-epIpqahactzwTtgiYLjUka7SrzCPDnu9THl4tCb8nxfwCfJ4r-yQZVHA"
#VENOM
we="https://discord.com/api/webhooks/829390738202034257/tLqaG4kGD8-g-HeT7YeJucr4AcKZfx6X-2IE5cZXiWugbvdoW8QFzkKS5lUko2jBpDSk"
#EMPTY
web="https://discord.com/api/webhooks/829773820143206420/Qr9qD-_kXYtKhitTQdqV5VbaFmAep8xPb6zqFWFJZNYKQWQ5YVlOkcH7aUPRGA1Iw-Bl"

try:
    hook = Webhook(webhook_url)
except:
    print("RAVE Invalid WebHook Url!")

try:
    hook3 = Webhook(web)
except:
    print("ELITE Invalid WebHook Url!")

try:
    hook2 = Webhook(webhook)
except:
    print("VENOM Invalid WebHook Url!")

try:
    hq = Webhook(we)
except:
    print("EMPTY Invalid WebHook Url!")
    

def show_not_on():
    colorama.init()
    # Set up logging
    logging.basicConfig(filename="data.log", level=logging.INFO, filemode="w")

    # Read in bearer token and user ID
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "BTOKEN.txt"), "r") as conn_settings:
        settings = conn_settings.read().splitlines()
        settings = [line for line in settings if line != "" and line != " "]

        try:
            BEARER_TOKEN = settings[0].split("=")[1]
        except IndexError as e:
            logging.fatal(f"Settings read error: {settings}")
            raise e

    print("getting")
    main_url = f"https://api-quiz.hype.space/shows/now?type="
    headers = {"Authorization": f"Bearer {BEARER_TOKEN}",
               "x-hq-client": "Android/1.3.0"}
    # "x-hq-stk": "MQ==",
    # "Connection": "Keep-Alive",
    # "User-Agent": "okhttp/3.8.0"}

    try:
        response_data = requests.get(main_url).json()
        print(response_data)
    except:
        print("Server response not JSON, retrying...")
        time.sleep(1)

    logging.info(response_data)

    if "broadcast" not in response_data or response_data["broadcast"] is None:
        if "error" in response_data and response_data["error"] == "Auth not valid":
            raise RuntimeError("Connection settings invalid")
        else:
            print("Show not on.")
            tim = (response_data["nextShowTime"])
            tm = aniso8601.parse_datetime(tim)
            x =  tm.strftime("%H:%M:%S [%d/%m/%Y] ")
            x_ind = tm.astimezone(timezone("Asia/Kolkata"))
            x_in = x_ind.strftime("%H:%M:%S [%d/%m/%Y] ")
    
            prize = (response_data["nextShowPrize"])
            time.sleep(5)
            print(x_in)
            print(prize)
            embed = Embed(title=f"<:light:877755481857355816> HQ Trivia", description=f"**Next HQ Time In India🇮🇳 :**\n**{x_in}**", color=0x00FF00)
            embed.add_field(name="Next Show Prize", value=f"**{prize}**",inline=True)
            embed.set_image(url="https://cdn.discordapp.com/attachments/649457795875209265/672845602824126494/Nitro_2.gif")
            embed.set_thumbnail(url="https://media.discordapp.net/attachments/931116321419194368/932667794623967243/200w_1.gif")
            embed.set_footer(text="Hype Google | Devloped by Prayas", icon_url="https://cdn.discordapp.com/attachments/578379566544846901/630400208265805835/401ec468afa82a2937b8ad3a4e811463.jpg")
            hook.send(content="**Connected To HQ Socket Buddy 😘!!**",embed=embed)
            print('Upcoming info sent successfully')
            #hq.send(f"**Hq Google Ready**")
            #hook2.send(content="**Connected To HQ Socket Buddy 😘!!**",embed=embed)
            



def show_active():
    main_url = 'https://api-quiz.hype.space/shows/now'
    response_data = requests.get(main_url).json()
    return response_data['active']


def get_socket_url():
    main_url = 'https://api-quiz.hype.space/shows/now'
    response_data = requests.get(main_url).json()

    socket_url = response_data['broadcast']['socketUrl'].replace('https', 'wss')
    return socket_url


def connect_websocket(socket_url, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}",
               "x-hq-client": "iPhone8,2"}


    websocket = WebSocket(socket_url)

    for header, value in headers.items():
        websocket.add_header(str.encode(header), str.encode(value))

    for msg in websocket.connect(ping_rate=5):
        if msg.name == "text":
            message = msg.text
            message = re.sub(r"[\x00-\x1f\x7f-\x9f]", "", message)
            message_data = json.loads(message)
            print(message_data)

            if message_data['type'] == 'question':
                question = message_data['question']
                qcnt = message_data['questionNumber']
                Fullcnt = message_data['questionCount']

                print(f"\nQuestion number {qcnt} out of {Fullcnt}\n{question}")
                answers = [unidecode(ans["text"]) for ans in message_data["answers"]]
                print(f"\n{answers[0]}\n{answers[1]}\n{answers[2]}\n")
                real_question = str(question).replace(" ","+")
                google_query = "https://google.com/search?q="+real_question  
                option1=f"{answers[0]}"
                option2=f"{answers[1]}"
                option3=f"{answers[2]}"
                op1 = str(option1).replace(" ","+")
                op2 = str(option2).replace(" ","+")
                op3 = str(option3).replace(" ","+")
                bar = "Search with all options"
                sl = "https://www.google.com/search?q="+real_question+"+"+op1+"+"+op2+"+"+op3          
                embed=discord.Embed(title=f"**Question {qcnt}/{Fullcnt}**",description=f"[{question}]({google_query}) \n\n [{bar}]({sl})")
                embed.set_footer(text="Made By Ben X Prayas")
                embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/578379566544846901/630400208265805835/401ec468afa82a2937b8ad3a4e811463.jpg")
                hook.send(embed=embed)
                #hook2.send(embed=embed)
                #hq.send(embed=embed)
                #hook3.send(embed=embed)
                r = requests.get("http://www.google.com/search?q="+ question +"+"+ option1 +"+"+ option2 +"+"+ option3)
                soup = BeautifulSoup(r.text, 'html.parser')
                response = soup.find_all("span", class_="st")
                res = str(r.text)
                countoption1 = res.count(option1)
                countoption2 = res.count(option2)
                countoption3 = res.count(option3)
                if 'not' in question or 'never' in question or 'incorrect' in question:
                    maxcount = min(countoption1, countoption2, countoption3)
                else:
                    maxcount = max(countoption1, countoption2, countoption3)
                sumcount = countoption1+countoption2+countoption3
                print("/n")
                if countoption1 == maxcount:
                	print(f"A {answers[0]}")
                elif countoption2 == maxcount:
                	print(f"B {answers[1]}")
                else:
                	print(f"C {answers[2]}")              
                if countoption1 == maxcount:
                    embed2=discord.Embed(title=f"**__Google Results!__**",description=f"\n**:one:. {answers[0]} `:` {countoption1} ✅**  \n**:two:. {answers[1]} `:` {countoption2}** \n**:three:. {answers[2]} `:` {countoption3}**",colour=0x00FBFF)
                    hook.send(embed=embed2)
                    #hq.send(embed=embed2)
                    #hook2.send(embed=embed2)
                    #hook3.send(embed=embed2)
                    #hook.send("e")
                    #hq.send("hq")
                    #hook2.send("e")
                    #hook3.send("+")
                    #sleep(10)
                    #embed=discord.Embed(title="",description="**Times Up!**",color=0x10C5FE) 
                    #embed.set_thumbnail(url="https://media.discordapp.net/attachments/931116321419194368/932833069738651658/Alarm_Clock_GIF_Animation_High_Res.gif")
                    #hook.send(embed=embed)
                    #hq.send(embed=embed)
                    #hook2.send(embed=embed)
                    #hook3.send(embed=embed)
                elif countoption2 == maxcount:
                    embed2=discord.Embed(title=f"**__Google Results!__**",description=f"\n**:one:. {answers[0]} `:` {countoption1}** \n**:two:. {answers[1]} `:` {countoption2} ✅**  \n**:three:. {answers[2]} `:` {countoption3}**",colour=0x00FBFF)
                    #embed2.set_thumbnail(url="https://is3-ssl.mzstatic.com/image/thumb/Purple113/v4/13/82/d5/1382d5b4-ecea-b99c-0622-e701fa5325ac/HQAppIcon-0-0-1x_U007emarketing-0-0-0-7-0-0-sRGB-0-0-0-GLES2_U002c0-512MB-85-220-0-0.png/246x0w.png")
                    #embed2.set_footer(text="Made By WC \𝐊𝐍𝐈𝐆𝐇𝐓 𝐊𝐈𝐍𝐆#6526")
                    hook.send(embed=embed2)
                    #hq.send(embed=embed2)
                    #hook.send("e")
                    #hq.send("hq")
                    #hook2.send(embed=embed2)
                    #hook2.send("e")
                    #hook3.send(embed=embed2)
                    #hook3.send("+")
                    #sleep(10)
                    #embed=discord.Embed(title="",description="**Times Up!**",color=0x10C5FE) 
                    #embed.set_thumbnail(url="https://media.discordapp.net/attachments/931116321419194368/932833069738651658/Alarm_Clock_GIF_Animation_High_Res.gif")
                    #hook.send(embed=embed)
                    #hq.send(embed=embed)
                    #hook2.send(embed=embed)
                    #hook3.send(embed=embed)
                else:
                    embed2=discord.Embed(title=f"**__Google Results!__**",description=f"\n**:one:. {answers[0]} `:` {countoption1}**\n**:two:. {answers[1]} `:` {countoption2}**\n**:three:. {answers[2]} `:` {countoption3} ✅**",colour=0x00FBFF)
                    #embed2.set_thumbnail(url="https://is3-ssl.mzstatic.com/image/thumb/Purple113/v4/13/82/d5/1382d5b4-ecea-b99c-0622-e701fa5325ac/HQAppIcon-0-0-1x_U007emarketing-0-0-0-7-0-0-sRGB-0-0-0-GLES2_U002c0-512MB-85-220-0-0.png/246x0w.png")
                    #embed2.set_footer(text="Made By WC \𝐊𝐍𝐈𝐆𝐇𝐓 𝐊𝐈𝐍𝐆#6526")
                    hook.send(embed=embed2)
                    #hq.send(embed=embed2)
                    #hook.send("e")
                    #hq.send("hq")
                    #hook2.send(embed=embed2)
                    #hook2.send("e")
                    #hook3.send(embed=embed2)
                    #hook3.send("+")
                    #sleep(10)
                    #embed=discord.Embed(title="",description="**Times Up!**",color=0x10C5FE) 
                    #embed.set_thumbnail(url="https://media.discordapp.net/attachments/931116321419194368/932833069738651658/Alarm_Clock_GIF_Animation_High_Res.gif")
                    #hook.send(embed=embed)
                    #hq.send(embed=embed)
                    #hook2.send(embed=embed)
                    #hook3.send(embed=embed)

                r = requests.get("http://www.google.com/search?q="+question)
                soup = BeautifulSoup(r.text, 'html.parser')
                response = soup.find_all("span", class_="st")
                res = str(r.text)
                countoption1 = res.count(option1)
                countoption2 = res.count(option2)
                countoption3 = res.count(option3)
                if 'not' in question or 'never' in question or 'incorrect' in question:
                    maxcount = min(countoption1, countoption2, countoption3)
                else:
                    maxcount = max(countoption1, countoption2, countoption3)
                sumcount = countoption1+countoption2+countoption3
                if countoption1 == maxcount:
                    embed2=discord.Embed(title=f"**__Google Results 2!__**",description=f"\n**:one:. {answers[0]} `:` {countoption1} ✅**  \n**:two:. {answers[1]} `:` {countoption2}** \n**:three:. {answers[2]} `:` {countoption3}**",colour=0x00FBFF)
                    hook.send(embed=embed2)
                    #hq.send(embed=embed2)
                    #hook2.send(embed=embed2)
                    #hook3.send(embed=embed2)
                    hook.send("e")
                    #hq.send("hq")
                    #hook2.send("e")
                    #hook3.send("+")
                    sleep(10)
                    embed=discord.Embed(title="",description="**Times Up!**",color=0x10C5FE) 
                    embed.set_thumbnail(url="https://media.discordapp.net/attachments/931116321419194368/932833069738651658/Alarm_Clock_GIF_Animation_High_Res.gif")
                    hook.send(embed=embed)
                    #hq.send(embed=embed)
                    #hook2.send(embed=embed)
                    #hook3.send(embed=embed)
                elif countoption2 == maxcount:
                    embed2=discord.Embed(title=f"**__Google Results 2!__**",description=f"\n**:one:. {answers[0]} `:` {countoption1}** \n**:two:. {answers[1]} `:` {countoption2} ✅**  \n**:three:. {answers[2]} `:` {countoption3}**",colour=0x00FBFF)
                    #embed2.set_thumbnail(url="https://is3-ssl.mzstatic.com/image/thumb/Purple113/v4/13/82/d5/1382d5b4-ecea-b99c-0622-e701fa5325ac/HQAppIcon-0-0-1x_U007emarketing-0-0-0-7-0-0-sRGB-0-0-0-GLES2_U002c0-512MB-85-220-0-0.png/246x0w.png")
                    #embed2.set_footer(text="Made By WC \𝐊𝐍𝐈𝐆𝐇𝐓 𝐊𝐈𝐍𝐆#6526")
                    hook.send(embed=embed2)
                    #hq.send(embed=embed2)
                    hook.send("e")
                    #hq.send("hq")
                    #hook2.send(embed=embed2)
                    #hook2.send("e")
                    #hook3.send(embed=embed2)
                    #hook3.send("+")
                    sleep(10)
                    embed=discord.Embed(title="",description="**Times Up!**",color=0x10C5FE) 
                    embed.set_thumbnail(url="https://media.discordapp.net/attachments/931116321419194368/932833069738651658/Alarm_Clock_GIF_Animation_High_Res.gif")
                    hook.send(embed=embed)
                    #hq.send(embed=embed)
                    #hook2.send(embed=embed)
                    #hook3.send(embed=embed)
                else:
                    embed2=discord.Embed(title=f"**__Google Results 2!__**",description=f"\n**:one:. {answers[0]} `:` {countoption1}**\n**:two:. {answers[1]} `:` {countoption2}**\n**:three:. {answers[2]} `:` {countoption3} ✅**",colour=0x00FBFF)
                    #embed2.set_thumbnail(url="https://is3-ssl.mzstatic.com/image/thumb/Purple113/v4/13/82/d5/1382d5b4-ecea-b99c-0622-e701fa5325ac/HQAppIcon-0-0-1x_U007emarketing-0-0-0-7-0-0-sRGB-0-0-0-GLES2_U002c0-512MB-85-220-0-0.png/246x0w.png")
                    #embed2.set_footer(text="Made By WC \𝐊𝐍𝐈𝐆𝐇𝐓 𝐊𝐈𝐍𝐆#6526")
                    hook.send(embed=embed2)
                    #hq.send(embed=embed2)
                    hook.send("e")
                    #hq.send("hq")
                    #hook2.send(embed=embed2)
                    #hook2.send("e")
                    #hook3.send(embed=embed2)
                    #hook3.send("+")
                    sleep(10)
                    embed=discord.Embed(title="",description="**Times Up!**",color=0x10C5FE) 
                    embed.set_thumbnail(url="https://media.discordapp.net/attachments/931116321419194368/932833069738651658/Alarm_Clock_GIF_Animation_High_Res.gif")
                    hook.send(embed=embed)
                    #hq.send(embed=embed)
                    #hook2.send(embed=embed)
                    #hook3.send(embed=embed)
            elif message_data["type"] == "questionSummary":

                answer_counts = {}
                correct = ""
                for answer in message_data["answerCounts"]:
                    ans_str = unidecode(answer["answer"])

                    if answer["correct"]:
                        correct = ans_str
                advancing = message_data['advancingPlayersCount']
                eliminated = message_data['eliminatedPlayersCount']
                nextcheck = message_data['nextCheckpointIn']
                ans = (5000)/(int(advancing))
                payout = float("{:.2f}".format(ans))
                total = int(advancing) + int(eliminated)
                percentAdvancing = (int(advancing)*(100))/(int(total))
                pA = float("{:.2f}".format(percentAdvancing))
                percentEliminated = (int(eliminated)*(100))/(int(total))
                pE = float("{:.2f}".format(percentEliminated))
                print(message_data)
                if option1 == correct:
                    embd=discord.Embed(title=f"**Question {qcnt} out of {Fullcnt}**",  description=f"**[{question}]({google_query})**", color=0x4286f4)
                    embd.add_field(name="**Correct Answer :-**", value=f"**Option 1️⃣. {correct}**")
                    embd.add_field(name="**Status :-**", value=f"**• Advancing Players: {advancing} ({pA}%)**\n**• Eliminated  Players: {eliminated} ({pE}%)\n• Current Payout: ${payout}**", inline=True)
                    embed.set_image(url="https://cdn.discordapp.com/attachments/649457795875209265/672845602824126494/Nitro_2.gif")
                    #embd.set_footer(text=f"HQ Google | Subrata#3297", icon_url="")
                    hook.send(embed=embd)
                    #hq.send(embed=embd)
                    #hook2.send(embed=embd)
                    #hook3.send(embed=embd)
                elif option2 == correct:
                    embd=discord.Embed(title=f"**Question {qcnt} out of {Fullcnt}**",  description=f"**[{question}]({google_query})**", color=0x4286f4)
                    embd.add_field(name="**Correct Answer :-**", value=f"**Option 2️⃣. {correct}**")
                    embd.add_field(name="**Status :-**", value=f"**• Advancing Players: {advancing} ({pA}%)**\n**• Eliminated  Players: {eliminated} ({pE}%)\n• Current Payout: ${payout}**", inline=True)
#                    embed.set_image(url="https://cdn.discordapp.com/attachments/649457795875209265/672845602824126494/Nitro_2.gif")
                    embed.set_image(url="https://cdn.discordapp.com/attachments/649457795875209265/672845602824126494/Nitro_2.gif")
                    #embd.set_footer(text=f"HQ Google | Subrata#3297", icon_url="")
                    hook.send(embed=embd)
                    #hq.send(embed=embd)
                    #hook2.send(embed=embd)
                    #hook3.send(embed=embd)
                else:
                    embd=discord.Embed(title=f"**Question {qcnt} out of {Fullcnt}**",  description=f"**[{question}]({google_query})**", color=0x4286f4)
                    embd.add_field(name="**Correct Answer :-**", value=f"**Option 3️⃣. {correct}**")
                    embd.add_field(name="**Status :-**", value=f"**• Advancing Players: {advancing} ({pA}%)**\n**• Eliminated  Players: {eliminated} ({pE}%)\n• Current Payout: ${payout}**", inline=True)
                    embed.set_image(url="https://cdn.discordapp.com/attachments/649457795875209265/672845602824126494/Nitro_2.gif")
                    #embd.set_footer(text=f"HQ Google | Subrata#3297", icon_url="")
                    hook.send(embed=embd)
                    #hq.send(embed=embd)
                    #hook2.send(embed=embd)
                    #hook3.send(embed=embd)

            elif message_data["type"] == "gameSummary":
                winn = message_data['numWinners']
                prizeMoney = str(message_data["winners"][0]["prize"])
                embed=discord.Embed(title="**__Game Summary__**",description="",color=0x00FBFF)
                embed.add_field(name="**• Payout**", value=f"**{prizeMoney}**", inline=True)
                embed.add_field(name="**• Total Winners**", value=f"**{winn} :tada:**", inline=True)
                embed.add_field(name="**• Prize Money :**", value=f"**5000$**", inline=True)
                embed.set_thumbnail(url="https://media.discordapp.net/attachments/931116321419194368/932667794892390450/200w.gif")
                embed.set_image(url="https://cdn.discordapp.com/attachments/649457795875209265/672845602824126494/Nitro_2.gif")
                #embed.set_footer(text=f"Made By ๖ۣۜǤнσsτ☠𝕮𝖍𝖎𝖑𝖉#7252")
                hook.send(embed=embed)
                #hq.send(embed=embed)
                #hook2.send(embed=embed)
                #hook3.send(embed=embed)



"""
def open_browser(question):
    main_url = "https://www.google.co.in/search?q=" + question
    webbrowser.open_new(main_url)
"""

def get_auth_token():
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "BTOKEN.txt"), "r") as conn_settings:
        settings = conn_settings.read().splitlines()
        settings = [line for line in settings if line != "" and line != " "]

        try:
            auth_token = settings[0].split("=")[1]
        except IndexError:
            print('No Key is given!')
            return 'NONE'

        return auth_token

while True:
    if show_active():
        url = get_socket_url()
        #print('Connecting to Socket : {}'.format(url))
        #hook.send('Connecting to Socket : {}'.format(url))

        token = get_auth_token()
        if token == 'None':
            print('Please enter a valid auth token.')
        else:
            connect_websocket(url, token)

    else:
        show_not_on()
        time.sleep(300)


