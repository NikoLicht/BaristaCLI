from rich.console import Console

console = Console()

styles = {
    "thing": "bold light_goldenrod3",
    "action": "bold rosy_brown",
    "warn": "italic deep_pink4",
    "barista": "bold wheat4",
    "required": "italic medium_purple4",
    "header": "u bold"
}

def say(*messages):
    global console
    if console is None:
        console = Console()
    for message in messages:
        console.print("    " + message)

def title(title):
    console.print("")
    title_style = "bold rosy_brown"
    graphic_title = """
 ____             _     _            ____ _     ___ 
| __ )  __ _ _ __(_)___| |_ __ _    / ___| |   |_ _|
|  _ \ / _` | '__| / __| __/ _` |  | |   | |    | | 
| |_) | (_| | |  | \__ \ || (_| |  | |___| |___ | | 
|____/ \__,_|_|  |_|___/\__\__,_|   \____|_____|___|
"""
    console.print(f"[plain]{graphic_title}[/plain]", style=title_style, justify="center", highlight=False)
    console.print(f"A CLI coffee brewing experience by Nikolaj Bundgaard Licht.", style=title_style, justify="center")


def wrap_style(text, style):
    global styles
    return f"[{styles[style]}]{text}[/{styles[style]}]"

def header(text):
    max = 35
    extend = max - len(text)
    header_text = text
    for x in range(extend):
        header_text += "_"
    return wrap_style(header_text, "header")

def thing(thing) -> str:
    return wrap_style(thing, "thing")

def action(action) -> str:
    return wrap_style(action, "action")

def warn(warn, full_sentence = True) -> str:
    warning = wrap_style(warn, "warn")
    if(full_sentence):
        say(warning)
        return
    return warning

def barista(barista = "barista") -> str:
    return wrap_style(barista, "barista")

def req(required) -> str:
    return wrap_style(required, "required")


__all__ = ["say", "thing", "action", "warn", "barista", "styles", "req", "title", "header"]
