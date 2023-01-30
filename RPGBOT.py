import discord
import random
import sqlite3
from math import *
import asyncio
from discord import Game
from discord.ext.commands import Bot
from discord.ext import commands
import time
from stuff import connect_database, remove_item, add_item, heal, chest, DefenseCalc, Attack, Move, Turn_Embed
#DEFINITIONS
#CLIENT
intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix=".",intents=intents)

@client.event
async def on_ready():
    chat = client.get_channel([REDACTED])
    await client.change_presence(status=discord.Status.online, activity=discord.Game("join no scam!"))

xp_dict = {"1":0,"2":100,"3":250,"4":475,"5":800,"6":1200,"7":1800,"8":2800,"9":4250,"10":6250,"11":8750,"12":12500,"13":17500,"14":24000,"15":32000,"16":42000,"17":55000,"18":70000,"19":90000,"20":120000,"21":99999999999}

@client.command(name="menu")
async def commands(context):
    random_lst = ["aye dog, whatcha wanna do", "Where would you like to go, brave one?", "go where do what?", "Heres the list of things you can do.", "Well? What would you like to do next?", "Heres the list of commands buddy", "Hmm.. what is it that you seek?", "Welcome to random RPG! What would you like to do?"]
    random_title = random_lst[random.randint(0,7)]
    menu_Embed = discord.Embed(title=random_title, description=":D", color=3066993)
    menu_Embed.add_field(name=".bipper", value="Visit Bipper (your sane guide)", inline=False)
    menu_Embed.add_field(name=".stats", value="View your basic stats here", inline=False)
    menu_Embed.add_field(name=".inv", value="View your inventory here", inline=False)
    menu_Embed.add_field(name=".wealth", value="View your wealth here", inline=False)
    menu_Embed.add_field(name=".equipment", value="View your equipments here", inline=False)
    menu_Embed.add_field(name=".shop", value="Enter shop here", inline=False)
    menu_Embed.add_field(name=".skill", value="View skills here [coming soon]", inline=False)
    menu_Embed.add_field(name=".fight", value="Battle another player [early version]", inline=False)
    menu_Embed.add_field(name=".map", value="Opens world map [coming soon]", inline=False)
    menu_Embed.add_field(name=".venture", value="Find and battle a random enemy [early version]", inline=False)
    menu_Embed.set_footer(text=".commands to view other commands")
    await context.message.channel.send(embed=menu_Embed)

@client.command(name="commands")
async def commands(context):
    help_Embed = discord.Embed(title="skididididididididi", description="- - - - - - - - - - - - - - - - - ", color=3066993)
    help_Embed.add_field(name=".item [item ID]", value="View item information (you can only view items that you own)", inline=False)
    help_Embed.add_field(name=".buy [item ID]", value="Buy an item from the shop", inline=False)
    help_Embed.add_field(name=".equip [item ID]", value="Equips an item", inline=False)
    help_Embed.add_field(name=".unequip [item ID]", value="Unequips an item", inline=False)
    help_Embed.add_field(name=".use [item ID]", value="Use an item. Used for consuming potions or opening chests.", inline=False)
    help_Embed.add_field(name=".join", value="creates an account. Each user can only have 1 account.", inline=False)
    await context.message.channel.send(embed=help_Embed)

@client.command(name="stats")
async def commands(context):
    db = connect_database()
    con = db.cursor()
    member = context.message.author
    cursor = con.execute("SELECT * FROM users WHERE user_id = ?", (member.id,))
    i = cursor.fetchone()
    cursor = con.execute("SELECT * FROM user_stats WHERE user_id = ?", (member.id,))
    x = cursor.fetchone()
    stats_Embed = discord.Embed(title=context.message.author.display_name + "'s stats",description="-",color=3447003)
    stats_Embed.add_field(name=f"Class: {str(i[3])}", value= f"Level {i[1]}, Exp: {i[2]}" , inline=False)
    stats_Embed.add_field(name="Physical Attack:", value=str(x[0]), inline=False)
    stats_Embed.add_field(name="Magic Power", value=str(x[1]), inline=False)
    stats_Embed.add_field(name="Health Points", value=f"{str(x[2])} / {str(x[10])}", inline=False)
    stats_Embed.add_field(name="Physical Defense", value=str(x[3]), inline=False)
    stats_Embed.add_field(name="Magic Resistance", value=str(x[4]), inline=False)
    stats_Embed.add_field(name="Agility", value=str(x[5]), inline=False)
    stats_Embed.add_field(name="Mana", value=str(x[6]), inline=False)
    stats_Embed.add_field(name="Physical Strength:", value=str(round(x[7],3)), inline=False)
    stats_Embed.add_field(name="Magic Potential:", value=str(round(x[8],3)), inline=False)
    stats_Embed.set_footer(text=".menu for list of commands")
    await context.message.channel.send(embed=stats_Embed)

