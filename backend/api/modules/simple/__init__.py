from simpleModule import SimpleModule

def init(module_name, app):

    nice_name = "Пример модуля"
    description = 'Описание примера модуля'

    module = SimpleModule(module_name, nice_name, app, description)
    
    database = module.database

    res = database.request("SELECT 'Hello world!'")

    print(res)
    # определение маршрутов api и другой бизнес-логики

    return module
    