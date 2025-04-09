import view as vw
import controller as ct
from state import *

class Model:
    def __init__(self, view: vw.View, controller: ct.Controller,
                 default_state: State):
        self.view = view
        self.controller = controller
        self.default_state = default_state # TODO: Use
        self.cur_state = default_state
    
    def _update(self):
        self.view.update(self.cur_state, self.controller)
        self.cur_state = self.controller.update(self.cur_state)
    
    def run(self):
        while not self.controller.received_quit():
            self._update()

def main():
    view = vw.TerminalView()
    controller = ct.TerminalController()
    model = Model(view, controller, State())
    model.run()

if __name__ == "__main__":
    main()