@client.command(name="inv")
async def commands(context):
    db = connect_database()
    con = db.cursor()
    member = context.message.author
    cursor = con.execute("SELECT * FROM user_items")
    data = cursor.fetchall()
    item_lst = []
    for i in data:
        if i[0] == member.id:
            item_lst.append([i[2],i[3],i[4],i[1]])
    inv_Embed = discord.Embed(title= context.message.author.display_name + "'s inventory",description="---------------------------",color=3447003)
    for i in item_lst:
        inv_Embed.add_field(name="-"+ str(i[0]) + " ("+ str(i[1]) + ")", value="`" + str(i[2]) + " [ID:" + str(i[3]) + "]`", inline=False)
    inv_Embed.set_footer(text= " '.item [item ID]' to view item information!")
    await context.message.channel.send(embed=inv_Embed)

@client.command(name="item")
async def commands(context):
    db = connect_database()
    con = db.cursor()
    member = context.message.author
    msg = context.message.content
    lst = msg.split()
    cursor = con.execute("SELECT * FROM items WHERE item_id = ?", (int(lst[1]), ))
    data = cursor.fetchone()
    cursor = con.execute("SELECT * FROM user_items WHERE item_id = ? and user_id = ?", (int(lst[1]), member.id, ))
    data2 = cursor.fetchone()
    if data[3] == "Weapon" or data[3] == "Armor":
        stats = data[4].split()
        stat_name = ["PHY ATK:","MAGIC PWR:","PHY DEF:","MAGIC RES:","RANGE:"]
        stats_lst = []
        for i in range(len(stats)):
            if int(stats[i]) > 0:
                stats_lst.append(stat_name[i] + " " + str(stats[i]))
        data3= ""
        for i in stats_lst:
            data3 = data3 + i + "\n"
    else:
        data3 = "This item has no stats"
    if data2 == None:
        data2 = [0,0,0,0,0,0]
    item_Embed = discord.Embed(title= data[1] + " (" + str(data2[3]) + " owned)", description=" ", color = 3447003)
    item_Embed.add_field(name=data[2],value= data3 ,inline=False)
    item_Embed.add_field(name="Rarity:", value= data[6], inline=False)
    item_Embed.set_footer(text="")
    await context.message.channel.send(embed=item_Embed)

@client.command(name="wealth")
async def commands(context):
    db = connect_database()
    con = db.cursor()
    member = context.message.author
    cursor = con.execute("SELECT * FROM users WHERE user_id = ?", (member.id, ))
    data = cursor.fetchone()
    wealth_Embed = discord.Embed(title= context.message.author.display_name + "'s wealth", description= "----------------------------------", color=3447003)
    wealth_Embed.add_field(name= "Gold: " + str(data[4]),value= "Stored in bank: " + str(data[6]) +"/5000",inline=False)
    wealth_Embed.add_field(name="Crystal Shards: " + str(data[5]), value= "----------------------------------", inline=False)
    wealth_Embed.set_footer(text="note: dying in battles will make you lose all the gold you carry! Use .dep [amount of gold] to store gold.")
    await context.message.channel.send(embed=wealth_Embed)

@client.command(name="dep")
async def commands(context):
    db = connect_database()
    con = db.cursor()
    lst = context.message.content.split()
    amount = lst[1]
    member = context.message.author
    await context.channel.send(f"Are you sure you want to deposit {amount} gold? If yes, type 'y'. ")
    def check(a):
        return a.author == member
    response = await client.wait_for('message', check=check)
    if response.content.lower() == 'y':
        con.execute("SELECT * FROM users WHERE user_id = ?", (member.id,))
        data = con.fetchone()
        if (int(data[4]) - int(amount)) >= 0:
            con.execute("UPDATE users SET bank = bank + ? WHERE user_id = ?", (amount, member.id,))
            con.execute("UPDATE users SET gold = gold - ? WHERE user_id = ?", (amount, member.id,))
            db.commit()
            await context.channel.send(f"You have deposited {amount} gold into the bank.")
        else:
            await context.channel.send("You do not have enough gold.")
    else:
        await context.channel.send("deposit cancelled.")

