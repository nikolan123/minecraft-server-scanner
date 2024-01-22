import discord
import os # default module
from dotenv import load_dotenv
import json
import random
import base64
import binascii

#load results
with open('results.json', 'r') as file:
    results = json.load(file)

intents = discord.Intents.all()
bot = discord.Bot(intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")

@bot.slash_command(name = "ping", description = "Replies with 'Pong'")
async def hello(ctx):
    latency = round(bot.latency*1000)
    await ctx.respond(f"Pong! {latency}ms")

def randServer():
    random_entry = random.choice(results)
    ip = random_entry.get('ip', 'N/A')
    ver = random_entry.get('version', 'N/A')
    onp = random_entry.get('onlineplayers', 'N/A')
    motd = random_entry.get('motd', 'N/A')
    return f"IP: {ip}\nVersion: {ver}\nOnline Players: {onp}\nMOTD: {motd}"
class RandomNBTN(discord.ui.View):
    @discord.ui.button(label="Rerun", style=discord.ButtonStyle.primary, emoji="🔁")
    async def button_callback(self, button, interaction):
        await interaction.response.send_message(randServer(), view=RandomNBTN())
@bot.slash_command(name = "random", description = "Sends a random Minecraft server")
async def randomcmd(ctx):
    the = await ctx.respond(randServer(), view=RandomNBTN())

class EntryView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.index = 0

    @discord.ui.button(label='Next Entry', style=discord.ButtonStyle.primary)
    async def next_entry(self, button, interaction):
        if self.index < len(results) - 1:
            self.index += 1
        else:
            self.index = 0
        await interaction.response.edit_message(content="Please wait...")
        await self.update_message()

    async def update_message(self):
        first_entry = results[self.index]
        ip = first_entry.get('ip', 'N/A')
        version = first_entry.get('version', 'N/A')
        onlineplayers = first_entry.get('onlineplayers', 'N/A')
        motd = first_entry.get('motd', 'N/A')

        message = f"IP: {ip}\nVersion: {version}\nOnline Players: {onlineplayers}\nMOTD: {motd}"
        await self.message.edit(content=message)

@bot.slash_command(name = "servers", description = "Shows Minecraft servers")
async def show_entries(ctx):
    view = EntryView()
    first_entry = results[view.index]
    ip = first_entry.get('ip', 'N/A')
    version = first_entry.get('version', 'N/A')
    onlineplayers = first_entry.get('onlineplayers', 'N/A')
    motd = first_entry.get('motd', 'N/A')

    message = f"IP: {ip}\nVersion: {version}\nOnline Players: {onlineplayers}\nMOTD: {motd}"
    await ctx.respond(content=message, view=view)

    

bot.run("no")
