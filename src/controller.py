from toolbox import *
from state import *

class Controller:
    def __init__(self):
        self.quit: bool = False
        self.INSTRUCTIONS = ""
        self.selected_space: int = 0
        self.target_space: int = 0
    
    def update(self, cur_state: State) -> State:
        pass
    
    def received_quit(self):
        return self.quit

class TerminalController(Controller):
    def __init__(self):
        super().__init__()
        self.INSTRUCTIONS: str = "Please select one of the following actions:\n" \
            "  1) quit\n" \
            "  2) select piece\n" \
            "  3) move to space\n"
    
    def update(self, cur_state: State) -> State:
        uin = input()
        try:
            uin = int(uin)
        except:
            warn("* Invalid integer")
            return cur_state
        
        if uin == 1:
            self.quit = True
        elif uin == 2:
            uin = input(">> selected space: ").upper()
            self.selected_space = convert_selected_space_to_int(uin)
            if is_illegal_piece_selection(cur_state, self.selected_space):
                self.selected_space = 0
        elif uin == 3:
            if self.selected_space == 0:
                warn("* Select a piece first")
                return cur_state
            uin = input(">> target space: ").upper()
            self.target_space = convert_selected_space_to_int(uin)
            if is_illegal_target_space(cur_state, self.selected_space, self.target_space):
                self.target_space = 0
                return cur_state
            new_state = get_new_state(cur_state, self.selected_space, self.target_space)
            self.selected_space = 0
            self.target_space = 0
            return new_state
        return cur_state
