from abc import ABC, abstractmethod
import os
from DbAdapter import DbAdapter

from fastapi import Request
import fastapi
import jwtAuth

class ModuleBase(ABC):

    @abstractmethod
    def __init__(self, module_name, nice_name, app, description = None):
        self.__app = app
        self.__module_path = f"{os.path.dirname(__file__)}/../modules/{module_name}"

        a = f"{os.path.dirname(__file__)}/../modules/{module_name}"
        # информация о модуле
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


    def getModelByRequest(self, request):
        model_name = self.__getModelName(request)

        model_path = f"{self.__module_path}/models/{model_name}"
 
        return self._import_model(model_path)

    def getDataSetByRequest(self, request):
        model_name = self.__getModelName(request)

        dataset_path = f"{self.__module_path}/models/{model_name}/dataset.csv"
 
        return self._import_data_set(dataset_path)

    def retrain(self, directory_path): #return (bool, model)
        (is_imported, data_set) = self._import_data_set(f'{directory_path}/dataset.csv')

        if (is_imported == False):
            # todo: возврат исключения
            print("Ошибка импорта")
            return

        (is_overfitting, model) = self._overfitting(data_set)

        if (is_overfitting == False):
            # todo: возврат исключения
            print("Ошибка обучения")
            return

        self._save_model(model, directory_path)

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
    def _import_data_set(self, directory_path): # return (bool, data_set)
        pass

    
    def __getModelName(self, request):
        # получение access-токена
                authorization_header = request.headers.get('Authorization')

                if (authorization_header is None):
                    return None

                _, _, token = authorization_header.partition(" ")

                user_uid = jwtAuth.decodeToken(token)['userUid']

                if (user_uid is None):
                    return None

                # проверка существование переобученной модели для данного пользователя
                return 'default' if os.path.isdir(f"{self.__module_path}/models/{user_uid}") == False else user_uid;