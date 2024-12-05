import discord
import re
from discord.ext import commands, tasks
import time
import asyncio
import datetime

def get_user_input(prompt):
  """Gets user input for a specific prompt and performs basic validation."""
  while True:
    user_input = input(prompt)
    if user_input:  # Check for empty input
      return user_input
    else:
      print("Please enter a value.")

def get_valid_integer(prompt):
    while True:
        try:
            value = int(input(prompt))
            return value
        except ValueError:
            print("viado burro numero ta errado")

# Obter os valores do usuário com validação
discord_token = get_user_input("Seu token de login: ")
server_id = get_valid_integer("Id do server: ")
channel_mudae = get_valid_integer("Id do canal da mudae: ")
numero_de_rolls = get_valid_integer("Quantos rolls você tem: ")
claim_rank = get_valid_integer("Qual o maior claim rank que você quer reagir? (ex: 500, você reagirá automaticamente em todos os porsonagens top 500 que aparecerem): ")

claim_rank = int(claim_rank)
server_id = int(server_id)
channel_mudae = int(channel_mudae)
numero_de_rolls = int(numero_de_rolls)

class MyClient(discord.Client):

    async def on_ready(self):
        print('logado como', self.user)
        self.channel = self.get_channel(channel_mudae) # pega o canal
        self.send_hourly_message.start() # task horaria

    async def on_message(self, message):
        if message.guild is None:  # dm ignorar
            return

        target_guild_id = server_id  # server id

        if message.guild.id != target_guild_id:
            return

        if message.author.id != 432610292342587392: # mudae
            return
#            await message.channel.send('MUDAE MANDOU MSG CARALHO FINALMENTE CONSEGUI FAZER ALGUMA COISA SOU FODA')
#            print(f'MUDAE MANDOU MSG EM: {message.guild.name}')

        if message.embeds:
            for embed in message.embeds:
                description = embed.description
                if description:
                    # Regex to find numbers after '#'
                    matches = re.findall(r"Claims: #(\d+)", description) 
                    for match in matches:
                        try:
                            number = int(match)
                            if number <= claim_rank:
                                await message.add_reaction("✅")
                                print(f"Reagiu com a boneca de claim rank: {number}")
                            else:
                                print(f"o claim rank {number} não é menor que 500")
                        except ValueError as e:
                            print(f"nigga: {e}")

    @tasks.loop(seconds=1) # checka todo segundo
    async def send_hourly_message(self):
        
        now = datetime.datetime.now()
        next_hour = (now + datetime.timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
        sleep_time = (next_hour - now).total_seconds()

        if sleep_time < 0:
          sleep_time = 3600
        
        print(f"tempo para o proximo reset em segundos: {sleep_time:.0f}")
        await asyncio.sleep(sleep_time)

        if self.channel:
            try:
                for _ in range(numero_de_rolls):  #loop numero_de_rolls
                    await self.channel.send("$wa")
                    await asyncio.sleep(2)  # Delay
                print("$wa enviados com sucesso")
            except Exception as e:
                print(f"deu erro: {e}")
        else:
            print("nao tem canal")

client = MyClient()
client.run(discord_token)