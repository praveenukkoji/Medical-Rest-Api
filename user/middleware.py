import jwt
from django.http import JsonResponse
from rest_framework.response import Response

from medical.settings import SECRET_KEY
from . import authorization


class IsAuthenticated(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_view(self, request, view_func, view_args, view_kwargs):
        try:
            requested_view = view_func.__name__
            if requested_view not in ('LoginView', 'LogoutView'):
                token = request.COOKIES.get('jwt')
                data = jwt.decode(token, SECRET_KEY, algorithms='HS256')
                role_id = data['role_id']
                user_can_access_view = authorization.can_access(requested_view, role_id)
                if not user_can_access_view:
                    response = {
                        'message': 'Unauthorized Access'
                    }
                    return JsonResponse(response, status=405)
            return None
        except jwt.ExpiredSignatureError as jwt_error:
            print(jwt_error)
            response = {
                "error": str(jwt_error)
            }
        except Exception as e:
            print(e)
            response = {
                "error": str(e)
            }
        return JsonResponse(response)
