import asyncio
import config
import discord
from discord.ext import commands
import time

TOKEN = config.token
prefix = config.prefix
activity = config.activity
role = config.access_role
category = config.category

bot = commands.Bot(command_prefix = prefix, help_command=None)

embed = discord.Embed(title="Default title", description="default description")

misschannel = discord.Embed(title="Questo canale non è un aae channel", description=f"si prega di creare un aae-channel usando il comando {prefix}embed", color=0x123456)

colori = {"rosso": 0xe74c3c, "blu": 0x2c3e50, "azzurro": 0x3498db, "turchese": 0x1abc9c, "giallo": 0xf1c40f, "arancione": 0xe67e22, "viola": 0x8e44ad, "grigio": 0x7f8c8d, "bianco": 0xecf0f1, "nero": 0x0f0f0f}

@bot.event
async def on_ready():
    print("Loggato con {0.user}".format(bot))
    await bot.change_presence(activity=discord.Game(name=activity))

@bot.command(name='embed', help='crea un canale in cui gestire il tuo embed')
@commands.has_role(role)
async def embed(ctx, name="embed"):

    global channel
    name = "aae-" + name

    print(f"{ctx.author.name} ha creato un canale embed ({name})")
    await ctx.message.delete()

    # creazione canale
    channel = await ctx.guild.categories[category].create_text_channel(name=name)

    # permessi al sender
    await channel.set_permissions(ctx.author, read_messages=True)
    await channel.set_permissions(ctx.author, send_messages=True)

    # embed da inviare all'inizio
    startembed = discord.Embed(title="NUOVO CANALE AAE", description="Crea un nuovo embed seguendo le istruzioni qua sotto!", color=colori["turchese"])
    startembed.set_author(name="AJstudios it", url="https://discord.io/AJstudios", icon_url="https://images-ext-1.discordapp.net/external/NV1bQ1UXM36jYiN8PAeEijA9XLj8G5uzsK_Dd526hh0/%3Fs%3D200%26v%3D4/https/avatars.githubusercontent.com/u/92890257")
    startembed.add_field(name="title, desc and colours", value=f'usa {prefix}head"<titolo>" "<descrizione>" "<colore>" per aggiungere un titolo al tuo embed (DA USARE PRIMA DI OGNI COMANDO)', inline=False)
    startembed.add_field(name="field inline", value=f'usa {prefix}fieldi "<titolo>" "<descrizione>" (NB usa le virgolette) per aggiungere una field inline al tuo embed', inline=False)
    startembed.add_field(name="field ouline", value=f'usa {prefix}fieldo "<titolo>" "<descrizione>" (NB usa le virgolette) per aggiungere una field outline al tuo embed', inline=False)
    startembed.add_field(name="footer", value=f'usa {prefix}foot <testo> per aggiungere un footer al tuo embed', inline=False)
    startembed.add_field(name="author", value=f'usa {prefix}auth "<testo>" "<url-icona>" (NB usa le virgolette) per aggiungere un author al tuo embed', inline=False)
    startembed.add_field(name="lista colori", value=f'usa {prefix}lcolor per vedere una lista di colori da applicare al tuo embed', inline=False)
    startembed.add_field(name="esempio", value=f'usa {prefix}example per vedere un embed predefinito per capire cosa sono author, footer ecc...', inline=False)
    startembed.add_field(name="preview", value=f'usa {prefix}pre per vedere una preview del tuo embed', inline=False)
    startembed.add_field(name="send", value=f"usa {prefix}send <id canale> per inviare l'embed nel canale specificato", inline=False)
    startembed.add_field(name="end", value=f"usa {prefix}end per eliminare il canale", inline=False)

    await channel.send(embed=startembed)

@bot.command(name='header', help='imposta il titolo, la descrizione e il colore di un embed')
@commands.has_role(role)
async def main(ctx, title, description, color):
    global embed
    if ctx.channel.name.__contains__("aae"):
        embed = discord.Embed(title=title, description=description, color=colori[color.lower()])
        await ctx.send("**HEAD** settato correttamente")
    else:
        await ctx.send(embed=misschannel)

@bot.command(name='field inline', help='crea un field inline in un embed')
@commands.has_role(role)
async def fieldi(ctx, title, description):
    global embed
    if ctx.channel.name.__contains__("aae"):
        embed.add_field(name=title, value=description, inline=True)
        await ctx.send("**FIELD** settato correttamente")
    else:
        await ctx.send(embed=misschannel)

@bot.command(name='field outline', help='crea un field outline in un embed')
@commands.has_role(role)
async def fieldo(ctx, title, description):
    global embed
    if ctx.channel.name.__contains__("aae"):
        embed.add_field(name=title, value=description, inline=False)
        await ctx.send("**FIELD** settato correttamente")
    else:
        await ctx.send(embed=misschannel)

