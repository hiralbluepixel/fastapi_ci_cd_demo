from fastapi import FastAPI

app = FastAPI()
data={}

@app.get("/users")
def get_user():
    return data


@app.post("/users")
def create_user(name: str, age: int):
    user_id = len(data) + 1
    data[user_id] = {"name": name, "age": age}
    return {
        "user_id": user_id,
        "name": name,
        "age": age
    }


@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    if user_id in data:
        del data[user_id]
        return {
            "message": f"User {user_id} deleted successfully"
        }
    return {"message": "User not found"}