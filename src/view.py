from state import *
from toolbox import *
import controller as ct

class View:
    def __init__(self):
        pass
    
    def _display_state(self, state: State):
        pass
    
    def _display_instructions(self, controller: ct.Controller):
        pass
    
    def update(self, state: State):
        self._display_state(state)
        # self._display_instructions()


class TerminalView(View):
    PIECE_STRINGS = [
        BColors.GREEN + ' Wp ',
        BColors.GREEN + ' WR ',
        BColors.GREEN + ' WN ',
        BColors.GREEN + ' WB ',
        BColors.GREEN + ' WQ ',
        BColors.BOLD + BColors.GREEN + ' WK ',
        BColors.RED + ' Bp ',
        BColors.RED + ' BR ',
        BColors.RED + ' BN ',
        BColors.RED + ' BB ',
        BColors.RED + ' BQ ',
        BColors.BOLD + BColors.RED + ' BK ',
    ]
    
    def __init__(self):
        super().__init__()
    
    def _print_grid(self, state: State):
        string = ''
        piece_types = [
            state.white_pawns,
            state.white_rooks,
            state.white_knights,
            state.white_bishops,
            state.white_queens,
            state.white_king,
            state.black_pawns,
            state.black_rooks,
            state.black_knights,
            state.black_bishops,
            state.black_queens,
            state.black_king,
        ]
        for row in range(8):
            for col in range(8):
                # Look for which piece type is occupying a space
                empty = True
                for i, p in enumerate(piece_types):
                    if p & 1:
                        string += TerminalView.PIECE_STRINGS[i] + BColors.ENDC
                        empty = False
                        break
                if empty:
                    string += ' .. '
                    
                # Look at next space
                for i in range(len(piece_types)):
                    piece_types[i] >>= 1
                
            string += '\n'
        print(string)
    
    def _display_state(self, state: State):
        self._print_grid(state)
        print("Turn: ", end="")
        print(BColors.GREEN + "WHITE" if state.white_turn else BColors.RED + "BLACK")
        print(BColors.ENDC)