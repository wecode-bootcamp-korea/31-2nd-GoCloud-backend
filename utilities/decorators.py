import jwt

from django.conf import settings
from django.http import JsonResponse

from users.models import User

def check_token(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            access_token = request.headers.get('Authorization')
            payload      = jwt.decode(access_token, settings.SECRET_KEY, settings.ALGORITHM)
            request.user = User.objects.get(id=payload['id'])

        except jwt.InvalidSignatureError:
            return JsonResponse({'message': 'INVALID_SIGNATURE_ERROR'}, status=400)
        except jwt.exceptions.DecodeError:
            return JsonResponse({'message': 'DECODE_ERROR' }, status=400)
        except User.DoesNotExist:
            return JsonResponse({'message': 'USER_DOES_NOT_EXIST_ERROR'}, status=400)
        except jwt.ExpiredSignatureError:
            return JsonResponse({"message": "EXPIRED_TOKEN"}, status=400)

        return func(self, request, *args, **kwargs)
    return wrapper