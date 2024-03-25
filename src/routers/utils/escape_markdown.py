def escape_markdown(text: str) -> str:
    escape_chars = ['\\', '`', '*', '_', '{', '}', '[', ']', '(', ')', '#', '+', '-', '.', '!']

    for char in escape_chars:
        text = text.replace(char, '\\' + char)

    return text