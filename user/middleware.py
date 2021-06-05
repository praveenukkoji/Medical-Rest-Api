import jwt
from django.http import JsonResponse
from medical.settings import SECRET_KEY


class IsAuthenticated(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_view(self, request, view_func, view_args, view_kwargs):
        try:
            if view_func.__name__ not in ('LoginView', 'LogoutView'):
                token = request.COOKIES.get('jwt')
                data = jwt.decode(token, SECRET_KEY, algorithms='HS256')
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
