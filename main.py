import discord
from discord.ext import commands
import json
from datetime import datetime

# Botの設定
TOKEN = "あなたのBotトークンをここに"
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# データ保存用ファイル
DATA_FILE = "sleep_data.json"

# JSONファイルを読み込み
def load_data():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# JSONファイルに保存
def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@bot.command()
async def sleep(ctx):
    """寝た時間を記録"""
    data = load_data()
    user_id = str(ctx.author.id)
    now = datetime.now().isoformat()
    data[user_id] = {"sleep": now}
    save_data(data)
    await ctx.send(f"おやすみ、{ctx.author.display_name}さん。就寝時間を記録しました。")

@bot.command()
async def wake(ctx):
    """起きた時間を記録して、睡眠時間を計算"""
    data = load_data()
    user_id = str(ctx.author.id)
    now = datetime.now()

    if user_id not in data or "sleep" not in data[user_id]:
        await ctx.send("先に「!sleep」で寝た時間を記録してね。")
        return

    sleep_time = datetime.fromisoformat(data[user_id]["sleep"])
    duration = now - sleep_time
    hours = duration.total_seconds() / 3600

    await ctx.send(
        f"おはよう、{ctx.author.display_name}さん！\n"
        f"睡眠時間は約 {hours:.1f} 時間でした。"
    )

    # データをリセット
    del data[user_id]["sleep"]
    save_data(data)

bot.run(TOKEN)
