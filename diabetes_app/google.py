from google.auth.transport import requests
from google.oauth2 import id_token


class Google:

    @staticmethod
    def validate(auth_token):
        try:
            info = id_token.verify_oauth2_token(
                auth_token, requests.Request())

            if 'accounts.google.com' in info['iss']:
                return info
        except:
            return 'Token is either incorrect or has expired'
