from time import time

from data import operations as data_service
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from models.accounts import User_Db, UserInfo_Out
from models.authentication import LoginSuccess_Out, TokenData
from passlib.context import CryptContext
from utils.secrets import get_secret

DB_COLLECTION_USERS = "users"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter()

# Authentication settings
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 20
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_password_hash(salt, password):
    password_pepper = get_secret("password_pepper")
    return pwd_context.hash(f"{salt}{password}{password_pepper}")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, get_secret("jwt_secret"), algorithms=[ALGORITHM])
        token_data = TokenData(**payload)
        user_id = token_data.id
        if not user_id:
            raise credentials_exception
    except JWTError as exception:
        raise credentials_exception
    return token_data


@router.post(
    path="/login",
    description="User login with email and password",
    response_model=LoginSuccess_Out,
    response_model_by_alias=False,
    operation_id="login",
)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    exception_authentication_failed = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )

    found_user = await data_service.find_one(DB_COLLECTION_USERS, {"email": form_data.username})
    if not found_user:
        raise exception_authentication_failed

    found_user_db = User_Db(**found_user)
    password_pepper = get_secret("password_pepper")
    if not pwd_context.verify(
        f"{found_user_db.email}{form_data.password}{password_pepper}", found_user_db.hashed_password
    ):
        raise exception_authentication_failed

    token_data = TokenData(**found_user_db.dict(), exp=int((time() * 1000) + (ACCESS_TOKEN_EXPIRE_MINUTES * 60 * 1000)))

    access_token = jwt.encode(
        claims=jsonable_encoder(token_data),
        key=get_secret("jwt_secret"),
        algorithm=ALGORITHM,
    )

    return LoginSuccess_Out(access_token=access_token, token_type="bearer")


@router.get(
    path="/me",
    description="Get the current user information",
    response_description="The current user information",
    response_model=UserInfo_Out,
    response_model_by_alias=False,
    status_code=status.HTTP_200_OK,
    operation_id="get_current_user_info",
)
async def get_current_user_info(
    current_user: User_Db = Depends(get_current_user),
):
    found_user = await data_service.find_one(DB_COLLECTION_USERS, {"_id": str(current_user.id)})
    if not found_user:
        raise HTTPException(status_code=404, detail="User not found")
    found_user_db = User_Db(**found_user)

    return UserInfo_Out(**found_user_db.dict())
