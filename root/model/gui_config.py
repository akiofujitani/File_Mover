import logging
from dataclasses import dataclass
from collections import namedtuple
from model.scripts.json_config import load_json_config, save_json_config

logger = logging.getLogger('gui')


TtkGeometry = namedtuple('TtkGeometry', 'width height x y')


@dataclass
class GuiConfiguration:
    always_on_top : bool
    list_geometry : dict

    def __eq__(self, other) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        else:
            self_values = self.__dict__
            for key in self_values.keys():
                if not getattr(self, key) == getattr(other, key):
                    return False
            return True
    
    def to_dict(self):
        dict_config = {}
        dict_config['list_geometry'] = {gui_name : [gui_value.width, gui_value.height, gui_value.x, gui_value.y] for gui_name, gui_value in self.list_geometry.items()}
        return dict_config

    def geometry_ttk_geometry(self, geometry_str: str) -> None:
        size_pos = geometry_str.split('+')
        win_size = size_pos[0].split('x')
        return TtkGeometry(int(win_size[0]), int(win_size[1]), int(size_pos[1]), int(size_pos[2]))

    def check_update_win_pos(self, geometry_str:str, win_name: str) -> str:
        '''
        Get win position in configuration object
        '''
        try:
            current_geometry = self.geometry_ttk_geometry(geometry_str)
            geometry_values = self.list_geometry.get(win_name)
            if current_geometry == geometry_values:
                return geometry_str
            if not geometry_values:
                self.list_geometry[win_name] = current_geometry
                self.save_config_on_change()
                return geometry_str
            if geometry_values and current_geometry.x == 0 and current_geometry.y == 0:
                return f'{geometry_values.width}x{geometry_values.height}+{geometry_values.x}+{geometry_values.y}'
            else:
                self.list_geometry[win_name] = current_geometry
                self.save_config_on_change()
                return geometry_str
        except Exception as error:
            logger.error(f'Error getting window position due {error}')
            raise error

    def check_win_pos(self, win_name: str) -> str:
        '''
        Get win position in configuration object
        '''
        try:
            config_win_pos = self.list_geometry.get(win_name)
            if config_win_pos.width and config_win_pos.height:
                geometry_values = f'{config_win_pos.width}x{config_win_pos.height}+{config_win_pos.x}+{config_win_pos.y}'
                logger.debug(geometry_values)
                return geometry_values
        except Exception as error:
            logger.error(f'Error getting window position due {error}')
            raise error

    def save_config_on_change(self):
        '''
        Save to configuration file if it has changes
        '''
        try:
            old_config = self.init_dict(load_json_config('./data/gui_configuration.json'))
            if not self.__eq__(old_config):
                save_json_config('./data/gui_configuration.json', self.to_dict())
        except Exception as error:
            logger.error(f'Could not save configuration values {error}')  

    @classmethod
    def init_dict(cls, config_values: dict):
        try:
            alwais_on_top = config_values.get('always_on_top')
            list_geometry = {name : TtkGeometry(*value) for name, value in config_values.get('list_geometry').items()} if isinstance(config_values.get('list_geometry'), dict) else {}
            return cls(alwais_on_top, list_geometry)
        except Exception as error:
            raise error