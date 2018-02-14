import discord
from google.cloud import translate
import json
discord_client = discord.Client()

keyfile = open("keys.txt", "r")
key = keyfile.read(60)

global last_message
last_message = "This is a placeholder"


@discord_client.event
async def on_ready():
    print("/-- Translate -- Discord --\\")
    print("Logged in as: ")
    print(discord_client.user.name)
    print(discord_client.user.id)
    print("----------------------------")
    await discord_client.change_presence(game=discord.Game(name=".translate help"))
    print("--- Bot Presence Changed ---")
    print("")


@discord_client.event
async def on_message(message):
    global last_message
    content = message.content
    if content.startswith(".translate"):
        # Makes the bot appear to be typing before sending its message
        discord_client.send_typing(message.channel)
        if " " in content:
            # When the user wants to call for help, or translate to more than english, this will parse their intention
            args = content.split(" ", 1)[1]
            print(args)
            langcode = check_language(args)
            if args.lower() == "help":
                help_message = "Type **.translate** to translate the message above to english.\n" \
                               " Type **.translate <language>** to translate it to that language."
                await discord_client.send_message(message.channel, help_message)
            elif langcode != "False":
                translation = translate_message(last_message, langcode)
                formatted_return = ("```" +
                                    "Translation: " + translation['translatedText'] + "\n"
                                    "Source Language : " + translation['detectedSourceLanguage'] +
                                    "```")
                await discord_client.send_message(message.channel, formatted_return)

        else:
            translation = translate_message(last_message, "en")
            formatted_return = ("```" +
                                "Translation: " + translation['translatedText'] + "\n"
                                "Source Language : " + translation['detectedSourceLanguage'] +
                                "```")
            await discord_client.send_message(message.channel, formatted_return)

    # Sets this message as the "ast message sent". Keep this at the END of the method
    last_message = content


# Translates the message and returns the output object.
def translate_message(message, target):
    translate_client = translate.Client.from_service_account_json('api-key.json')
    result = translate_client.translate(message, target_language=target)
    print(u'Text: {}'.format(result['input']))
    return result


# Takes in a string that may or may not be a language code.
# If it is a language code, it returns said code.
# If it is a language, it returns the affiliated code. If not, it returns -1
def check_language(code):
    with open('languages.json') as data:
        languages = json.load(data)
        for lang in languages:
            if (lang['language'].lower() == code.lower())or (lang['name'].lower() == code.lower()):
                return lang['language']
        return "False"


discord_client.run(key)
