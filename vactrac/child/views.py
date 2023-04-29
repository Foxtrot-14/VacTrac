
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from account.serializers import *
from account.renderers import *
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from account.models import User

class AddChildView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        posts = Child.objects.filter(adder=request.user)
        serializer = ChildSerializer(posts, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = ChildSerializer(data = request.data, context={'user':request.user})
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Child added'}, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class ChildDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Child.objects.get(pk = pk)
        except Child.DoesNotExist:
            return None

    def get(self, request, pk, *args, **kwargs):
        child = self.get_object(pk)
        if child is None:
            return Response({'error': 'Child not found'}, status = status.HTTP_404_NOT_FOUND)
        if child.adder.id==request.user.id or child.referred_to.id==request.user.id:
            serializer = ChildSerializer(child)
            return Response(serializer.data, status = status.HTTP_200_OK)
        return Response({'error':'You are not authorized to access the information'}, status = status.HTTP_401_UNAUTHORIZED)

    def put(self, request, pk, *args, **kwargs):
        child = self.get_object(pk)
        if child is None:
            return Response({'error': 'Child not found'}, status = status.HTTP_404_NOT_FOUND)
        serializer = ChildSerializer(child, data = request.data, context={'user':request.user}, partial = True)
        if serializer.is_valid():
            if child.adder.id == request.user.id or child.referred_to.id==request.user.id:
                serializer.save()
                return Response(serializer.data, status = status.HTTP_200_OK)
            return Response({"error": "You are not authorized to edit the details"}, status = status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        child = self.get_object(pk)
        if child is None:
            return Response({'error': 'Child not found'}, status = status.HTTP_404_NOT_FOUND)
        if child.adder.id == request.user.id:
            child.delete()
            return Response({"res": "Child deleted!"}, status = status.HTTP_200_OK)
        return Response({"error": "You are not authorized to delete the profile"}, status = status.HTTP_401_UNAUTHORIZED)