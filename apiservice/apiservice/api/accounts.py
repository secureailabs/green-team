import json

from api.authentication import get_current_user, get_password_hash
from data import operations as data_service
from fastapi import APIRouter, Body, Depends, HTTPException, Path, status
from fastapi.encoders import jsonable_encoder
from models.accounts import (
    AddSocialMedia_In,
    GetMultipleUsers_Out,
    GetUsers_Out,
    RegisterUser_In,
    RegisterUser_Out,
    SocialMedia,
    Timeline,
    TimelineEvents_Db,
    User_Db,
    UserAccountState,
)
from models.authentication import TokenData
from models.common import PyObjectId
from utils import background_couroutines

DB_COLLECTION_USERS = "users"
DB_COLLECTION_VIDEOS = "videos"
DB_COLLECTION_TEXTS = "texts"
router = APIRouter()


@router.post(
    path="/api/users",
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
    path="/api/users",
    description="Get list of all the users",
    response_description="List of users",
    response_model=GetMultipleUsers_Out,
    response_model_by_alias=False,
    response_model_exclude_unset=True,
    status_code=status.HTTP_200_OK,
    operation_id="get_all_users",
)
async def get_all_users():
    users = await data_service.find_all(DB_COLLECTION_USERS)

    return GetMultipleUsers_Out(users=[GetUsers_Out(**user) for user in users])


@router.get(
    path="/api/users/{user_id}",
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
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return GetUsers_Out(**user)


@router.put(
    path="/api/users/{user_id}",
    description="Add a new social media handle",
    response_model_by_alias=False,
    response_model_exclude_unset=True,
    status_code=status.HTTP_204_NO_CONTENT,
    operation_id="set_user_handle",
)
async def set_user_handle(
    user_id: PyObjectId = Path(description="UUID of the requested user"),
    social_media_handle: AddSocialMedia_In = Body(description="Social media handle"),
    current_user: TokenData = Depends(get_current_user),
) -> None:
    user = await data_service.find_one(DB_COLLECTION_USERS, {"_id": str(user_id)})
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found")
    user = User_Db(**user)

    # Update the social media handle one by one
    for key in social_media_handle.social_media:
        user.social_media[key] = social_media_handle.social_media[key]

        if key is SocialMedia.TIKTOK:
            # Create a background task to scrape the social media handle and add it to database
            background_couroutines.add_async_task(scrape_social_media(user_id, social_media_handle.social_media[key]))

    await data_service.update_one(DB_COLLECTION_USERS, {"_id": str(user_id)}, {"$set": jsonable_encoder(user)})


async def scrape_social_media(user_id: PyObjectId, social_media_handle: str):

    # TODO: download all videos and get the path of the downloaded video as a list
    # read the list of videos from timeline.json file in the sample_data folder
    with open("sample_data/timeline.json", "r") as f:
        videos = json.load(f)
        videos = videos["timeline"]

    for video in videos:
        # Add the path of the scrapped video to the database
        event = TimelineEvents_Db(
            user_id=user_id,
            video_path=video["video_path"],
            video_content_url=video["video_content_url"],
            video_page_url=video["video_page_url"],
            timestamp=video["timestamp"],
            datestring=video["datestring"],
            text=video["text"],
            summary=video["summary"],
            title=video["title"],
        )

        await data_service.insert_one(
            DB_COLLECTION_VIDEOS,
            jsonable_encoder(event),
        )

        # Create a background task to extract the text from the video
        # background_couroutines.add_async_task(video_to_text(result.inserted_id, video["path"]))


# async def video_to_text(video_id: PyObjectId, video_path: str):
#     # TODO Convert video to wav audio file

#     # TODO Convert wav audio file to text
#     # Read the text from the file as a string
#     with open("sample_data/text1.txt", "r") as file:
#         result_text = file.read()

#     # TODO: Generate the summary of the text and the title
#     with open("sample_data/summary1.txt", "r") as file:
#         summary_text = file.read()
#     with open("sample_data/title1.txt", "r") as file:
#         title_text = file.read()

#     # Add the text to the database
#     response = await data_service.update_one(
#         DB_COLLECTION_VIDEOS,
#         {"_id": str(video_id)},
#         {"$set": {"text": result_text, "summary": summary_text, "title": title_text}},
#     )

#     if response.modified_count == 0:
#         raise Exception("Failed to update the video")


@router.get(
    path="/api/users/{user_id}/timeline",
    description="Get the timeline of a user sorted by date",
    response_model=Timeline,
    response_model_by_alias=False,
    response_model_exclude_unset=True,
    status_code=status.HTTP_200_OK,
    operation_id="get_user",
)
async def get_timeline(
    user_id: PyObjectId = Path(description="UUID of the requested user"),
    current_user: TokenData = Depends(get_current_user),
) -> Timeline:
    user = await data_service.find_one(DB_COLLECTION_USERS, {"_id": str(user_id)})
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    videos = await data_service.find_by_query(DB_COLLECTION_VIDEOS, {"user_id": str(user_id)})

    return Timeline(timeline=[TimelineEvents_Db(**video) for video in videos])
