from abc import ABC, abstractmethod
import os
from DbAdapter import DbAdapter

class ModuleBase(ABC):

    @abstractmethod
    def __init__(self, module_name, nice_name, app, description = None):
        self.__app = app
        self.__module_path = f"{os.getcwd()}/modules/{module_name}"

        # информация о моде
        self.__name = module_name
        self.__nice_name = nice_name
        self.__description = description

        # создание адаптера БД
        self.__db_adapter = DbAdapter(module_name)


    @property
    def name(self):
        return self.__name
    
    @property
    def nice_name(self):
        return self.__nice_name

    @property
    def description(self):
        return self.__description

    @property
    def database(self):
        return self.__db_adapter

    def getModelForUser(self, user_id: None):
        user_id = "default" if user_id is None else user_id
        model_file_path = f"{self.__modules_path}/neuralNetworks/{user_id}"

        model = self._importModel(model_file_path)

        return model

    def retrain(self, file_path): #return (bool, model)
        (is_imported, data_set) = self._import_data_set(file_path)

        if (is_imported == False):
            # todo: возврат исключения
            print("Ошибка импорта")
            return

        (is_overfitting, model) = self._overfitting(data_set)

        if (is_overfitting == False):
            # todo: возврат исключения
            print("Ошибка обучения")
            return

        self._save_model(model)

        return (True, model)

    @abstractmethod
    def _overfitting(self, data_set): # return (bool, model)
        pass

    @abstractmethod
    def _import_model(self, file_path):
        pass

    @abstractmethod
    def _save_model(self, model, file_path):
        pass

    @abstractmethod
    def _import_data_set(self, file_path): # return (bool, data_set)
        pass