@bot.command(name='footer', help='imposta il footer in un embed')
@commands.has_role(role)
async def foot(ctx, title):
    global embed
    if ctx.channel.name.__contains__("aae"):
        embed.set_footer(text=title)
        await ctx.send("**FOOTER** settato correttamente")
    else:
        await ctx.send(embed=misschannel)

@bot.command(name='author', help="imposta l'autore di un embed")
@commands.has_role(role)
async def auth(ctx, txt, url):
    global embed
    if ctx.channel.name.__contains__("aae"):
        try:
            embed.set_author(name=txt, icon_url=url)
            await ctx.send("**AUTHOR** settato correttamente")
        except Exception as e:
            await ctx.send(f"**EXCEPTION:** {e}")
    else:
        await ctx.send(embed=misschannel)

@bot.command(name='esempio', help='manda un embed di esempio')
@commands.has_role(role)
async def example(ctx):
    if ctx.channel.name.__contains__("aae"):
        example = discord.Embed(title="Questo è il titolo", description="Questa è la descrizione", color=0x123456)
        example.add_field(name="Questo è il titolo di un field inline", value="questa è la descrizione del field inline", inline=True)
        example.add_field(name="Questo è il titolo di un field inline", value="questa è la descrizione del field inline", inline=True)
        example.add_field(name="Questo è il titolo di un field outline", value="questa è la descrizione del field outline", inline=False)
        example.add_field(name="Questo è il titolo di un field outline", value="questa è la descrizione del field outline", inline=False)
        example.set_author(name="Questo è il testo dell'author", icon_url="https://images-ext-1.discordapp.net/external/NV1bQ1UXM36jYiN8PAeEijA9XLj8G5uzsK_Dd526hh0/%3Fs%3D200%26v%3D4/https/avatars.githubusercontent.com/u/92890257")
        example.set_footer(text="Questo è il testo del footer")

        await ctx.send(embed=example)
    else:
        await ctx.send(embed=misschannel)

@bot.command(name='preview', help="manda l'embed in preview")
@commands.has_role(role)
async def pre(ctx):
    try:
        await ctx.send(embed=embed)
    except Exception as e:
            await ctx.send(f"**EXCEPTION:** {e}")

@bot.command(name='send', help="invia l'embed creato nel canale scelto")
@commands.has_role(role)
async def send(ctx, channel):
    if ctx.channel.name.__contains__("aae"):
        channel = int(channel)
        channel = bot.get_channel(channel)
        await channel.send(embed=embed)
        await ctx.send(":+1:")
    else:
        await ctx.send(embed=misschannel)

@bot.command(name='color list', help='invia una lista di colori disponibili per gli embed')
@commands.has_role(role)
async def lcolor(ctx):
    if ctx.channel.name.__contains__("aae"):
        lcolor = discord.Embed(title="Lista colori", description="**rosso** #e74c3c \n **blu** #2c3e50 \n **azzurro** #3498db \n **turchese** #1abc9c \n **giallo** #f1c40f \n **arancione** #e67e22 \n **viola** #8e44ad \n **grigio** #7f8c8d \n **bianco** #ecf0f1 \n **nero** #0f0f0f")
        await ctx.send(embed=lcolor)
    else:
        await ctx.send(embed=misschannel)

@bot.command(name='end', help='elimina il canale usato per creare il ticket')
@commands.has_role(role)
async def end(ctx):
    if ctx.channel.name.__contains__("aae"):
        eembed = discord.Embed(title="Chiuso", description=" :white_check_mark: | embed chiuso correttamente", color=colori["turchese"])
        await ctx.send(embed=eembed)
        time.sleep(1)
        await ctx.channel.delete()
    else:
        await ctx.send(embed=misschannel)

@bot.command(name='ping', help='ritorna il tempo di risposta del bot')
async def ping(ctx):
    latency = round(bot.latency, 3)
    latency = latency*1000
    latency = int(latency)
    await ctx.send(f'Ping » {latency} ms')

@bot.command(name='help', help='mostra questo comando')
async def help(ctx):
    help = discord.Embed(title="HELP", description="", color=0xe74c3c)
    help.add_field(name=f"bot: AAEmbed", value="Bot creato da AJstudios per qualsiasi utilizzo. Il codice è open source ed è soggetto ai Diritti d'Autore, è modificabile a patto che la modifica sia disponibile a TUTTI su github.com (con ovvia menzione al creatore). Al contrario, in nessun modo il codice può essere privato dai crediti al creatore (presenti in questo messaggio). I crediti devono essere accessibili da tutti tramite: descrizione del bot O comando di un bot O messaggio con crediti in un canale contenente solo esso accessibile a tutti.")

    await ctx.send(embed=help)

bot.run(TOKEN)