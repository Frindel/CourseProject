import os
import importlib
import sys
import secrets

from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi import FastAPI, Header, Body, WebSocket


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
current_directory = os.path.dirname(current_file) # дериктория файла main.py (текущего файла)

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

# создание путей переобучения для модулей
for (name, module_obj) in modules.items():

    module_name = name;
    async def overfitting(websocket: WebSocket, key: str | None = Header(default=None)):
        await websocket.accept()

        # проверка наличия id пользователя
        if (key is None):
             await websocket.close(400, JSONResponse(content={'error': 'user key not set'}).json())

        # ожидание получения датасета
        while True:
            data = await websocket.receive_bytes()
        
        

        # todo: сохранение файла в папку пользователя
        
        # todo: переобучение

        await websocket.close()

    # получение датасета модуля
    async def getModuleDateSet(key: str | None = Header(default=None)):

        # проверка переданного ключа
        if (key is None):
            return JSONResponse(content= {'error': 'user key not set'}, status_code=400)  

        # проверка существование переобученной модели для данного пользователя         
        model_name = 'default' if os.path.isdir(f"{current_directory}/modules/{module_name}/models/{key}") == False else key;
        
        file = FileResponse(f"{current_directory}/modules/{module_name}/models/{model_name}/dataset.csv", filename="dataset.csv")
        
        return file;
    
    # регистрация метода переобучения модуля
    app.add_api_websocket_route(f"/api/v1/{name}/overfitting", overfitting)

    # регистрация метода получения датасета модуля
    app.add_api_route(f"/api/v1/{name}/data-set", getModuleDateSet, methods=['GET'])
    
    