from simpleModule import SimpleModule

from fastapi import Request, FastAPI

module = None

def init(module_name, app):
    global module

    nice_name = "Пример модуля"
    description = 'Описание примера модуля'

    module = SimpleModule(module_name, nice_name, app, description)

    database = module.database

    res = database.request("SELECT 'Hello world!'")
    
    print(res)

    # определение маршрутов api и другой бизнес-логики
    setRoutes(app)

    return module

def setRoutes(app : FastAPI):
    app.add_api_route("/api/test", test, methods=['GET'])


# end points

async def test (request: Request):
    module.getDataSetByRequest(request)