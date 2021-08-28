import logging

from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from decorators import require_params, is_valid_role
from vending_machine.models import User
from vending_machine.serializer.user_serializer import UserSerializer
from vending_machine.services.token_handler import expires_in, token_expire_handler
from vending_machine.views.exceptions import RequestBodyNotAcceptable


@api_view(["POST"])
@require_params(["username", "password", "email", "first_name", "last_name", "role", "deposit"])
def create_user(request):
    try:
        payload = request.data
        logging.info(payload)
        new_user = User.objects.create(
            username=payload["username"],
            email=payload["email"],
            first_name=payload["first_name"],
            last_name=payload["last_name"],
            is_active=True,
            role = payload['role'],
            deposit = payload['deposit']
        )
        new_user.set_password(payload["password"])
        new_user.save(update_fields=["password"])
        user = get_object_or_404(User, pk=new_user.id)
        serialized_user = UserSerializer(user)
        return Response(
            data={
                "data": serialized_user.data,
            },
            status=status.HTTP_201_CREATED,
        )

    except Exception as e:
        logging.info(e)
        return Response(
            data={"conflict": "User already exists."}, status=status.HTTP_409_CONFLICT
        )


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_user(request, user_id):
    payload = request.data
    u = get_object_or_404(User, pk=user_id)
    if 'first_name' in payload:
        u.first_name = payload['first_name']
    if 'last_name' in payload:
        u.last_name = payload['last_name']
    if 'email' in payload:
        u.email = payload['email']
    u.save(update_fields=["first_name", "last_name", "email"])
    return Response(status=status.HTTP_200_OK)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_user(request, user_id):
    u = get_object_or_404(User, pk=user_id)
    u.delete()
    return Response(status=status.HTTP_200_OK)



@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    serialized_user = UserSerializer(user)
    return Response(
        data={
            "data": serialized_user.data,
        },
        status=status.HTTP_200_OK,
    )


@api_view(["POST"])
@require_params(["username", "password"])
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    user = authenticate(username=username, password=password)
    if not user:
        return Response(
            {
                "errors": [
                    {"field": "detail", "message": "Invalid username/password."}
                ],
                "code": 2,
                "title": "UNAUTHENTICATED",
            },
            status=status.HTTP_401_UNAUTHORIZED,
        )
    token, _ = Token.objects.get_or_create(user=user)
    is_expired, token = token_expire_handler(token)
    serialized_user = UserSerializer(user)
    return Response(
        data={
            "data": {
                "user": serialized_user.data,
                "expires_in": expires_in(token),
                "token": token.key,
            }
        },
        status=status.HTTP_200_OK,
    )


@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def logout(request):
    user = request.user
    token = Token.objects.get(user=user)
    token.delete()
    return Response(status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
@is_valid_role('buyer')
@require_params(["deposit"])
def deposit_coins(request):
    deposit = request.data.get('deposit')
    if deposit not in [5, 10, 20, 50, 100]:
        raise RequestBodyNotAcceptable('you can only deposit 5,10,20,50,100 cents')
    request.user.deposit = deposit
    request.user.save()
    user = get_object_or_404(User, pk=request.user.id)
    serialized_user = UserSerializer(user)
    return Response(
        data={
            "data": serialized_user.data,
        },
        status=status.HTTP_200_OK,
    )


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
@is_valid_role('buyer')
def reset_deposit(request):
    request.user.deposit = 0
    request.user.save()
    user = get_object_or_404(User, pk=request.user.id)
    serialized_user = UserSerializer(user)
    return Response(
        data={
            "data": serialized_user.data,
        },
        status=status.HTTP_200_OK,
    )