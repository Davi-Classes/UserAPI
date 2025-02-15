import db
from fastapi import FastAPI, HTTPException, status
from models import User
from schemas import MessageOut, UserIn, UserOut


app = FastAPI(
    title='User API',
    description='Api para gerenciar usuários'
)


@app.get('/users')
def get_all_users() -> list[UserOut]:
    users = db.get_all_users()

    if len(users) == 0:
        raise HTTPException(status.HTTP_204_NO_CONTENT)

    return users


@app.get('/users/{id}')
def get_user_by_id(id: str) -> UserOut:
    user = db.get_user_by_id(id)

    if user is None:
        raise HTTPException(
            detail='Usuário não encontrado',
            status_code=status.HTTP_404_NOT_FOUND
        )
    
    return user


@app.post('/users', status_code=status.HTTP_201_CREATED)
def create_new_users(user_in: UserIn):
    exist_user = db.get_user_by_email(user_in.email)

    if exist_user is not None:
        raise HTTPException(
            detail='Já existe um usuário cadastrado com esse email',
            status_code=status.HTTP_400_BAD_REQUEST
        )

    new_user = User(**user_in.model_dump())
    db.create_new_user(new_user)
    return MessageOut(message='Usuário Cadastrado com Sucesso.')


@app.put('/users/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_user(id: str, user_in: UserIn):
    user = db.get_user_by_id(id)

    if user is None:
        raise HTTPException(
            detail='Usuário não encontrado',
            status_code=status.HTTP_404_NOT_FOUND
        )
    
    exist_user = db.get_user_by_email(user_in.email)
    if exist_user is not None and exist_user.id != user.id:
        raise HTTPException(
            detail='Já existe um usuário cadastrado com esse email',
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    user.name = user_in.name
    user.email = user_in.email
    user.password = user_in.password

    db.update_user(user)
    return MessageOut(message='Usuário atualizado com sucesso.')


@app.delete('/users/{id}', status_code=status.HTTP_202_ACCEPTED)
def delete_user(id: str):
    user = db.get_user_by_id(id)

    if user is None:
        raise HTTPException(
            detail='Usuário não encontrado',
            status_code=status.HTTP_404_NOT_FOUND
        )
    
    db.delete_user(id)
    return MessageOut(message='Usuário excluido com sucesso.')
