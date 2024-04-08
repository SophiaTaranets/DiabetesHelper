from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed

from diabetes_helper.diabetes_app.models import User


def register_social_user(provider, user_id, email, username):
    filtered_user_by_email = User.objects.filter(email=email)

    if filtered_user_by_email.exists():
        if provider == filtered_user_by_email[0].auth-provider:
            registered_user = authenticate(
                email=email, password='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'
            )

            return {
                'username': registered_user.username,
                'email': registered_user.email,
                'tokens': registered_user.tokens()
            }

        else:
            raise AuthenticationFailed(
                detail='Please continue your login using' + filtered_user_by_email[0].auth_provider
            )

    else:
        u