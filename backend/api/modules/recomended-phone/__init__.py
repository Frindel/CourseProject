from recomendedPhone import RecomendedPhone
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Body, HTTPException, Request, Query
import pandas as pd

SimpleModuleApp = None

def init(module_name, app):
    global SimpleModuleApp
    nice_name = "Рекомендации телефонов"
    description = 'Вам необходимо пройти опрос, по результатам опроса программа выдаст вам список телефонов подходящих по описанию. Вам необязательно заполнять все ячейки при прохождении опроса.'

    module = RecomendedPhone(module_name, nice_name, app, description)
    SimpleModuleApp = module
    database = module.database

    res = database.request("SELECT 'Hello world!'")

    print(res)
    # определение маршрутов api и другой бизнес-логики
    app.add_api_route(f"/api/v1/recomended-phone/years-statistics", yearsStatistics, methods=['GET'])
    app.add_api_route(f"/api/v1/recomended-phone/price-statistics", priceStatistics, methods=['GET'])
    app.add_api_route(f"/api/v1/recomended-phone/search", searhcPhone, methods=['GET'])
    
    return module

def yearsStatistics(request: Request):
    data_set = SimpleModuleApp.getDataSetByRequest(request)[1]

    genre_counts = data_set['Release'].value_counts().reset_index()
    genre_counts.columns = ['Release', 'Count']
    genre_counts = genre_counts.to_dict(orient='records')
    return JSONResponse(genre_counts)

def priceStatistics(request: Request):
    data_set = SimpleModuleApp.getDataSetByRequest(request)[1]

    # Определение диапазонов цен с шагом в 20000
    price_bins = list(range(0, data_set['Price'].max() + 25000, 25000))
    price_labels = [f'{price_bins[i]}-{price_bins[i+1]}' for i in range(len(price_bins) - 1)]

    # Создание столбца с диапазонами цен
    data_set['Price Range'] = pd.cut(data_set['Price'], bins=price_bins, labels=price_labels, right=False)

    # Подсчет количества моделей телефонов по каждому диапазону цен
    price_range_counts = data_set['Price Range'].value_counts().reset_index()
    price_range_counts.columns = ['Диапазон цен', 'Количество моделей']

    # Сортировка данных по диапазонам цен
    price_range_counts = price_range_counts.sort_values('Диапазон цен')
    
    # Преобразование данных в словарь и возврат в формате JSON
    price_range_counts = price_range_counts.to_dict(orient='records')
    return JSONResponse(price_range_counts)

def parse_range(range_str):
    if isinstance(range_str, str):
        range_list = list(map(int, range_str.split('-')))
        if len(range_list) == 1:  # Если пользователь ввел только одно значение
            return 0, range_list[0]  # Телефон подбирается от 0 до указанной суммы
        return range_list[0], range_list[1]
    return range_str, range_str

def searhcPhone(request: Request, 
                osClass: int= Query(-1), 
                priceRange: str = Query("0-10000000"), 
                batteryCapacity: str = Query("0-10000"), 
                operativeMemory: str =Query(""),
                internalMemory: str = Query("")):
    df = SimpleModuleApp.getDataSetByRequest(request)[1]
    
    os_class = osClass
    price_min, price_max = parse_range(priceRange)
    battery_min, battery_max = parse_range(batteryCapacity)
    
    # Обработка оперативной памяти
    operative_memory_str = operativeMemory
    if operative_memory_str:
        operative_memory_min, operative_memory_max = parse_range(operative_memory_str)
    else:
        operative_memory_min, operative_memory_max = 0, 1000  # По умолчанию от 0 до 1000
    
    # Обработка внутренней памяти
    internal_memory_str = internalMemory
    if internal_memory_str:
        memory_min, memory_max = parse_range(internal_memory_str)
    else:
        memory_min, memory_max = 0, 10000  # По умолчанию от 0 до 10000

    filtered_df = df[
        ((df['os_class'] == os_class) | (os_class == -1)) &
        (df['Price'] >= price_min) & (df['Price'] <= price_max) &
        (
            ((battery_min == battery_max) & (df['Battery capacity (mAh)'] == battery_min)) |
            ((battery_min != battery_max) & (df['Battery capacity (mAh)'] >= battery_min) & (df['Battery capacity (mAh)'] <= battery_max))
        )&
        (
            ((operative_memory_min == operative_memory_max) & (df['RAM capacity (GB)'] == operative_memory_min)) |
            ((operative_memory_min != operative_memory_max) & (df['RAM capacity (GB)'] >= operative_memory_min) & (df['RAM capacity (GB)'] <= operative_memory_max))
        ) &
        (
            ((memory_min == memory_max) & (df['Built-in memory capacity (GB)'] == memory_min)) |
            ((memory_min != memory_max) & (df['Built-in memory capacity (GB)'] >= memory_min) & (df['Built-in memory capacity (GB)'] <= memory_max))
        )
    ]
    
    # Сортировка и выбор первых 15 записей
    sorted_df = filtered_df.sort_values(by='Price').head(15)
    
    # Возврат только модели и цены
    result = sorted_df[['Model', 'Price']].to_dict(orient='records')
    return result

def get_recommended_phone(data: dict = Body(...)):
    result = searhcPhone(data)
    return JSONResponse(content=result)