@client.command(name="withdraw")
async def commands(context):
    db = connect_database()
    con = db.cursor()
    lst = context.message.content.split()
    amount = lst[1]
    member = context.message.author
    await context.channel.send(f"Are you sure you want to withdraw {amount} gold? If yes, type 'y'. ")
    def check(a):
        return a.author == member
    response = await client.wait_for('message', check=check)
    if response.content.lower() == 'y':
        con.execute("SELECT * FROM users WHERE user_id = ?", (member.id,))
        data = con.fetchone()
        if (int(data[6]) - int(amount)) >= 0:
            con.execute("UPDATE users SET bank = bank - ? WHERE user_id = ?", (amount, member.id,))
            con.execute("UPDATE users SET gold = gold + ? WHERE user_id = ?", (amount, member.id,))
            db.commit()
            await context.channel.send(f"You withdrew {amount} gold.")
        else:
            await context.channel.send("You do not have enough gold in the bank.")
    else:
        await context.channel.send("withdrawal cancelled.")


@client.command(name="equip")
async def commands(context):
    db = connect_database()
    con = db.cursor()
    member = context.message.author
    msg = context.message.content
    lst = msg.split()
    cursor = con.execute("SELECT item_id FROM user_items WHERE user_id = ? and item_id = ?", (member.id, int(lst[1]),))
    data = cursor.fetchone()
    if data == None:
        await context.message.channel.send("You do not own this equipment.")
        return None
    cursor = con.execute("SELECT * FROM items WHERE item_id = ?", (int(lst[1]),))
    data = cursor.fetchone()
    if data[3] not in ["Weapon", "Armor"]:
        await context.message.channel.send("This item cannot be equipped.")
        return None
    stats = data[4].split()
    cursor = con.execute("SELECT * FROM user_equipment WHERE user_id = ?", (member.id,))
    equipments = cursor.fetchone()
    if data[0] in equipments:
        await context.message.channel.send("Oops! You already have a " + data[1] + " equipped. You can't equip 2 of the same items!")
        return None
    if data[3] == "Weapon":
        if equipments[1] == None:
            con.execute("UPDATE user_equipment SET weapon1_id = ? WHERE user_id = ?", (data[0], member.id,))
        elif equipments[2] == None:
            con.execute("UPDATE user_equipment SET weapon2_id = ? WHERE user_id = ?", (data[0], member.id,))
        else:
            await context.message.channel.send("Oops! Weapon slots are full. Please unequip a weapon first.")
            return None
    if data[3] == "Armor":
        if equipments[6] == None:
            con.execute("UPDATE user_equipment SET armor_id = ? WHERE user_id = ?", (data[0], member.id,))
        else:
            await context.message.channel.send("Oops! You already have an armor equipped. Please unequip the armor first.")
            return None
    con.execute("UPDATE user_stats SET Physical_Attack = Physical_Attack + ?, Magic_Power = Magic_Power + ? , Physical_Defense = Physical_Defense + ?, Magic_Resistance = Magic_Resistance + ? WHERE user_id = ?",
                (int(stats[0]), int(stats[1]), int(stats[2]),int(stats[3]), member.id))
    db.commit()
    remove_item(data[0],member.id,1)
    await context.message.channel.send("You have equipped " + data[1] + ".")

@client.command(name="equipment")
async def commands(context):
    db = connect_database()
    con = db.cursor()
    member = context.message.author
    cursor = con.execute("SELECT * FROM user_equipment WHERE user_id = ?", (member.id,))
    equipment = cursor.fetchone()
    e_lst = []
    for i in equipment:
        if i != None:
            print(i)
            cursor = con.execute("SELECT * FROM items WHERE item_id = ?", (i,))
            data = cursor.fetchone()
            if data != None:
                e_lst.append(data[1])
            else:
                e_lst.append("None")
        else:
            e_lst.append("None")
    equipment_Embed = discord.Embed(title= context.message.author.display_name + "'s equipments", description="----------------------------------", color=3447003)
    equipment_Embed.add_field(name="Weapons", value="Weapon 1: " + e_lst[1] + " [ID: " + str(equipment[1]) + "]" + "\n" + "Weapon 2: " + e_lst[2] + " [ID: " + str(equipment[2]) + "]", inline=False)
    equipment_Embed.add_field(name="Armor",value=e_lst[6] + " [ID: " + str(equipment[6]) + "]", inline=False)
    equipment_Embed.add_field(name="Accessory", value=e_lst[5] + " [ID: " + str(equipment[5]) + "]", inline=False)
    equipment_Embed.add_field(name="Skills",value=f"Skill 1: {e_lst[1]} [ID: {str(equipment[1])}]" + "\n" + f"Skill 1: {e_lst[2]} [ID: {str(equipment[2])}]", inline=False)
    equipment_Embed.set_footer(text = "'.unequip [Item ID]' to unequip item.")
    await context.message.channel.send(embed=equipment_Embed)

