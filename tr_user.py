from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

# fastapi, uvicorn[standard]- библиотеки

user_db = []
transactions_db = []

app = FastAPI()

# Создание модели данных User.
class User(BaseModel):
    username: str
    password: str
    email: str
    balance: float = 0.0
    
# Получение списка пользователей.
@app.get("/users/", response_model=List[User])
async def read_users():
    return user_db

# Получение пользователя по ID.
@app.get("/users/{user_id}", response_model=User)
async def read_user(user_id: int):
    if user_id < 0 and user_id > len(user_db)-1:
        raise HTTPException(status_code=404, detail="User not found")
    return user_db[user_id]

# Создание пользователя.
@app.post("/users/", response_model=User)
async def create_user(user: User):
    user_dict = user.dict()
    user_dict['balance'] = 0.0
    user_db.append(user_dict)
    return user_dict

# Обновление пользователя по ID.
@app.put("/users/{user_id}", response_model= User)
async def update_user(user_id: int, user: User):
    if user_id < 0 and user_id > len(user_db)-1:
        raise HTTPException(status_code=404, detail="User not found")
    user_dict = user.dict()
    user_db[user_id] = user_dict
    return user_dict

# Удаление пользователя по ID.
@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    if user_id < 0 and user_id > len(user_db)-1:
        raise HTTPException(status_code=404, detail="User not found")
    deleted_user = user_db.pop(user_id)
    return deleted_user

# Пополнение баланса по ID пользователя и добавление транзакции в базу данных.
@app.post("/deposit/{user_id}", response_model=User)
async def deposit(user_id: int, amount: float):
    
    if user_id < 0 and user_id > len(user_db)-1:
        raise HTTPException(status_code=404, detail="User not found")
    
    user_db[user_id]['balance'] += amount
    return user_db[user_id]

# Получение баланса по ID пользователя.
@app.get("/balance/{user_id}", response_model=float)
def get_balance(user_id: int):
    if user_id < 0 and user_id > len(user_db)-1:
        raise HTTPException(status_code=404, detail="User not found")
    return user_db[user_id]['balance']

# Снятие средств с баланса по ID пользователя и добавление транзакции в базу данных.
@app.put("/balance/{user_id}", response_model = User)
async def withdraw(user_id: int, amount: float):
    if user_id < 0 or user_id > len(user_db)-1:
        raise HTTPException(status_code=404, detail="User not found")
    
    user = user_db[user_id]
    if user['balance'] < amount:
        raise HTTPException(status_code=400, detail="Insufficient funds")
    
    user['balance'] -= amount
    return user

# Выдача кредита по ID пользователя и добавление транзакции в базу данных.
@app.post("/credit/{user_id}", response_model = User)
async def credit(user_id: int, credit_limit: float):
    if user_id < 0 or user_id > len(user_db)-1:
        raise HTTPException(status_code=404, detail="User not found")
    
    if credit_limit<0:
        raise HTTPException(status_code=400, detail="Credit limit cannot be negative")
    
    if credit_limit < 999 and credit_limit > 100000:
        raise HTTPException(status_code=400, detail="Credit limit must be between 999 and 100000")
    user = user_db[user_id]
    try:
        if user['credit']>0 and user['credit']<100000:
            user['credit'] += credit_limit
            user['balance'] += credit_limit
            return user
        elif user['credit']== 0:
            user['credit'] = credit_limit
            user['balance'] += credit_limit
            return user
        else:
            raise HTTPException(status_code=400, detail="User already has a credit limit")
    except KeyError:
        user['credit'] = credit_limit
        user['balance'] += credit_limit
        return user
# Получение информации о кредите по ID пользователя.
@app.get("/credit/{user_id}", response_model=float)
async def get_credit(user_id: int):
    if user_id < 0 or user_id > len(user_db)-1:
        raise HTTPException(status_code=404, detail="User not found")
    user = user_db[user_id]
    try:
        return user_db[user_id]['credit']
    except KeyError:
        return 0.0
# Оплата кредита по ID пользователя и добавление транзакции в базу данных.
@app.get("/credit/payment/{user_id}", response_model=User)
async def pay_credit(user_id: int, amount: float):
    if user_id < 0 or user_id > len(user_db)-1:
        raise HTTPException(status_code=404, detail="User not found")
    user = user_db[user_id]
    try:
        if user["credit"]<= 0:
            raise HTTPException(status_code=400, detail="User does not have a credit")
        if user['credit'] < amount:
            raise HTTPException(status_code=400, detail="Insufficient funds")
        user['credit'] -= amount
        user['balance'] -= amount
        return user
    except KeyError:
        raise HTTPException(status_code=400, detail="User does not have a credit")
    
        

    