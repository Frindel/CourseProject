import jwt
from bestconfig import Config
from datetime import datetime, timedelta
from secrets import token_urlsafe

config = Config()

PRIVATE_KEY = config["JwtAuthSettings.priveteKey"]
PUBLIC_KEY = config["JwtAuthSettings.publicKey"]
ALGORITHM = config["JwtAuthSettings.algorithm"]
LIVE_TIME = config["JwtAuthSettings.liveTime"]

ACCESS_TOKEN_TYPE = 'access'

def generateAccessToken(user_id: str) -> str:
    jwt_payload = {
        "userUid": user_id,
        "type": ACCESS_TOKEN_TYPE,
    }
    
    # установка времени выпуска и жизни токета
    now = datetime.utcnow()
    expire = now + timedelta(minutes= LIVE_TIME)

    jwt_payload["exp"] = expire
    jwt_payload["iat"] = now

    token = jwt.encode(jwt_payload, PRIVATE_KEY, algorithm=ALGORITHM)
    return token

def generateRefreshToken() -> str:
    token = token_urlsafe(128)
    
    return token

def decodeToken(token: str) -> dict:
    return jwt.decode(token, PUBLIC_KEY, algorithms=[ALGORITHM])