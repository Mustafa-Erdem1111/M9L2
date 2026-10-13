import discord
from discord.ext import commands
import requests
import os
import traceback
import importlib.util
from config import TOKEN

gTTS = None
if importlib.util.find_spec("gtts") is not None:
    from gtts import gTTS

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

city = "Mardin"


@bot.command()
async def start(ctx):
    await ctx.send(
        "Merhaba! Ben hava durumunu yazılı ve sesli "
        "olarak bildiren bir botum! 🌦️\n"
        "!weather yazarak hava durumunu öğrenebilirsin."
    )


@bot.command()
async def weather(ctx):
    filename = "hava_durumu.mp3"

    try:
        url = "https://wttr.in/" + city + "?format=3"
        response = requests.get(url, timeout=15)
        response.raise_for_status()

        weather_text = response.text.strip()

        if not weather_text:
            await ctx.send("Hava durumu bilgisi alınamadı.")
            return

        await ctx.send("🌦️ " + weather_text)

        if gTTS is None:
            await ctx.send(
                "Sesli çıktı için gtts kütüphanesi kurulu değil. "
                "Terminalde `pip install gtts` komutunu çalıştırın."
            )
            return

        tts = gTTS(
            text=weather_text,
            lang="tr"
        )

        tts.save(filename)

        if not os.path.isfile(filename):
            await ctx.send("Ses dosyası oluşturulamadı.")
            return

        await ctx.send(
            "🔊 Hava durumu ses kaydı:",
            file=discord.File(filename)
        )

        print("Ses başarıyla gönderildi!")

    except Exception as e:
        print("\n--- HATA DETAYLARI ---")
        print("Hata türü:", type(e).__name__)
        print("Hata mesajı:", str(e))
        traceback.print_exc()

        await ctx.send(
            "Bir hata oluştu dostum. "
            "Terminaldeki hata mesajını kontrol et."
        )

    finally:
        if os.path.isfile(filename):
            try:
                os.remove(filename)
            except OSError:
                pass


@bot.event
async def on_ready():
    print("Bot hazır!")
    print("Bot adı:", bot.user)


bot.run(TOKEN)
