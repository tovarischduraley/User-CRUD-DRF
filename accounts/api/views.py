from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import WriteOnlyUserSerializer, ReadOnlyUserSerializer


@api_view(['POST', 'GET'])
def api_users_view(request):
    if request.method == 'GET':
        data = []
        for user in User.objects.all():
            serializer = ReadOnlyUserSerializer(user)
            data.append(serializer.data)
        return Response(data)

    if request.method == 'POST':
        serializer = WriteOnlyUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            read_serializer = ReadOnlyUserSerializer(user)
            return Response(read_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def api_user_view(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ReadOnlyUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'PUT':
        serializer = WriteOnlyUserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.update(user,  request.data)
            read_serializer = ReadOnlyUserSerializer(user)
            return Response(read_serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'PATCH':
        serializer = WriteOnlyUserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.update(user, request.data)
            read_serializer = ReadOnlyUserSerializer(user)
            return Response(read_serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        operation = user.delete()
        if operation:
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"failure": "delete failed"})
