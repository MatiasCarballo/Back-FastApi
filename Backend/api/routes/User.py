from fastapi import APIRouter, HTTPException, status
from db.models.user import User
from db.schemas.user import user_schema, users_schema
from db.Connection import db_client
from bson import ObjectId

router = APIRouter(prefix='/user')

@router.get('/')
async def user_all():
    return users_schema(db_client.users.find())

@router.get('/{id}')
async def hola(id:str):
    print(id)

@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def user(user: User):
    if type(search_user("mail", user.mail)) == User:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="El usuario ya existe")

    print()
    user_dict = dict(user) #se transforma en un diccionario para que mongo lo pueda entender 
    #del user_dict["id"] #delete "id"

    id = db_client.users.insert_one(user_dict).inserted_id #tomo el id que me da mongo
    new_user = user_schema(db_client.users.find_one({"_id": id})) # y por ultimo busco en db el nuevo user
    return User(**new_user)

@router.put('/{id}', response_model=User)
async def user(id:str ,user: User):
    user_dict = dict(user)
    print(user_dict)
    print(id)
    try:
        db_client.users.find_one_and_update({"_id": ObjectId(id)}, {"$set" :user_dict})
    except:
        return {"error": "No se ha actualizado el usuario"}
    
    return search_user("_id", ObjectId(id))


@router.delete('/{id}')
async def user_delete(id:str):
    db_client.users.find_one_and_delete({"_id": ObjectId(id)})
    return users_schema(db_client.users.find())

def search_user(field: str, key):

    try:
        user = db_client.users.find_one({field: key})
        return User(**user_schema(user))
    except:
        return {"error": "No se ha encontrado el usuario"}