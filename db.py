from tinydb import TinyDB, Query
from models import User


db = TinyDB('./database.json', indent=2)


def get_all_users() -> list[User]:
    users = db.table('users').all()
    return [User(**user) for user in users]


def get_by_email(email: str) -> User | None:
    QUser = Query()
    result = db.table('users').search(QUser.email == email)
    
    if len(result) == 0:
        return None
    
    return User(**result[0])

def create_new_user(user: User) -> None:
    user_document = user.model_dump()
    
    user_document.update({
        'id': str(user.id),
        'created_at': user.created_at.isoformat()
    })
    
    db.table('users').insert(user_document)