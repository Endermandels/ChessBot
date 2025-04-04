class Controller:
    def __init__(self):
        self.quit: bool = False
    
    def update(self):
        pass
    
    def received_quit(self):
        return self.quit

class TerminalController(Controller):
    def __init__(self):
        super().__init__()
    
    def update(self):
        uin = input("To quit, press q: ")
        if uin.lower() == 'q':
            self.quit = True