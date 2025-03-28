from fastapi import HTTPException, Request

async def check_session(request: Request):
    guild_id = request.session.get("guild_id")
    channel_id = request.session.get("channel_id")
    user_id = request.session.get("user_id")

    if not guild_id or not channel_id or not user_id:
        raise HTTPException(status_code=401, detail="Session values missing")

    return
