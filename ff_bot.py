import sqlite3
from pyrogram import Client, filters
import random

# 🔹 Telegram API Details
api_id = 29750323  # Apna API ID yahan daal
api_hash = "5758cd5e87af90cf7918aa05e58832dc"
bot_token = "7957416817:AAHANto5L04t0mkkyyU5wo99KVQ06qVahyc"

# 🔹 Bot Setup
bot = Client("ff_group_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# 🔹 Database Setup (SQLite)
conn = sqlite3.connect("ff_bot.db", check_same_thread=False)
conn.execute("PRAGMA journal_mode=WAL;")  # ✅ WAL Mode Enable Karna
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS players (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT)")
conn.commit()
conn.close()

# 🔹 Start Command
@bot.on_message(filters.command("start") & filters.group)
def start(client, message):
    message.reply_text("👋 Welcome to KAKKAROT Bot! \nCommands:\n✅ /addme - Team me join kare\n✅ /team - Current team dikhaye\n✅ /reset - Team reset kare\n✅ /match - Random 2 teams banaye")

# 🔹 Player Ko Team Me Add Karna
@bot.on_message(filters.command("addme") & filters.group)
def add_player(client, message):
    conn = sqlite3.connect("ff_bot.db", check_same_thread=False)
    cursor = conn.cursor()
    user = message.from_user.first_name
    cursor.execute("SELECT * FROM players WHERE name=?", (user,))
    if cursor.fetchone():
        message.reply_text("⚠️ Tum already team me ho!")
    else:
        cursor.execute("INSERT INTO players (name) VALUES (?)", (user,))
        conn.commit()
        message.reply_text(f"✅ {user} team me add ho gaya!")
    conn.close()

# 🔹 Show Team Players
@bot.on_message(filters.command("team") & filters.group)
def show_team(client, message):
    conn = sqlite3.connect("ff_bot.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM players")
    players = cursor.fetchall()
    conn.close()
    if players:
        team_list = "\n".join([f"🔥 {p[0]}" for p in players])
        message.reply_text(f"🎮 Current Team:\n{team_list}")
    else:
        message.reply_text("❌ Abhi tak koi player add nahi hua!")

# 🔹 Reset Team
@bot.on_message(filters.command("reset") & filters.group)
def reset_team(client, message):
    conn = sqlite3.connect("ff_bot.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM players")
    conn.commit()
    conn.close()
    message.reply_text("🔄 Team reset kar di gayi hai!")

# 🔹 Random Match Making (2 Teams)
@bot.on_message(filters.command("match") & filters.group)
def match_teams(client, message):
    conn = sqlite3.connect("ff_bot.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM players")
    players = [p[0] for p in cursor.fetchall()]
    conn.close()
    if len(players) < 4:
        message.reply_text("⚠️ Kam se kam 4 players chahiye match banane ke liye!")
        return
    
    random.shuffle(players)
    mid = len(players) // 2
    team1 = players[:mid]
    team2 = players[mid:]
    
    team1_list = "\n".join([f"🔥 {p}" for p in team1])
    team2_list = "\n".join([f"💀 {p}" for p in team2])
    
    message.reply_text(f"🎯 Match Teams:\n\n🏆 Team 1:\n{team1_list}\n\n⚔️ Team 2:\n{team2_list}")

bot.run()