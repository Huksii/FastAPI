from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

my_list = []

@app.get("/")
async def list_all():
    return {
        "message" : "List of all items",
        "data" : my_list,
        "status" : "success",
        "index" : f"from 0 to {len(my_list)-1}"
            }


@app.get("/item/{index}")
async def list_item(index: int):
    try:
        data = my_list[index]
    except IndexError:
        return {
            "message": "ошибка при получении",
            "status" : "error",
            "index" : f"имеются id от 0 до {len(my_list)-1}"
        }
    else:
        return {
            "message": "получение прошло успешно",
            "data": data,
            "status": "success",
        }


@app.post("/create/item/")
async def create_item(model: str, marka : str, year: Union[int, None] = None):
    data = {
        "model" : model,
        "marka" : marka,
        "year" : year,
    }
    my_list.append(data)
    return {
        "message": "item created",
        "data": data,
        "status": "success",
    }
    
    
@app.put("/update/item/{index}")
async def update_item(index: int, model: str, marka : str, year: Union[int, None] = None):
    data = {        
        "model" : model,
        "marka" : marka,
        "year" : year,
    }
    
    try:
        my_list[index] = data
    
    except IndexError:
        return {
            "message": "ошибка при обновлении",
            "status" : "error",
            "index" : f"имеются id от 0 до {len(my_list)-1}"
        }
    else:
        return {
            "message": "обновление прошло успешно",
            "data": data,
            "status": "success",
        }
        
        
@app.delete("/delete/item.{index}")
async def delete_item(index: int):
    try:
        data = my_list.pop(index)
    except IndexError:
        return{
            "message": "ошибка при удалении",
            "status" : "error",
            "index" : f"имеются id от 0 до {len(my_list)-1}"
        }
    else:
        return {
            "message": "удаление прошло успешно",
            "data": data,
            "status": "success",
        }