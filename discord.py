import discord
import os,time,random

import json
import requests
from replit import db
























client = discord.Client()


prefix = "$"
author = "<@360469246108762113>"

sad_words = [
  "fuck",
  "unhappy",
  "angry",
  "depressed",
  "depress",
  "depressing",
  "حزين"

]

encourging = [
  "لا تيأس",
  "لا تعصب الامور طيبه",
  "ليش زعلان",
  "من مزعلك يا وحش"


]

def get_quots():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quots = json_data[0]["q"] + " |-| " + json_data[0]["a"]
  return(quots)


def remove_credits(user,amount):
  credits = db["credits2"]
  user = str(user)
  amount = int(credits[user]) - amount
  credits[user] = amount
  print(f"Removed {amount} from {user}")
  db["credits2"] = credits

def update_credit(user,amount):

  if "credits2" in db.keys():
    credits = db["credits2"]
    user = str(user)
    print(credits)
    try:
      if credits[user]:
        
        amount += int(credits[user])
        

        credits[user] = amount
        print(credits)
        db["credits2"] = credits
        print("Done")

      else:
        amount = 1000
        credits = db["credits2"]
        data = {user:amount}
        credits.update(data)
        db["credits2"] = credits
        print("User not found")

    except Exception as ex:
      amount = 1000
      credits = db["credits2"]
      data = {user:amount}
      credits.update(data)
      db["credits2"] = credits
      print(f"New user {user} has been created")
  else:
    user = str(user)
    amount=1000
    print("Hello")

    db["credits2"] = {user:amount}

def set_credits(user,amount):
  user_data = db["credits2"]
  user_data[user] = amount
  db["credits2"] = user_data



def update_encourage(encourage_message):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(encourage_message)
    db["encouragements"] = encouragements

  else:
    db["encouragements"] = [encourage_message]

def delete_encouragemets(index):
  encouragements = db["encouragements"]
  if len(encouragements) > index:
    del encouragements[index]
    db["encouragements"]= encouragements



@client.event
async def on_ready():
  print("I have logged in as {0.user}".format(client))
  activity = discord.Game(name="اكتب $inspire", type=1)
  await client.change_presence(status=discord.Status.idle, activity=activity)
  channel = client.get_channel(792393468101525514)
  await channel.send("I am online")


@client.event
async def on_message(message):
  msg = message.content
  user = str(message.author.id)
  bot_name = str(client.user)
  bot_fname = bot_name.split("#")
  mention = f'<@!{client.user.id}>'

  owner = False
  if message.author == bot_name:
    return

  if msg.startswith(f"{prefix}hello"):
    await message.channel.send("Hello!")

  if msg.startswith(f"{prefix}inspire"):
    quots = get_quots()
    await message.channel.send(quots)

  print(user)

  if msg.startswith(f"{prefix}vip"):
    if user == '360469246108762113':
      await message.channel.send("You are the owner")

   

  if msg.startswith(f"{prefix}ping"):

      
    before = time.monotonic()
    message = await message.channel.send("Pong!")
    ping = (time.monotonic() - before) * 1000
    await message.edit(content=f"Pong!  `{int(ping)}ms` :signal_strength:")
    print(f'Ping {int(ping)}ms')
  
  options = encourging
  if "encouragements" in db.keys():
    options = options + db["encouragements"]

  if msg.startswith("{}new".format(prefix)):
    encourage_message = msg.split("{}new ".format(prefix),1)[1]
    update_encourage(encourage_message)
    await message.channel.send("تم الاضافة بنجاح")


  if msg.startswith("{}del".format(prefix)):
    encouragements= []
    if "encouragements" in db.keys():
      index = int(msg.split("{}del".format(prefix),1)[1])
      delete_encouragemets(index)
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)

  if msg.startswith("{}list".format(prefix)):
    encouragements = db["encouragements"]
    for i in encouragements:
      await message.channel.send(i)
    



  if msg.startswith(f"{prefix}credits") or msg == "فلوسي" or msg == "رصيدي":

    credits = db["credits2"]
    try:
      user = msg.split(" ",1)[1]
      user1 = user[3:20]
      user_credits = credits[str(user1)]
      await message.channel.send(f"``{user_credits}$`` :credit_card: رصيدك الحالي هو {user}")
    except Exception as ex:
      user = user
      user_credits = credits[str(user)]
      await message.channel.send(f"``{user_credits}$`` :credit_card: رصيدك الحالي هو {message.author.mention}")
  

  if msg.startswith(f"{prefix}daily"):
    amount = 100
    amount = int(amount)
    update_credit(user,amount)
    credits = db["credits2"]
    await message.channel.send(f"```الى رصيدك {amount} تمت اضافة ```")
  i = 0
  if msg.startswith(f"{prefix}spamming"):
    while True:
      i+=1
      await message.channel.send(f"Spaming {i}")
      print(f"Spaming {i}")
      if msg == "stop":
        break

  if msg.startswith(f"{prefix}givecredits"):
    try:
      d = msg.split(" ",3)
      amount = d[2]
      user1 = d[1]
      user = user1[3:20]
      user = str(user)
      amount = int(amount)
      print(user,amount)
      update_credit(user,amount)
      remove_credits(message.author.id,amount)
      credits = db["credits2"]
      await message.channel.send(f"{user1} الى```{amount}``` تم تحويل")
    except ValueError:
      await message.channel.send(":warning: يرجى ادخال الصيغة الصحيحة")

  if mention in msg:
    await message.channel.send("```diff\n- امرني؟ \n```{}".format(message.author.mention))

  #Owner permission required  
  if user == '360469246108762113' or user == '44897177878741005' :
    if msg.startswith(f"{prefix}set-credits"):
      amount = msg.split("{}set-credits ".format(prefix),1)[1]
      user = str(user)
      await message.channel.send(f"{amount} تم تعيين اموالى الى")
      set_credits(user,amount)
    
    if msg.startswith(f"{prefix}reset-credits"):
      user = msg.split("{}reset-credits ".format(prefix),1)[1]
      set_credits(user,0)
      await message.channel.send(f"{user} :تم اعادى ضبط اموال")
    

    
    if msg.startswith(f"{prefix}addcredits"):

      try:
        d = msg.split(" ",3)
        amount = d[2]
        user1 = d[1]
        user = user1[3:20]
        user = str(user)
        amount = int(amount)
        print(user,amount)
        update_credit(user,amount)
      
        credits = db["credits2"]
        await message.channel.send(f"{user1} من الاموال الى ``{amount}`` تم اضافة")
      except ValueError:
        await message.channel.send(":warning: يرجى ادخال الصيغة الصحيحة")




  if msg.startswith("{}info".format(prefix)):
    await message.channel.send("```diff\n- تمت برمجة البوت من قبل \n```{}".format(author))


  for word in sad_words:
    if word in msg:
      await message.channel.send(random.choice(encourging))
    
  if user == '360469246108762113'  :
    if msg.startswith(f"{prefix}restart-bot") or msg == "restarting" or msg.startswith(f"{prefix}restart") or msg == "تحديث":
      await message.channel.send(":hammer_pick: !.....جاري التحديث")

      while 1:
        print(f"Restarting...{bot_name}")
        os.system("python main.py")
        time.sleep(0.2) # 200ms to CTR+C twice
      quit()

client.run(os.getenv("TOKEN"))