@client.command(name="unequip")
async def commands(context):
    db = connect_database()
    con = db.cursor()
    member = context.message.author
    msg = context.message.content
    lst = msg.split()
    cursor = con.execute("SELECT * FROM user_equipment WHERE user_id = ?", (member.id,))
    data = cursor.fetchone()
    if data == None:
        await context.message.channel.send("Oops! You do not have this item equipped")
        return None
    e_lst = ["user_id", "weapon1_id", "weapon2_id", "skill1_id","skill2_id","accessory_id","armor_id"]
    for i in range(len(data)):
        if data[i] == int(lst[1]):
            name = e_lst[i]
            con.execute("UPDATE user_equipment SET (%s) = ? WHERE user_id = ?" %(name), (None, member.id,))
    db.commit()
    add_item(int(lst[1]),member.id,1)
    cursor = con.execute("SELECT * FROM items WHERE item_id = ?", (int(lst[1]),))
    data = cursor.fetchone()
    stats = data[4].split()
    con.execute("UPDATE user_stats SET Physical_Attack = Physical_Attack - ?, Magic_Power = Magic_Power - ? , Physical_Defense = Physical_Defense - ?, Magic_Resistance = Magic_Resistance - ? WHERE user_id = ?",(int(stats[0]), int(stats[1]), int(stats[2]), int(stats[3]), member.id))
    db.commit()
    await context.message.channel.send("Alright, it has been added back to ur inventory.")

@client.command(name="shop") #C: 50/100 U:250/500 R:1000/2000 L:5000/10000
async def commands(context):
    db = connect_database()
    con = db.cursor()
    member = context.message.author
    shop_Embed = discord.Embed(title="shop",description="----------------------------------", color=3447003)
    cursor = con.execute("SELECT * FROM shop")
    shop_lst = cursor.fetchall()
    print(shop_lst)
    for i in shop_lst:
        cursor = con.execute("SELECT * FROM items WHERE item_id = ?",(i[0],))
        data = cursor.fetchone()
        shop_Embed.add_field(name=f"{data[1]} [ID:{data[0]}]",value=f"Cost: {i[1]} Gold",inline=False)
    await context.channel.send(embed=shop_Embed)

@client.command(name="buy")
async def commands(context):
    db = connect_database()
    con = db.cursor()
    member = context.message.author
    id = int(context.message.content.split()[1])
    cursor = con.execute("SELECT * FROM shop WHERE item_id =?",(id,))
    item = cursor.fetchone()
    if item == None:
        await context.channel.send("Sorry pal, this item isn't for sale.")
        return None
    cursor = con.execute("SELECT gold FROM users WHERE user_id = ?",(member.id,))
    gold = cursor.fetchone()
    if int(gold[0]) >= int(item[1]):
        add_item(id,member.id,1)
        con.execute("UPDATE users SET gold = gold - ? WHERE user_id = ?",(int(item[1]),member.id))
        db.commit()
        await context.channel.send("Item has been bought successfully.")
    else:
        await context.channel.send("Insufficient gold.")

@client.command(name="use")
async def commands(context):
    db = connect_database()
    con = db.cursor()
    txt=""
    member = context.message.author
    id = int(context.message.content.split()[1])
    cursor = con.execute("SELECT * FROM items WHERE item_id =?",(id,))
    item = cursor.fetchone()
    cursor = con.execute("SELECT * FROM users WHERE user_id = ?",(member.id,))
    data = cursor.fetchone()
    if item[3] not in ["Chest", "Consumable"]:
        await context.channel.send("This item cannot be used as it is neither a chest nor a consumable.")
        return None
    if item[3] == "Chest":
        locked = False
        if id == 32:
            cursor = con.execute("SELECT * FROM user_items WHERE item_id = 34 AND user_id = ?", (member.id,))
            key = cursor.fetchone()
            if key == None:
                await context.channel.send("The `Crystal Chest` appears to be locked...")
                locked = True
            else:
                await context.channel.send("You insert the `Mysterious Key` into the keyhole and the `Crystal Chest` opens!")
        if locked == False:
            data = chest(id,member.id,data[3])
            message = await context.channel.send(f"Opening {item[1]}...")
            await asyncio.sleep(2)
            txt += "You got:\n"
            for i in range(len(data[0])):
                cursor = con.execute("SELECT item_name FROM items WHERE item_id =?",(data[0][i],))
                txt += f"`{cursor.fetchone()[0]}` [ID:{data[0][i]}] \n"
            txt += f"`{data[1]}` Gold"
            await message.edit(content=txt)
    elif item[3] == "Consumable":
        if item[0] in [14,15,16]: #HEALING ITEM
            healing_dict = {14: 50, 15: 150, 16: 300}
            results = remove_item(item[0], member.id, 1)
            if results == False:
                await context.channel.send("You do not own this item.")
            else:
                results = heal(healing_dict[item[0]], member.id)
                await context.channel.send(f"{member.mention} used `{item[1]} [ID: {item[0]}]` and recovered `{results[0]}` HP! Current HP: `{results[1]}`")
        pass


