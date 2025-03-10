import discord
import datetime
import gspread

KEY = ""

def find_name(message):
    for i in range(len(message)):
        if message[i] == "Y":
            for j in range(len(message) - i - 1):
                if message[j + i + 1] == "!":
                    new_message = message[0:j + i]
                    for k in [len(new_message) - 1 - k for k in range(len(new_message))]:
                        if message[k] == " ":
                            return message[k+1:j+i+1]
        
def find_level(message):
    for i in range(len(message)):
        if message[i] == "Y":
            for j in range(len(message) - i - 1):
                if message[j + i + 1] == "!":
                    new_message = message[0:j + i]
                    for k in [len(new_message) - 1 - k for k in range(len(new_message))]:
                        if message[k] == " ":
                            return message[k-2:k]
        
def save_last_msg_time(dateTime):
    f = open("lastmessage.txt", "w")
    f.write(str(dateTime))
    f.close()
    return

def read_last_msg_time():
    f = open("lastmessage.txt", "r")
    lastTime = f.read()
    f.close()
    return lastTime

def update_sheet(data):
    gc = gspread.service_account(filename="credentials.json")
    sh = gc.open_by_key(KEY)
    worksheet = sh.sheet1
    
    entries = len(worksheet.col_values(1))
    
    worksheet.insert_rows(data, entries + 1)

client = discord.Client()

new_data = []

@client.event
async def on_ready():
    print('ready....')
    channel = discord.utils.get(client.get_all_channels(), name='pokemon-safari-zone')
    if channel == None:
        print('Error')
    else:
        print(channel.id)
        
        #get last message and save time in text file
        last_msg_time = read_last_msg_time()
        message_time = datetime.datetime.strptime(last_msg_time, '%Y-%m-%d %H:%M:%S.%f')
        
        last_message = await channel.fetch_message(channel.last_message_id)
        print(last_message.created_at)
        save_last_msg_time(last_message.created_at)
        counter = 0
        
        async for message in channel.history(after=message_time, oldest_first=True, limit=5000000):
            if str(message.author) == "Pokétwo#8236":
                if message.content.startswith("Congratulations <"):
                    counter += 1
                    mentions = message.mentions
                    catcher = mentions[0]
                    dateTime = str(message.created_at)
                    pokemon = find_name(message.content)
                    level = find_level(message.content)
                    
                    new_data.append([str(catcher), dateTime, str(pokemon), str(level)])       

        update_sheet(new_data)
        await channel.send("Added all mons since " + str(last_msg_time) + ". " + str(counter) + " mons were added.")
    
    
client.run()
