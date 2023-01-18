import random
from bson.objectid import ObjectId
from fastapi import APIRouter, status, Depends, HTTPException
from app.db_scheme import *
from app.db_conn import User, Post, Red
from app import auth2
from app.serializers import *

router = APIRouter()


@router.post('/create_post', status_code=status.HTTP_201_CREATED, response_model=PostResponse)
async def create_post(payload: CreatePostSchema, user_id: str = Depends(auth2.require_user)):
    user = user_response_entity(User.find_one({'_id': ObjectId(str(user_id))}))
    payload.user = user["email"]
    payload.created_at = datetime.utcnow()
    payload.updated_at = payload.created_at
    result = Post.insert_one(payload.dict())
    print(result.inserted_id)
    new_post = post_response_entity(Post.find_one({'_id': result.inserted_id}))
    print(new_post)
    return {"status": "success", "post": new_post}


@router.post('/get_by_id', status_code=status.HTTP_200_OK, response_model=PostResponse)
async def get_posts(payload: GetPostSchema, user_id: str = Depends(auth2.require_user)):
    # user = user_response_entity(User.find_one({'_id': ObjectId(str(user_id))}))
    post = generic_post_check(payload.id)
    return {"status": "success", "post": post}


@router.post('/edit', status_code=status.HTTP_200_OK, response_model=PostResponse)
async def edit_post(payload: EditPostSchema, user_id: str = Depends(auth2.require_user)):
    user = user_response_entity(User.find_one({'_id': ObjectId(str(user_id))}))
    old_post = generic_post_check(payload.id)
    if old_post["user"] != user["email"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='You are not authorized to edit this post')
    payload.updated_at = datetime.utcnow()
    payload.created_at = old_post["created_at"]
    payload.user = old_post["user"]
    payload.likes = old_post["likes"]
    payload.dislikes = old_post["dislikes"]
    Post.update_one({'_id': ObjectId(str(payload.id))}, {'$set': payload.dict()})
    new_post = post_response_entity(Post.find_one({'_id': ObjectId(str(payload.id))}))
    return {"status": "success", "post": new_post}


@router.post('/delete', status_code=status.HTTP_200_OK, )
async def delete_post(payload: DeletePostSchema, user_id: str = Depends(auth2.require_user)):
    user = user_response_entity(User.find_one({'_id': ObjectId(str(user_id))}))
    post = generic_post_check(payload.id)
    if post["user"] != user["email"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='You are not authorized to delete this post')
    Post.delete_one({'_id': ObjectId(str(payload.id))})
    return {"status": "success", "Deleted post id": str(payload.id)}


@router.post('/like', status_code=status.HTTP_200_OK)
async def like_post(payload: AddLikeSchema, user_id: str = Depends(auth2.require_user)):
    user = user_response_entity(User.find_one({'_id': ObjectId(str(user_id))}))
    post = generic_post_check(payload.id)
    if post["user"] == user["email"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='You Cannot like your own post')
    if user["email"] in post["likes"]:
        push_action_to_redis(user["email"], payload.id, "like")
        Post.update_one({'_id': ObjectId(str(payload.id))}, {'$pull': {'likes': user["email"]}})
    else:
        push_action_to_redis(user["email"], payload.id, "remove like")
        Post.update_one({'_id': ObjectId(str(payload.id))}, {'$push': {'likes': user["email"]}})
    return {"status": "success"}


@router.post('/dislike', status_code=status.HTTP_200_OK)
async def dislike_post(payload: AddDislikeSchema, user_id: str = Depends(auth2.require_user)):
    user = user_response_entity(User.find_one({'_id': ObjectId(str(user_id))}))
    post = generic_post_check(payload.id)
    if post["user"] == user["email"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='You Cannot dislike your own post')
    if user["email"] in post["dislikes"]:
        push_action_to_redis(user["email"], payload.id, "dislike")
        Post.update_one({'_id': ObjectId(str(payload.id))}, {'$pull': {'dislikes': user["email"]}})
    else:
        push_action_to_redis(user["email"], payload.id, "remove dislike")
        Post.update_one({'_id': ObjectId(str(payload.id))}, {'$push': {'dislikes': user["email"]}})
    return {"status": "success"}


@router.get('/get_all_your_actions', status_code=status.HTTP_200_OK)
async def get_all_redis_actions(user_id: str = Depends(auth2.require_user)):
    user = user_response_entity(User.find_one({'_id': ObjectId(str(user_id))}))
    return {"status": "success", "actions": get_all_actions_from_redis(user["email"])}


def get_all_actions_from_redis(user_email):
    actions = []
    for key in Red.scan_iter("user:" + user_email + ":*"):
        action = Red.get(key)
        action = action.decode("utf-8")
        actions.append(action)
    return actions


def push_action_to_redis(email, post_id, act):
    # action = UserActionToRedis(email, post_id, act)
    who_where = f'user:{email}:where:{post_id} act_id:{random.randrange(0, 999999)}'
    # new json var email, post_id, act, time
    json_info = json.dumps({"email": email, "post_id": post_id, "act": act, "time": datetime.utcnow().isoformat()})
    Red.set(who_where, json_info)


def generic_post_check(post_id):
    # validate post Object id
    try:
        post_id = ObjectId(str(post_id))
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid post id')
    post = Post.find_one({'_id': ObjectId(str(post_id))})
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Post not found')
    return post_response_entity(post)