@client.command(name="join")
async def commands(context):
    db = connect_database()
    con = db.cursor()
    user_data = con.execute("SELECT * FROM users")
    data = user_data.fetchall()
    member = context.message.author
    data.append([1,1])
    for i in data:
        if i[0] == member.id:
            await context.channel.send("You have already joined.")
            return None
        entry_Embed = discord.Embed(title="Welcome to uh... a random RPG!",description="Please select your starting class! Your starting class only affects your starting stats and items, you will still be able to use items from other classes.",color=3066993)
        entry_Embed.add_field(name="Warrior", value="Magic is for weaklings lol", inline=False)
        entry_Embed.add_field(name="Mage", value="Only peasants fight without magic", inline=False)
        entry_Embed.add_field(name="Archer", value="A stick with string is pretty op", inline=False)
        entry_Embed.set_footer(text="Reply with 1 to choose Warrior, 2 to choose Mage or 3 to choose Archer.")
        cursor = con.execute("SELECT * FROM users WHERE user_id = ?", (member.id,))
        data = cursor.fetchone()
        if data == None:
            await context.message.channel.send(embed=entry_Embed)
        def check(m):
            return m.content in ['1', '2', '3'] and m.author == member
        choice = await client.wait_for('message', check=check)
        class_dict = {"1": ["Warrior",1], "2": ["Mage",2], "3": ["Archer",3]}
        #stat format: Phy ATK, Magic Power, HP, PHY def, Magic def, Agility, Mana, Strength, Potential
        stats_dict = {"2": [5,20,100,10,20,10,100,1.0,1.0], "1": [20,5,150,20,20,10,50,1.0,1.0], "3": [10,10,100,10,10,20,100,1.0,1.0]}
        await context.channel.send("You have selected: {}".format(class_dict[choice.content]))
        await context.channel.send("Welcome to random RPG! Use .menu for list of commands.")
        con.execute("INSERT INTO user_stats(Physical_Attack, Magic_Power, Health_Points, Physical_Defense, Magic_Resistance, Agility, Mana, Physical_Strength, Magic_Potential, user_id, max_HP) VALUES(?,?,?,?,?,?,?,?,?,?,?)",(stats_dict[choice.content][0],stats_dict[choice.content][1],stats_dict[choice.content][2],stats_dict[choice.content][3],stats_dict[choice.content][4],stats_dict[choice.content][5],stats_dict[choice.content][6],stats_dict[choice.content][7],stats_dict[choice.content][8],member.id,stats_dict[choice.content][2]))
        con.execute("INSERT INTO users(user_id, user_lvl, user_xp, user_class, gold, crystal_shards, bank) VALUES(?, ?, ?, ?, ?, ?, ?)", (member.id, 1, 0, class_dict[choice.content][0],400 ,0, 0))
        con.execute("INSERT INTO user_equipment(user_id) VALUES(?)", (member.id,))
        cursor = con.execute("SELECT * FROM items")
        data = cursor.fetchall()
        for a in data:
            if a[0] == class_dict[choice.content][1]:
                data = a
        cursor = con.execute("SELECT * FROM items WHERE item_id = 4")
        data2 = cursor.fetchone()
        con.execute("INSERT INTO user_items(user_id, item_id, item_name, qty, type) VALUES(?,?,?,?,?)", (member.id, data[0], data[1], 1, data[3]))
        con.execute("INSERT INTO user_items(user_id, item_id, item_name, qty, type) VALUES(?,?,?,?,?)",(member.id, data2[0], data2[1], 1, data2[3]))
        db.commit()
        return None


@client.event #CHECK USER LEVEL + LVL UP
async def on_message(message):
    db = connect_database()
    con = db.cursor()
    member = message.author
    cursor = con.execute("SELECT * FROM users WHERE user_id = ?", (member.id, ))
    data = cursor.fetchone()
    class_stats = {'Warrior':[0.06,0.02], 'Archer':[0.04,0.04], 'Mage':[0.02,0.06]}
    if data != None:
        if data[2] >= xp_dict[str(data[1] + 1)]:
            con.execute("UPDATE users SET user_lvl= user_lvl + 1 WHERE user_id = ?", (member.id, ))
            con.execute("UPDATE user_stats SET Physical_Attack = Physical_Attack + 1, Magic_Power = Magic_Power + 1, Health_Points = Health_Points + 15, Physical_Strength = Physical_Strength + ?, Magic_Potential = Magic_Potential + ?, max_HP = max_HP + 15 WHERE user_id = ?", (class_stats[data[3]][0],class_stats[data[3]][1],member.id, ))
            cursor = con.execute("SELECT user_lvl FROM users WHERE user_id = ?", (member.id, ))
            user_lvl = cursor.fetchone()
            print(user_lvl)
            if user_lvl in [5,10,15,20]:
                con.execute("UPDATE user_stats SET Agility = Agility + 10 WHERE user_id = ?", (member.id, ))
            db.commit()
            await message.channel.send("Yas! You just levelled up! You are now level "+ str(data[1] + 1) + "! Base stats slightly increased!")
    await client.process_commands(message)

