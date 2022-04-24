from dotty import ChatBot, Message, Storage, UserRegistry


class Colors:
    GREY = "\033[90m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    Default = "\033[99m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def respond(text: str) -> None:
    print(Colors.MAGENTA + f"🤖 {text}" + Colors.ENDC)


def bot_loop(the_bot: ChatBot) -> None:
    exit_loop: bool = False
    group: str = "Main"
    user: str = "Pascal"

    respond("Hello! I'm a bot named Dotty")
    while not exit_loop:
        console_input: str = str(input(Colors.CYAN + f"{user} @ [{group}] : " + Colors.ENDC))
        if console_input.casefold() == "bye":
            respond("Bye Bye!")
            exit_loop = True
        else:
            the_message = Message(body=console_input, sent_in=group, sent_by=user)
            response = the_bot.process_message(the_message)
            if response:
                respond(response)


if __name__ == "__main__":
    storage = Storage()
    users_registry = UserRegistry(storage=storage)
    dotty_bot = ChatBot(name="Dotty", owner_identifier="Pascal", users_registry=users_registry)
    bot_loop(the_bot=dotty_bot)
