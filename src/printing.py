from rich.console import Console

console = Console()

styles = {
    "thing": "bold light_goldenrod3",
    "action": "bold rosy_brown",
    "warn": "italic deep_pink4",
    "barista": "bold wheat4"
}

def say(*messages):
    global console
    if console is None:
        console = Console()
    for message in messages:
        console.print("    " + message)

def wrap_style(text, style):
    global styles
    return f"[{styles[style]}]{text}[/{styles[style]}]"

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


__all__ = ["say", "thing", "action", "warn", "barista", "styles"]
