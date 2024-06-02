import os
import importlib
import sys
import secrets

from fastapi import FastAPI, Header, Body, WebSocket, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt import InvalidTokenError

from api.common.DbAdapter import DbAdapter
import jwtAuth


# создание экземпляра приложения
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db_adapter = DbAdapter()

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

# регистрация пользователя
@app.get('/api/v1/register')
def register():
    # генерация refresh-токена
    refresh_token = jwtAuth.generateRefreshToken()

    # todo: создание пользователя и сохранение в БД
    user_id = db_adapter.request(f'INSERT INTO users (refresh_token) VALUES (\'{refresh_token}\') RETURNING id')[0][0]

    # генерация access-токена
    access_token = jwtAuth.generateAccessToken(user_id)

    return JSONResponse(content= {
        "accessToken": access_token,
        "refreshToken": refresh_token
    })

@app.post('/api/v1/update-access-token')
def updateAccessToken(body = Body()):
    # получение refresh-токена
    refresh_token = body.get('refreshToken')

    if refresh_token is None:
        return JSONResponse(content = {"error": "refresh token not set"}, status_code= 400)

    # поиск пользователя в БД и провера refresh-токена
    sql_result = db_adapter.request(f'SELECT id FROM users WHERE refresh_token = \'{refresh_token}\'')

    if (sql_result is None):
        return JSONResponse(content = {"error": "refresh token is not valid"}, status_code= 400)

    user_id = sql_result[0][0]

    # генерация новых токенов
    new_refresh_token = jwtAuth.generateRefreshToken()
    new_access_token = jwtAuth.generateAccessToken(user_id)

    # сохранение нового refresh-токена в БД
    db_adapter.request(f"UPDATE users SET refresh_token = (\'{new_refresh_token}\') WHERE id = {user_id}")
    
    return JSONResponse(content= {
        "accessToken": new_access_token,
        "refreshToken": new_refresh_token
    })

@app.get('/api/v1/modules')
def getModules():
    modules_info = [ {'name': module.name, 'niceName': module.nice_name, 'description': module.description} for
                 module in modules.values()]
    
    return modules_info


# создание путей переобучения для модулей
for (name, module_obj) in modules.items():

    module_name = name;
    
    async def overfitting(websocket: WebSocket):

        async def returnStepStatus(step_name: str, isSuccess: bool):
            message = {
               'stage': step_name,
                'isSuccess': isSuccess
            }
            await websocket.send_json(message)

        await websocket.accept()

        # получение access-токена
        token = await websocket.receive_text()

        # получение id пользователя
        try:
            user_id = jwtAuth.decodeToken(token)['userUid']
            await returnStepStatus('geting token', True)
        except InvalidTokenError as e:
            await returnStepStatus('getting token', False)
            await websocket.close()
            return
        
        # опеделение пути к датасету
        dataset_dir = f'{current_directory}/modules/{module_name}/models/{user_id}'
        
        # получение датасета
        dataset = await websocket.receive_bytes()

        # сохранение датасета
        os.makedirs(dataset_dir, exist_ok=True)
        with open(f"{dataset_dir}/dataset.csv", 'wb+') as f:
            f.write(dataset)

        # for test
        if (module_name =='simple'):
            await websocket.close()
            return;

        # переобучение
        isSuccess, _ = modules[module_name].retrain(f"{dataset_dir}/dataset.csv")

        await websocket.close()
        return

        # получение access-токена
        access_token = websocket.headers.get('Sec-WebSocket-Protocol')
        if (access_token is None):
            await websocket.close(401)
            return

        try:
            # получение id пользователя
            user_id = jwtAuth.decodeToken(access_token)['userUid']
            await websocket.send_text("yes")
        except InvalidTokenError as e:
            await websocket.close(401)
            return
        
        file_path = f'{current_directory}/modules/{module_name}/models/{user_id}/dataset.csv'

        # ожидание получения датасета
        dataset = await websocket.receive_text()
        
        websocket.send_text("testr")
        websocket.close(200)
        return;

        # сохранение файла в папку пользователя
        file_path = f'{getModelRoute(user_id)}/dataset.csv'
        with open(file_path, 'wb') as f:
            f.write(dataset)
        
        websocket.send_json({'stage': 'import','isSuccess': True})

        # переобучение
        isSuccess, _ = modules[module_name].retrain(file_path)

        websocket.send_json({'stage': 'retrain','isSuccess': isSuccess})

        # todo: удаление файла при неуспешном переобучении

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


# db_adapter.request("DROP TABLE IF EXISTS users")
db_adapter.request("CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, refresh_token VARCHAR(256) UNIQUE NOT NULL)")
