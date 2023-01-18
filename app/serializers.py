import json


def user_entity(user) -> dict:
    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"],
        "password": user["password"],
        "created_at": user["created_at"],
        "updated_at": user["updated_at"]
    }


def user_response_entity(user) -> dict:
    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"],
        "created_at": user["created_at"],
        "updated_at": user["updated_at"]
    }


# def embedded_user_response(user) -> dict:
#     return {
#         "id": str(user["_id"]),
#         "name": user["name"],
#         "email": user["email"],
#     }
#

def user_list_entity(users) -> list:
    return [user_entity(user) for user in users]


# post entity
def post_entity(post) -> dict:
    return {
        "id": str(post["_id"]),
        "title": post["title"],
        "body": post["body"],
        "user_id": str(post["user_id"]),
        "created_at": post["created_at"],
        "updated_at": post["updated_at"]
    }


# post response entity
def post_response_entity(post) -> dict:
    return {
        "id": str(post["_id"]),
        "title": post["title"],
        "body": post["body"],
        "user": post["user"],
        "likes": post["likes"],
        "dislikes": post["dislikes"],
        "created_at": post["created_at"],
        "updated_at": post["updated_at"]
    }


# def action_to_rdb_entity(action) -> json:
#     return {
#         "user_id": action.user_id,
#         "post_id": action.post_id,
#         "action": action.action,
#         "time": action.time
#     }
