import discord;

Client = discord.Client()

keyfile = open("keys.txt", "r")
key = keyfile.read(60)


@Client.event
async def on_ready():
    print("/-- Translate -- Discord --\\")
    print("Logged in as: ")
    print(Client.user.name)
    print(Client.user.id)
    print("----------------------------")

    await Client.change_presence(game=discord.Game(name=".translate help"))
    print("--- Bot Presence Changed ---")
    print("")


@Client.event
async def on_message(message):
    content = message.content
    if content.startswith(".translate"):
        # Makes the bot appear to be typing before sending its message
        Client.send_typing(message.channel)
        if " " in content:
            # When the user wants to call for help, or translate to more than english, this will parse their intention
            args = content.split(" ", 1)[1]
            print(args)
            if args.lower() == "help":
                print("call for help")

        else:
            print("This is when it will just translate to english")

Client.run(key)
