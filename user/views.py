from rest_framework.generics import GenericAPIView
from django.http import JsonResponse
from rest_framework.response import Response
import json
from user.models import Role, User
from uuid import uuid4
from datetime import datetime, timedelta
from medical.settings import SECRET_KEY
import jwt
from passlib.hash import pbkdf2_sha256


# add user
class AddUserView(GenericAPIView):
    def post(self, requests):
        try:
            requests = json.load(requests)
            users = requests.get("users")
            for user in users:
                user_id = uuid4()
                user_name = user["user_name"]
                user_email = user["user_email"]
                user_password = pbkdf2_sha256.hash(user["user_password"])
                role = Role.objects.get(pk=user["role_id"])
                new_user = User(user_id=user_id, user_name=user_name, user_email=user_email,
                                user_password=user_password, role_id=role)
                new_user.save()

            response = {
                "message": "users created successfully"
            }
        except Exception as e:
            print(e)
            response = {"error": str(e)}
        return JsonResponse(response)


# get all user
class GetAllUserView(GenericAPIView):
    def post(self, requests):
        try:
            data = []
            users = User.objects.all()
            for user in users:
                data.append({
                    "user_id": user.user_id,
                    "user_name": user.user_name,
                    "user_email": user.user_email,
                    "role_type": user.role_id.role_type,
                })
            response = {
                "data": data
            }
        except Exception as e:
            print(e)
            response = {"error": str(e)}
        return JsonResponse(response)


# get user
class GetUserView(GenericAPIView):
    def post(self, requests):
        try:
            requests = json.load(requests)
            users = requests.get("users")
            data = []
            for user_id in users:
                user_obj = User.objects.get(pk=user_id)
                data.append({
                    "user_id": user_obj.user_id,
                    "user_name": user_obj.user_name,
                    "user_email": user_obj.user_email,
                    "role_id": user_obj.role_id.role_id
                })
            response = {
                "data": data
            }
        except Exception as e:
            print(e)
            response = {"error": str(e)}
        return JsonResponse(response)


# update user
class UpdateUserView(GenericAPIView):
    def post(self, requests):
        try:
            requests = json.load(requests)
            users = requests.get("users")
            update_data = {}
            for user in users:
                update_data["user_name"] = user["update"]["user_name"]
                update_data["user_email"] = user["update"]["user_email"]

                if user["update"]["user_password"] != "":
                    updated_password = pbkdf2_sha256.hash(user["update"]["user_password"])
                    update_data["user_password"] = updated_password

                User.objects.filter(pk=user["user_id"]).update(**update_data)
            response = {
                "message": "users updated successfully"
            }
        except Exception as e:
            print(e)
            response = {"error": str(e)}
        return JsonResponse(response)


# delete user
class DeleteUserView(GenericAPIView):
    def post(self, requests):
        try:
            requests = json.load(requests)
            users = requests.get("users")
            for user_id in users:
                user = User.objects.get(pk=user_id)
                user.delete()
            response = {
                "message": "users deleted successfully"
            }
        except Exception as e:
            print(e)
            response = {"error": str(e)}
        return JsonResponse(response)


# add role
class AddRoleView(GenericAPIView):
    def post(self, requests):
        try:
            requests = json.load(requests)
            roles = requests.get("roles")
            for role in roles:
                role_id = uuid4()
                role_type = role["role_type"]
                new_role = Role(role_id=role_id, role_type=role_type)
                new_role.save()

            response = {
                "message": "roles created successfully"
            }
        except Exception as e:
            print(e)
            response = {"error": str(e)}
        return JsonResponse(response)


# get all roles
class GetAllRoleView(GenericAPIView):
    def post(self, requests):
        try:
            data = []
            roles = Role.objects.all()
            for role in roles:
                data.append({
                    "role_id": role.role_id,
                    "role_type": role.role_type,
                })
            response = {
                "data": data
            }
        except Exception as e:
            print(e)
            response = {"error": str(e)}
        return JsonResponse(response)


# get role
class GetRoleView(GenericAPIView):
    def post(self, requests):
        try:
            requests = json.load(requests)
            roles = requests.get("roles")
            data = []
            for role_id in roles:
                role_obj = Role.objects.get(pk=role_id)
                data.append({
                    "role_id": role_obj.role_id,
                    "role_type": role_obj.role_type
                })
            response = {
                "data": data
            }
        except Exception as e:
            print(e)
            response = {"error": str(e)}
        return JsonResponse(response)


# update role
class UpdateRoleView(GenericAPIView):
    def post(self, requests):
        try:
            requests = json.load(requests)
            roles = requests.get("roles")
            for role in roles:
                Role.objects.filter(pk=role["role_id"]).update(**role["update"])
            response = {
                "message": "roles updated successfully"
            }
        except Exception as e:
            print(e)
            response = {"error": str(e)}
        return JsonResponse(response)


# delete role
class DeleteRoleView(GenericAPIView):
    def post(self, requests):
        try:
            requests = json.load(requests)
            roles = requests.get("roles")
            for role_id in roles:
                role = Role.objects.get(pk=role_id)
                role.delete()
            response = {
                "message": "roles deleted successfully"
            }
        except Exception as e:
            print(e)
            response = {"error": str(e)}
        return JsonResponse(response)


# login
class LoginView(GenericAPIView):
    def post(self, requests):
        try:
            requests = json.load(requests)
            user_email = requests.get("user_email")
            user_password = requests.get("user_password")

            user = User.objects.get(user_email=user_email)
            valid_password = pbkdf2_sha256.verify(user_password, user.user_password)
            if not valid_password:
                response = Response()
                data = {
                    "authenticated": False,
                    "message": "incorrect credentials"
                }
                response.data = data
                return response
            if user:
                token_generation_payload = {
                    "user_email": user_email,
                    "user_password": user_password,
                    "exp": datetime.utcnow() + timedelta(minutes=60),
                    "iat": datetime.utcnow()
                }
                token = jwt.encode(token_generation_payload, SECRET_KEY, algorithm='HS256')
                response = Response()
                response.set_cookie(key='jwt', value=token, httponly=True)
                data = {
                    "authenticated": True,
                    "user_id": user.user_id
                }
                response.data = data
            else:
                response = Response()
                data = {
                    "authenticated": False
                }
                response.data = data
        except Exception as e:
            print(e)
            response = JsonResponse({"error": str(e)})
        return response


# logout
class LogoutView(GenericAPIView):
    def post(self, requests):
        try:
            response = Response()
            response.delete_cookie('jwt')
            data = {
                "message": "user logged out successfully"
            }
            response.data = data
        except Exception as e:
            print(e)
            response = JsonResponse({"error": str(e)})
        return response
