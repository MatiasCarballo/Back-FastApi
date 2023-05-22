
def user_schema(user) -> dict:
    return {"id": str(user["_id"]),
            "name": user["name"],
            "mail": user["mail"],
            "age": user["age"]}

def users_schema(users) -> list:
    return [user_schema(user) for user in users]