import requests
from config import settings

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# basic hash without secret
def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str):
    return pwd_context.verify(password, hashed_password)


def verify_email(email: str):
    # make get request to email api
    # if email is valid return true
    # https://api.hunter.io/v2/email-verifier?email=patrick@stripe.com&api_key=7d0831abe18dc13417dce1ff0467fee5b2bba095
    # Get Request to api.hunter.io
    url = f'https://api.hunter.io/v2/email-verifier?email={email}&api_key={settings.EMAIL_VERIFICATION_KEY}'
    resp = requests.get(url)
    # find in response
    if resp.json()['data']['result'] == 'deliverable':
        return True
    else:
        return False
    #


# check if user is logged in
# def is_logged_in(response: Response, Authorize: AuthJWT = Depends()):
#     Authorize.jwt_refresh_token_required()
#
#     user_id = Authorize.get_jwt_subject()
#     if not user_id:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
#                             detail='Could not refresh access token')
#     user = user_entity(User.find_one({'_id': ObjectId(str(user_id))}))
#     if not user:
#     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
#                         detail='The user belonging to this token no logger exist')
#     if request.cookies.get('logged_in'):
#         return True
#     else:
#         return False
