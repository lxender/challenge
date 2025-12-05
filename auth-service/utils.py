from fastapi import Header, HTTPException
from security import decode_access_token, hash_password
from db import get_user_by_id, update_user as db_update_user

# get_current_user be used as a dependency for fastapi routes
# It looks for the "Authorization" header and checks it token for validity
# If the token is valid, it returns the associated user from the database
def get_current_user(authorization: str = Header(...)):
    # Expects the header "Bearer <token>"
    try:
        token = authorization.split(" ")[1]
    except:
        raise HTTPException(status_code=401, detail="Invalid Authorization header")

    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    loginId = payload.get("sub")
    if not loginId:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    user = get_user_by_id(loginId)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user

def update_user(loginId: int, field: str, new_value: str):
    if field not in ["name", "email", "password"]:
        raise HTTPException(404, detail="Field not allowed to be changed")

    if field == "password":
        hashed = hash_password(new_value)
        db_update_user(loginId, field, hashed)

    db_update_user(loginId, field, new_value)