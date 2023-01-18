from fastapi import APIRouter, Depends
from bson.objectid import ObjectId
from app.serializers import user_response_entity

from app.db_conn import User
from app import db_scheme, auth2

router = APIRouter()


@router.get('/me', response_model=db_scheme.UserResponse)
def get_me(user_id: str = Depends(auth2.require_user)):
    user = user_response_entity(User.find_one({'_id': ObjectId(str(user_id))}))
    return {"status": "success", "user": user}