from datetime import timedelta
from bson.objectid import ObjectId
from fastapi import APIRouter, Response, status, Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from app.db_scheme import *
import app.tools as tools
from app.db_conn import User
from config import settings
from app import auth2
from app.serializers import *
router = APIRouter()
ACCESS_TOKEN_EXPIRES_IN = settings.ACCESS_TOKEN_EXPIRES_IN
REFRESH_TOKEN_EXPIRES_IN = settings.REFRESH_TOKEN_EXPIRES_IN


@router.post('/register', status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def create_user(payload: CreateUserSchema):
    # Check if user exist
    user = User.find_one({'email': payload.email.lower()})
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail='Account already exist')
    # hunter.co Verification part
    # If user is not created yet, check email with hunter.io
    # else:
    #     if not tools.verify_email(payload.email):
    #         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
    #                             detail='Invalid email')
    #  Hash the password
    payload.password = tools.hash_password(payload.password)
    payload.email = payload.email.lower()
    payload.created_at = datetime.utcnow()
    payload.updated_at = payload.created_at
    result = User.insert_one(payload.dict())
    new_user = user_response_entity(User.find_one({'_id': result.inserted_id}))
    return {"status": "success", "user": new_user}


@router.post('/login')
def login(payload: LoginUserSchema, response: Response, Authorize: AuthJWT = Depends()):
    # Check if the user exist
    db_user = User.find_one({'email': payload.email.lower()})
    if not db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Incorrect Email or Password')
    user = user_entity(db_user)

    # Check if the password is valid
    if not tools.verify_password(payload.password, user['password']):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Incorrect Email or Password')

    # Create token
    access_token = Authorize.create_access_token(
        subject=str(user["id"]), expires_time=timedelta(minutes=ACCESS_TOKEN_EXPIRES_IN))

    # Refresh token
    refresh_token = Authorize.create_refresh_token(
        subject=str(user["id"]), expires_time=timedelta(minutes=REFRESH_TOKEN_EXPIRES_IN))

    # Storing Cookies
    response.set_cookie('access_token', access_token, ACCESS_TOKEN_EXPIRES_IN * 60,
                        ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, True, 'lax')
    response.set_cookie('refresh_token', refresh_token,
                        REFRESH_TOKEN_EXPIRES_IN * 60, REFRESH_TOKEN_EXPIRES_IN * 60, '/', None, False, True, 'lax')
    response.set_cookie('logged_in', 'True', ACCESS_TOKEN_EXPIRES_IN * 60,
                        ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, False, 'lax')

    # Send tokens back
    return {'status': 'success', 'access_token': access_token}


@router.get('/refresh')
def refresh_token(response: Response, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_refresh_token_required()

        user_id = Authorize.get_jwt_subject()
        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not refresh access token')
        user = user_entity(User.find_one({'_id': ObjectId(str(user_id))}))
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='The user belonging to this token no logger exist')
        access_token = Authorize.create_access_token(
            subject=str(user["id"]), expires_time=timedelta(minutes=ACCESS_TOKEN_EXPIRES_IN))
    except Exception as e:
        error = e.__class__.__name__
        if error == 'MissingTokenError':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail='Please provide refresh token')
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    response.set_cookie('access_token', access_token, ACCESS_TOKEN_EXPIRES_IN * 60,
                        ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, True, 'lax')
    response.set_cookie('logged_in', 'True', ACCESS_TOKEN_EXPIRES_IN * 60,
                        ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, False, 'lax')
    return {'access_token': access_token}


@router.get('/logout', status_code=status.HTTP_200_OK)
def logout(response: Response, Authorize: AuthJWT = Depends(), user_id: str = Depends(auth2.require_user)):
    Authorize.unset_jwt_cookies()
    response.set_cookie('logged_in', '', -1)

    return {'status': 'success'}


# if user logged in middleware
