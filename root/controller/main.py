from queue import Queue
from view.main import View
from model.main import Model
from .main_view_controller import MainViewController

class Controller:
    def __init__(self, view: View, model: Model, log_queue: Queue) -> None:
        self.view = view
        self.model = model
        self.gui_configuration = self.model.gui_configuration
        self.database = self.model.database
        self.view.root.geometry(self.gui_configuration.check_update_win_pos(self.view.root.geometry(), 'main'))
        self.main_view_controller = MainViewController(view.main_view, self.model, log_queue)

    def start(self):
        self.view.start_main_loop()
    