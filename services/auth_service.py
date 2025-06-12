import jwt
from datetime import datetime, timedelta
import os

class AuthService:
    def __init__(self):
        self.secret_key = os.environ.get("SECRET_KEY", "fallback_secret")

    def generate_token(self, user_info):
        """
        生成 JWT
        :param user_info: 用户信息字典
        :return: JWT 字符串
        """
        payload = {
            "sub": "Notes login",
            "name": user_info.get("login"),
            "iat": int(datetime.now().timestamp()),
            "exp": int((datetime.now() + timedelta(hours=24)).timestamp())
        }
        return jwt.encode(payload, self.secret_key, algorithm="HS256")

    def verify_token(self, token):
        """
        验证 JWT
        :param token: JWT 字符串
        :return: 解码后的 payload 或 None（如果验证失败）
        """
        try:
            return jwt.decode(token, self.secret_key, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return None  # Token 过期
        except jwt.InvalidTokenError:
            return None  # Token 无效