#stats1: PHY ATK, MAGIC PW, PHY DEF, MAGIC RES, RANGE
#stats2: LIFESTEAL, BURN, BLEED, AGILITY, MANA, CRIT

#--------------------------------------------------BATTLE STUFF. I HOPE THIS WORKS------------------------------------------------------------
#enemy stats(basic): phy_atk, magic_pwr, HP, phy_def, magic_res, range, agility
def PVE1():
    pass


#-------------------------------------------------------------------------------------------------

@client.command(name="fight")
async def fight(context, user: discord.Member):
    turn = 0
    turn_count = 1
    db = connect_database()
    con = db.cursor()
    p2 = user.mention
    member = context.message.author
    p1 = context.message.author.mention
    cursor = con.execute("SELECT weapon1_id, weapon2_id FROM user_equipment WHERE user_id =?", (member.id,))
    data = cursor.fetchone()
    if None in data:
        await context.message.channel.send("Please ensure that both players has equipped 2 weapons. We do not encourage fist fights.")
        return None
    cursor = con.execute("SELECT * FROM user_stats WHERE user_id = ?", (user.id,))
    data2 = cursor.fetchone()
    cursor = con.execute("SELECT * FROM user_stats WHERE user_id = ?", (member.id,))
    data1 = cursor.fetchone()
    cursor = con.execute("SELECT * FROM items WHERE item_id = ?",(data[0],))
    p1weapon1 = cursor.fetchone()
    cursor = con.execute("SELECT * FROM items WHERE item_id = ?", (data[1],))
    p1weapon2 = cursor.fetchone()
    cursor = con.execute("SELECT weapon1_id, weapon2_id FROM user_equipment WHERE user_id =?", (user.id,))
    data = cursor.fetchone()
    if None in data:
        await context.message.channel.send("Please ensure that both players has equipped 2 weapons. We do not encourage fist fights.")
        return None
    cursor = con.execute("SELECT * FROM items WHERE item_id = ?", (data[0],))
    p2weapon1 = cursor.fetchone()
    cursor = con.execute("SELECT * FROM items WHERE item_id = ?", (data[1],))
    p2weapon2 = cursor.fetchone()
    print(p1weapon1,p1weapon2,p2weapon1,p2weapon2)
    p1selected = p1weapon1
    p1notselected = p1weapon2
    p2selected = p2weapon1
    p2notselected = p2weapon2
    if p1 == p2:
        await context.channel.send(f"You cannot fight yourself {p1} :D")
    else:
        await context.channel.send(f"{p1} challenges {p2} to a battle! Please reply with 'y' if you accept this challenge!")
    def check(a):
        return a.author == user
    response = await client.wait_for('message', check=check)
    if response.content.lower() == "y":
        position = [15,25]
        action_pt = 3
        while data1[2] > 0 and data2[2] > 0:
            cursor = con.execute("SELECT * FROM user_stats WHERE user_id = ?", (user.id,))
            data2 = cursor.fetchone()
            cursor = con.execute("SELECT * FROM user_stats WHERE user_id = ?", (member.id,))
            data1 = cursor.fetchone()
            if turn == 0:
                await context.channel.send(embed = Turn_Embed(member.display_name,data1,data2,turn_count, position[0], position[1], action_pt,p1selected,p1notselected))

                def check(m):
                    return m.author == member and m.content.split()[0] in ["attack","move","skip","switch"]

                response = await client.wait_for('message', check=check)
                if "skip" in response.content.split():
                    action_pt = 0

                if "move" in response.content.split() and turn == 0:
                    if int(response.content.split()[2]) > data1[5]/10:
                        await context.channel.send(f"You cannot move {response.content.split()[2]}m as your current Agility[{data1[5]}] only allows you to move {floor(data1[5]/10)}")
                    else:
                        position = Move("1",member.display_name,response.content.split()[1],int(response.content.split()[2]),position)
                        action_pt -= 1

                if "attack" in response.content.lower() and turn == 0:
                    print(data1, data2)
                    if int(abs(position[0] - position[1])) > int(p1selected[4].split()[4]):
                        await context.channel.send("Your attack cannot reach the enemy. Get closer!")
                    else:
                        lst = Attack(member.display_name, user, data1, data2, position, p1selected, p1notselected, "player","pvp", None)
                        await context.channel.send(lst)
                        action_pt -= 1
                if "switch" in response.content.lower() and turn == 0:
                    if p1selected == p1weapon1:
                        p1selected = p1weapon2
                        p1notselected = p1weapon1
                    else:
                        p1selected = p1weapon1
                        p1notselected = p1weapon2

            elif turn == 1:
                await context.channel.send(embed=Turn_Embed(user.display_name, data2, data1, turn_count, position[0], position[1], action_pt,p2selected, p2notselected))

                def check(o):
                    return o.author == user and o.content.split()[0] in ["attack","move","skip","switch"]

                response = await client.wait_for('message', check=check)
                if "skip" in response.content.split():
                    action_pt = 0
                if "move" in response.content.lower().split() and turn == 1:
                    if int(response.content.split()[2]) > data2[5]/10:
                        await context.channel.send(f"You cannot move {response.content.split()[2]}m as your current Agility[{data2[5]}] only allows you to move {floor(data2[5]/10)}m")
                    else:
                        position = Move("2",user.display_name,response.content.split()[1],int(response.content.split()[2]),position)
                        action_pt -= 1

                if "attack" in response.content.lower() and turn == 1:
                    if int(abs(position[0] - position[1])) > int(p2selected[4].split()[4]):
                        await context.channel.send("Your attack cannot reach the enemy. Get closer!")
                    else:
                        lst = Attack(user.display_name, user, data2, data1, position, p2selected, p2notselected, "player", "pvp", None)
                        await context.channel.send(lst)
                        action_pt -= 1

                if "switch" in response.content.lower() and turn == 0:
                    if p1selected == p1weapon1:
                        p2selected = p1weapon2
                        p2notselected = p1weapon1
                    else:
                        p2selected = p1weapon1
                        p2notselected = p1weapon2

            if action_pt == 0:
                if turn == 0:
                    turn += 1
                elif turn == 1:
                    turn -= 1
                turn_count += 1
                action_pt = 3

        if data1[2] > 0:
            await context.channel.send(f"{p1} Wins!!!")
            con.execute("UPDATE user_stats SET Health_Points = ? WHERE user_id = ?", (20,data2[9]))
            db.commit()
        elif data2[2] >0 :
            await context.channel.send(f"{p2} Wins!!!")
            con.execute("UPDATE user_stats SET Health_Points = ? WHERE user_id = ?", (20,data1[9]))
            db.commit()
    else:
        await context.channel.send("Challenge rejected.")

