from pymongo import errors


async def get_user(db, username=None, email=None, include_id=True):
    return await db.users.find_one(
        {'email': email} if email else {'_id': username},
        projection={'_id': include_id})


async def insert_user(db, **kwobj):
    data = {'_id': kwobj.pop('username')}
    data.update(kwobj)
    data.setdefault("roles", [])
    data['roles'].append("reg")
    try:
        return await db.users.insert_one(data)
    except errors.DuplicateKeyError:
        return None


async def update_user(db, **kwobj):
    res = await db.users.update_one(
        {'_id': kwobj.pop('username')},
        {'$set': kwobj})
    return res.matched_count, res.modified_count

async def remove_user(db, username):
    return (await db.users.delete_one({'_id': username})).deleted_count or None
