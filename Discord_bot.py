import discord
import os
import pandas as pd
import openpyxl as xl
from tabulate import tabulate
from keep_alive import keep_alive

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hel'):
        await message.channel.send('hello')

    if message.content.startswith('$percentage'):
        await message.channel.send("Fetching Data Please wait")
        os.system("python run_spider.py")
        # Check if the Excel file exists in the current directory
        filename = 'Win_rate.xlsx'
        if os.path.exists(filename):
            # # Load the Excel file using openpyxl
            # wb = xl.load_workbook(filename)
            # sheet = wb.active
            #
            # # Create a fixed-width ASCII table of the Excel file contents
            # headers = [cell.value for cell in sheet[1]]
            # data = [[cell.value for cell in row] for row in sheet.iter_rows(min_row=2)]
            # table = tabulate(data, headers=headers, tablefmt='plain')
            #
            # # Send the table in a message
            # await message.channel.send('```' + table + '```')
            with open(filename, 'rb') as f:
                file = discord.File(f)
                await message.channel.send(file=file)
        else:
            await message.channel.send('The file Win_rate.xlsx does not exist.')
#keep_alive()
#client.run(os.getenv['token'])
