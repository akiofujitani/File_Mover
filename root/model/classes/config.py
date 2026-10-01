import logging
from dataclasses import dataclass
from os.path import normpath, abspath

logger = logging.getLogger('config')


@dataclass
class Move_Settings:
    source: str
    destination: str
    extention: str
    days_from_today: int
    copy: bool
    path_organization: str


    def __eq__(self, other) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        else:
            self_values = self.__dict__
            for key in self_values.keys():
                if not getattr(self, key) == getattr(other, key):
                    return False
            return True
    

    @classmethod
    def check_type_insertion(cls, source=str, destination=str, extention=str, days_from_today=int, copy=bool, path_organization=str):
        try:
            source = normpath(abspath(str(source)))
            destination = normpath(abspath(str(destination)))
            extention = str(extention)
            days_from_today = int(days_from_today)
            copy = eval(str(copy))
            path_organization = str(path_organization)
            return cls(source, destination, extention, days_from_today, copy, path_organization)
        except Exception as error:
            raise error


    def convert_to_dict(self) -> dict:
        values_dict = {}
        values_dict['source'] = self.source.replace('\\', '/')
        values_dict['destination'] = self.destination.replace('\\', '/')
        values_dict['extention'] = self.extention
        values_dict['days_from_today'] = self.days_from_today
        values_dict['copy'] = self.copy
        values_dict['path_organization'] = self.path_organization
        return values_dict

@dataclass
class Configuration_Values:
    wait_time: int
    file_per_cicle: int
    month_name_list: list
    directory_list: list


    def __eq__(self, other) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        else:
            self_values = self.__dict__
            for key in self_values.keys():
                if not getattr(self, key) == getattr(other, key):
                    return False
            return True
    

    @classmethod
    def check_type_insertion(cls, config_file_path=str, template=str):
        try:
            config = json_config.load_json_config(config_file_path, template)
            wait_time = int(config['wait_time'])
            files_per_cicle = int(config['files_per_cicle'])
            month_name_list = list(config['month_name_list'])
            directory_list = [Move_Settings.check_type_insertion(item['source'],
                            item['destination'],
                            item['extention'],
                            item['days_from_today'],
                            item['copy'],
                            item['path_organization']) for item in config['directory_list']]
            return cls(wait_time, files_per_cicle, month_name_list, directory_list)
        except Exception as error:
            raise error


    def convert_to_dict(self) -> dict:
        values_dict = {}
        values_dict['wait_time'] = self.wait_time
        values_dict['files_per_cicle'] = self.file_per_cicle
        values_dict['month_name_list'] = self.month_name_list
        values_dict['directory_list'] = [directory_value.convert_to_dict() for directory_value in self.directory_list]
        return values_dict


    def directory_list_add(self, move_settings=Move_Settings) -> None:
        self.directory_list.append(move_settings)


    def min_to_seconds(self) -> int:
        return self.wait_time * 60