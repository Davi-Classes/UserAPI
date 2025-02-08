import db
from fastapi import FastAPI, HTTPException, status
from models import User
from schemas import UserIn, UserOut


app = FastAPI()


@app.get('/users')
def get_all_users() -> list[UserOut]:
    users = db.get_all_users()

    if len(users) == 0:
        raise HTTPException(status.HTTP_204_NO_CONTENT)

    return users


@app.post('/users')
def create_new_users(user: UserIn):
    exist_user = db.get_by_email(user.email)

    if exist_user is not None:
        raise HTTPException(
            detail='Já existe um usuário cadastrado com esse email',
            status_code=status.HTTP_400_BAD_REQUEST
        )

    new_user = User(**user.model_dump())
    db.create_new_user(new_user)
    return { 'message': 'Usuário Cadastrado com Sucesso.'}
