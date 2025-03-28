import jwt
import datetime, time
from dotenv import load_dotenv
import os

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

def generate_token(guild_id, channel_id, user_id):
    payload = {
        "guild_id": guild_id,
        "channel_id": channel_id,
        "user_id": user_id,
        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=1)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def decode_token(token):
    try:
        info = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_info = {
            "guild_id": info["guild_id"],
            "channel_id": info["channel_id"],
            "user_id": info["user_id"]
        }
        return user_info
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
    except KeyError:
        return None

if __name__ == "__main__":
    print(generate_token(123456789, 987654321, 123456789))