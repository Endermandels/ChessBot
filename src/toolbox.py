class BColors:
    """ Text colors """
    BLACK = '\033[90m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    ENDC = '\033[0m'

WRN_COL = BColors.YELLOW # warn color
ERR_COL = BColors.RED # error color

def cprint(string: str, col: BColors=BColors.ENDC, endcol: BColors=BColors.ENDC):
    """ Print string with specified color """
    print(f"{col}{string}{endcol}")

def warn(string: str):
    """ Print a warning string """
    print(f"{BColors.BOLD}{WRN_COL}{string}{BColors.ENDC}")
    
def error(string: str):
    """ Print an error string """
    print(f"{BColors.BOLD}{ERR_COL}{string}{BColors.ENDC}")