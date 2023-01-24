from api.authentication import get_current_user, get_password_hash
from data import operations as data_service
from fastapi import APIRouter, Body, Depends, HTTPException, Path, status
from fastapi.encoders import jsonable_encoder
from models.accounts import (
    GetMultipleUsers_Out,
    GetUsers_Out,
    RegisterUser_In,
    RegisterUser_Out,
    User_Db,
    UserAccountState,
)
from models.authentication import TokenData
from models.common import PyObjectId

DB_COLLECTION_USERS = "users"
router = APIRouter()


@router.post(
    path="/users",
    description="Register new user",
    response_description="User Id",
    response_model=RegisterUser_Out,
    response_model_by_alias=False,
    status_code=status.HTTP_201_CREATED,
    operation_id="register_user",
)
async def register_user(
    user: RegisterUser_In = Body(description="User details"),
):
    # Check if the user is already registered
    user_db = await data_service.find_one(DB_COLLECTION_USERS, {"email": user.email})
    if user_db:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already registered")

    # Create an admin user account
    user_db = User_Db(
        name=user.name,
        email=user.email,
        hashed_password=get_password_hash(user.email, user.password),
        account_state=UserAccountState.ACTIVE,
        avatar=user.avatar,
    )

    await data_service.insert_one(DB_COLLECTION_USERS, jsonable_encoder(user_db))

    return RegisterUser_Out(_id=user_db.id)


@router.get(
    path="/users",
    description="Get list of all the users",
    response_description="List of users",
    response_model=GetMultipleUsers_Out,
    response_model_by_alias=False,
    response_model_exclude_unset=True,
    status_code=status.HTTP_200_OK,
    operation_id="get_all_users",
)
async def get_all_users(current_user: TokenData = Depends(get_current_user)):
    users = await data_service.find_all(DB_COLLECTION_USERS)

    return GetMultipleUsers_Out(users=[GetUsers_Out(**user) for user in users])


@router.get(
    path="/users/{user_id}",
    description="Get the information about a user",
    response_model=GetUsers_Out,
    response_model_by_alias=False,
    response_model_exclude_unset=True,
    status_code=status.HTTP_200_OK,
    operation_id="get_user",
)
async def get_user(
    user_id: PyObjectId = Path(description="UUID of the requested user"),
    current_user: TokenData = Depends(get_current_user),
) -> GetUsers_Out:
    user = await data_service.find_one(DB_COLLECTION_USERS, {"_id": str(user_id)})
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found")

    return GetUsers_Out(**user)
