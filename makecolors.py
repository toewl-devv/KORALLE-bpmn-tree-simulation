import colorsys


def highlight(text):
    return f"\033[1;42m{text}\033[0m"

def non_highlight(text):
    return f"\033[31m{text}\033[0m"

PROCESS_COLORS = [
    "\033[31m",  # red
    "\033[32m",  # green
    "\033[33m",  # yellow
    "\033[34m",  # blue
    "\033[35m",  # magenta
    "\033[36m",  # cyan
]
RESET = "\033[0m"

def highlight_process(text, process, n):
    colors = [
        tuple(int(x * 255) for x in colorsys.hsv_to_rgb(i / n, 1, 1))
        for i in range(n)
    ]

    process_colors = [
        f"\033[38;2;{r};{g};{b}m"
        for r, g, b in colors
    ]

    color = process_colors[process]
    return f"{color}{text}{RESET}"
