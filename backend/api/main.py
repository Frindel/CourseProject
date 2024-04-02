from fastapi import FastAPI
import os
import importlib
import sys
import secrets
from fastapi.middleware.cors import CORSMiddleware

# создание экземпляра приложения
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

current_file = os.path.realpath(__file__)
current_directory = os.path.dirname(current_file)

sys.path.append(f'{current_directory}/common')

# подключение модулей
modules = {}
for module_name in os.listdir(f'{current_directory}/modules'):
        
        # Импортируем модуль
        sys.path.append(f'{current_directory}/modules/simple')
        module = importlib.import_module(f'modules.{module_name}')
        module_obj = module.init(module_name, app)

        # сохранение модуля
        modules[module_name] = module_obj

# определение базовых методов api

@app.get('/api/v1/authorization')
def authorization(): 
    token = secrets.token_urlsafe(128)
    
    return {'token': token}

@app.get('/api/v1/modules')
def getModules():
    modules_info = [ {'name': module.name, 'niceName': module.nice_name, 'description': module.description} for
                 module in modules.values()]
    
    return modules_info

getModules()

# создание путей переобучения для модулей
# возможен перенос в ModuleBase
for (name, module_obj) in modules.items():

    async def overfitting():
        # todo: получение id пользователя
        # todo: сохранение файла в папку пользователя
        # todo: переобучение

        return name

    app.add_api_route(f"/api/v1/{name}/overfitting", overfitting, methods=['GET'])