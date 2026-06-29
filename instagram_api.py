import requests
from requests.auth import HTTPBasicAuth
from config import BOXAPI_USERNAME, BOXAPI_PASSWORD


def get_profile(username: str):
    url = "https://boxapi.ir/api/instagram/user/get_web_profile_info"

    response = requests.post(
        url,
        json={"username": username},
        auth=HTTPBasicAuth(BOXAPI_USERNAME, BOXAPI_PASSWORD),
        timeout=10,
    )
    response.raise_for_status()

    try:
        return response.json()["response"]["body"]["data"]["user"]
    except (KeyError, TypeError):
        raise ValueError("Unexpected API response format")


def get_stories(username: str):
    user_profile = get_profile(username)
    try:
        user_id = str(user_profile["id"])
    except KeyError:
        raise Exception(f"Unexpected profile response structure: {user_profile}")

    url = "https://boxapi.ir/api/instagram/user/get_stories"
    response = requests.post(
        url,
        json={"ids": [user_id]},
        auth=HTTPBasicAuth(BOXAPI_USERNAME, BOXAPI_PASSWORD),
        timeout=10,
    )
    response.raise_for_status()
    try:
        user_stories = response.json()["response"]["body"]["reels"]
        if not user_stories:
            return []
        return user_stories[user_id]["items"]
    except (KeyError, TypeError):
        raise ValueError("Unexpected API response format")


def get_medias(username: str):
    url = "https://boxapi.ir/api/instagram/user/get_media_by_username"
    response = requests.post(
        url,
        json={"username": username, "count": 12},
        auth=HTTPBasicAuth(BOXAPI_USERNAME, BOXAPI_PASSWORD),
        timeout=10,
    )
    response.raise_for_status()
    try:
        return response.json()["response"]["body"]["items"]
    except (KeyError, TypeError):
        raise ValueError("Unexpected API response format")
