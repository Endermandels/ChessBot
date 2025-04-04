import view as vw
import controller as ct
from state import *

DEFAULT_STATE = State(
    # Bitboards for white pieces
    white_pawns   = 0b0000000000000000000000000000000000000000000000001111111100000000,
    white_rooks   = 0b0000000000000000000000000000000000000000000000000000000010000001,
    white_knights = 0b0000000000000000000000000000000000000000000000000000000001000010,
    white_bishops = 0b0000000000000000000000000000000000000000000000000000000000100100,
    white_queens  = 0b0000000000000000000000000000000000000000000000000000000000010000,
    white_king    = 0b0000000000000000000000000000000000000000000000000000000000001000,
    
    # Bitboards for black pieces (mirrored from white)
    black_pawns   = 0b0000000011111111000000000000000000000000000000000000000000000000,
    black_rooks   = 0b1000000100000000000000000000000000000000000000000000000000000000,
    black_knights = 0b0100001000000000000000000000000000000000000000000000000000000000,
    black_bishops = 0b0010010000000000000000000000000000000000000000000000000000000000,
    black_queens  = 0b0001000000000000000000000000000000000000000000000000000000000000,
    black_king    = 0b0000100000000000000000000000000000000000000000000000000000000000,
)

class Model:
    def __init__(self, view: vw.View, controller: ct.Controller,
                 default_state: State):
        self.view = view
        self.controller = controller
        self.default_state = default_state # TODO: Use
        self.cur_state = default_state
    
    def _update(self):
        self.view.update(self.cur_state)
        self.controller.update()
    
    def run(self):
        while not self.controller.received_quit():
            self._update()

def main():
    view = vw.TerminalView()
    controller = ct.TerminalController()
    model = Model(view, controller, DEFAULT_STATE)
    model.run()

if __name__ == "__main__":
    main()