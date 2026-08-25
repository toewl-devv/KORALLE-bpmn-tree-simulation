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

def highlight_process(text, process):
    color = PROCESS_COLORS[process % len(PROCESS_COLORS)]
    return f"{color}{text}{RESET}"


