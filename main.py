import discord
from discord.ext import commands
import requests

TOKEN = 'MTI2NDk2Mzk2ODM2MzkyNTY2OA.G0KQDL.rnQiGryq2u96xdm0Ad6AZt3jtE5ZRcuxisf7m4'

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='$', intents=intents)

# Define item_values dictionary globally
item_values = {}

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command(name='additem', help='Adds an item with a value and optional image URL.')
async def add_item(ctx, *, item_details: str):
    try:
        # Split item details by the first comma to separate name from value and image URL
        parts = item_details.split(',', 2)
        if len(parts) < 2:
            await ctx.send('Please provide item details in the format: "item_name, value, [image_url]"')
            return

        item_name = parts[0].strip().lower()  # Convert to lowercase for case-insensitive storage
        value = float(parts[1].strip())
        image_url = parts[2].strip() if len(parts) > 2 else None

        item_values[item_name] = {'value': value, 'image_url': image_url}
        await ctx.send(f'Item "{item_name}" with value "{value}" added. Image URL: {image_url}')
    except ValueError:
        await ctx.send('Invalid value provided. Please ensure the value is a number.')
    except Exception as e:
        await ctx.send(f'An error occurred: {str(e)}')

@bot.command(name='removeitem', help='Removes an item by name.')
async def remove_item(ctx, *, item_name: str):
    item_name = item_name.strip().lower()
    if item_name in item_values:
        del item_values[item_name]
        await ctx.send(f'Item "{item_name}" has been removed.')
    else:
        await ctx.send(f'Item "{item_name}" not found.')

@bot.command(name='checkvalue', help='Checks the value of an item by name.')
async def check_value(ctx, *, item_name: str):
    item_name = item_name.strip().lower()
    item = item_values.get(item_name)
    if item:
        response = f'Item "{item_name}" has value "{item["value"]}".'
        if item.get('image_url'):
            # Check if URL is valid and direct
            if requests.head(item['image_url']).status_code == 200:
                embed = discord.Embed(description=response)
                embed.set_image(url=item['image_url'])
                await ctx.send(embed=embed)
            else:
                await ctx.send('Image URL is not accessible or valid.')
        else:
            await ctx.send(response)
    else:
        await ctx.send(f'Item "{item_name}" not found.')

@bot.command(name='listitems', help='Lists all items with their values.')
async def list_items(ctx):
    if item_values:
        for item_name, item in item_values.items():
            response = f'**{item_name}**: {item["value"]}'
            embed = discord.Embed(description=response)
            if item.get('image_url'):
                # Check if URL is valid and direct
                if requests.head(item['image_url']).status_code == 200:
                    embed.set_image(url=item['image_url'])
                else:
                    await ctx.send(f'Error displaying image for item "{item_name}": Image URL is not accessible or valid.')
            await ctx.send(embed=embed)
    else:
        await ctx.send('No items found.')

@bot.command(name='commands', help='Lists all available commands.')
async def list_commands(ctx):
    commands_list = [f'${command.name}: {command.help}' for command in bot.commands]
    await ctx.send(f'Available commands:\n' + '\n'.join(commands_list))

bot.run(TOKEN)