#-------------------------------------------------------------------------------------------------

def bot1(position, enemy): #standard brainless / melee
    if int(abs(position[0] - position[1])) < int(enemy[2].split()[4]):
        return "Attack" 
    elif int(position[1] - position[0]) > 0:
        return f"Move left {int(enemy[3].split()[0])}"
    else:
        return f"Move right {int(enemy[3].split()[0])}"

def bot2(position, enemy): #slightly smarter ranged, moves away at 6m
    if int(abs(position[0] - position[1])) < 8:
        if int(position[1] - position[0]) > 0:
            return f"Move right {int(enemy[3].split()[0])}"
        else:
            return f"Move left {int(enemy[3].split()[0])}"
    else:
        return "Attack"

def skills(position, player_data, enemy, mode):
    pass 
        
#-------------------------------------------------------------------------------------------------

@client.command(name="venture")
async def venture(context):
    turn = 0
    turn_count = 1
    db = connect_database()
    con = db.cursor()
    member = context.message.author
    p1 = context.message.author.mention
    cursor = con.execute("SELECT weapon1_id, weapon2_id FROM user_equipment WHERE user_id =?", (member.id,))
    data = cursor.fetchone()
    if None in data:
        await context.message.channel.send(
            "Please ensure that you have equipped 2 weapons. We do not encourage fist fights.")
        return None
    cursor = con.execute("SELECT * FROM user_stats WHERE user_id = ?", (member.id,))
    data1 = cursor.fetchone()
    cursor = con.execute("SELECT * FROM items WHERE item_id = ?", (data[0],))
    p1weapon1 = cursor.fetchone()
    cursor = con.execute("SELECT * FROM items WHERE item_id = ?", (data[1],))
    p1weapon2 = cursor.fetchone()
    p1selected = p1weapon1
    p1notselected = p1weapon2
    rng_enemy = random.randint(1,100)
    if rng_enemy <= 10:
        lst = [6,7]
        rng = lst[random.randint(0,len(lst)-1)]
    elif rng_enemy <= 50:
        lst = [3,4,2]
        rng = lst[random.randint(0, len(lst)-1)]
    else:
        lst = [1,5,8]
        rng = lst[random.randint(0, len(lst)-1)]
    cursor = con.execute("SELECT * FROM Enemy WHERE enemy_id = ?",(rng,))
    enemy = cursor.fetchone()
    enemy_HP = int(enemy[3].split()[1])
    enemy_agil = int(enemy[3].split()[0])
    await context.channel.send(f"You encountered a `{enemy[1]}` ! \n Enemy info:`{enemy[7]}` \n Rarity:`{enemy[6]}` \n Enter 'y' if you wish to fight it!")
    def check(a):
        return a.author == member
    response = await client.wait_for('message', check=check)
    if "y" in response.content.lower():
        position = [15, 25]
        action_pt = 3
        while data1[2] > 0 and enemy_HP > 0:
            cursor = con.execute("SELECT * FROM user_stats WHERE user_id = ?", (member.id,))
            data1 = cursor.fetchone()
            if turn == 0:
                await context.channel.send(
                    embed=Turn_Embed(member.display_name, data1, [enemy_HP,enemy_HP,enemy_HP,enemy_HP,enemy_HP], turn_count, position[0], position[1], action_pt,
                                     p1selected, p1notselected))

                def check(m):
                    return m.author == member and m.content.split()[0] in ["attack", "move", "skip", "switch"]

                response = await client.wait_for('message', check=check)
                if "skip" in response.content.split():
                    action_pt = 0

                if "move" in response.content.split() and turn == 0:
                    if int(response.content.split()[2]) > data1[5] / 10:
                        await context.channel.send(
                            f"You cannot move {response.content.split()[2]}m as your current Agility[{data1[5]}] only allows you to move {floor(data1[5] / 10)}")
                    else:
                        position = Move("1", member.display_name, response.content.split()[1],
                                        int(response.content.split()[2]), position)
                        action_pt -= 1

                if "attack" in response.content.lower() and turn == 0:
                    if int(abs(position[0] - position[1])) > int(p1selected[4].split()[4]):
                        await context.channel.send("Your attack cannot reach the enemy. Get closer!")
                    else:
                        lst = Attack(member.display_name, enemy[1], data1, enemy, position, p1selected, p1notselected, "player", "pve", enemy_HP)
                        enemy_HP = lst[1]
                        await context.channel.send(lst[0])
                        action_pt -= 1
                if "switch" in response.content.lower() and turn == 0:
                    if p1selected == p1weapon1:
                        p1selected = p1weapon2
                        p1notselected = p1weapon1
                    else:
                        p1selected = p1weapon1
                        p1notselected = p1weapon2

            elif turn == 1:
                response = bot1(position, enemy)
                if "Move" in response and turn == 1:
                    position = Move("2", enemy[1], response.split()[1],
                                    int(response.split()[2]), position)
                    action_pt -= 1

                if "Attack" in response and turn == 1:
                    lst = Attack(enemy[1], member.display_name, enemy, data1, position, None, None, "bot", "pve", None)
                    await context.channel.send(lst)
                    action_pt -= 1

            if action_pt == 0:
                if turn == 0:
                    turn += 1
                elif turn == 1:
                    turn -= 1
                turn_count += 1
                action_pt = 3

        if data1[2] > 0:
            #Player wins
            await context.channel.send("You Win!!!")
            reward_info = Reward(enemy[6], 'grass plains', data1[9])
            final_gold = reward_info[0]
            final_exp = reward_info[1]
            await context.channel.send(f"You earned {final_gold} gold and {final_exp} exp!")
            pass
        else:
            #Enemy wins
            await context.channel.send("you died.")
            con.execute("UPDATE user_stats SET Health_Points = ? WHERE user_id = ?", (20,data1[9],))
            con.execute("UPDATE users SET gold = 0 WHERE user_id = ?",(data1[9],))
            db.commit()
    else:
        await context.channel.send("You ran away.")

#-------------------------------------------------------------------------------------------------


def Reward(enemy_rarity, enemy_biome, user_id):
    db = connect_database()
    con = db.cursor()
    if enemy_biome == 'grass plains':
        difficulty = 1
    elif enemy_biome == 'forest':
        difficulty = 2
    elif enemy_biome == 'mountains':
        difficulty = 3
    elif enemy_biome == 'dungeon ruins':
        difficulty = 4
    if enemy_rarity == 'COMMON':
        gold = random.randint(50,75)
        exp = random.randint(30,45)
    elif enemy_rarity == 'UNCOMMON':
        gold = random.randint(120,160)
        exp = random.randint(70,95)
    elif enemy_rarity == 'RARE':
        gold = random.randint(290,345)
        exp = random.randint(130,165)
    final_exp = exp*difficulty
    final_gold = gold*difficulty
    con.execute("UPDATE users SET gold = gold + ?, user_xp = user_xp + ? WHERE user_id = ?", (final_gold, final_exp, user_id))
    db.commit()
    return [final_gold, final_exp]
    pass

client.run("[REDACTED]")


