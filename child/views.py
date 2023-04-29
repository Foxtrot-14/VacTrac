
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from account.serializers import *
from account.renderers import *
from rest_framework.permissions import IsAuthenticated

from vactrac.child.models import Due, Taken
from .serializers import *
from account.models import User

class AddChildView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        posts = Child.objects.filter(adder=request.user)
        if posts is None:
            return Response({'msg':'You Have not added any profiles'}, status = status.HTTP_404_NOT_FOUND)
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
    renderer_classes = [UserRenderer]
    def get_object(self, pk):
        try:
            return Child.objects.get(pk = pk)
        except Child.DoesNotExist:
            return None

    def get(self, request, pk, *args, **kwargs):
        child = self.get_object(pk)
        if child is None:
            return Response({'error': 'Child not found'}, status = status.HTTP_404_NOT_FOUND)
        if child:
            serializer = ChildSerializer(child)
            return Response(serializer.data, status = status.HTTP_200_OK)
        return Response({'error':'You are not authorized to access the information'}, status = status.HTTP_401_UNAUTHORIZED)

    def put(self, request, pk, *args, **kwargs):
        child = self.get_object(pk)
        if child is None:
            return Response({'error': 'Child not found'}, status = status.HTTP_404_NOT_FOUND)
        serializer = ChildSerializer(child, data = request.data, context={'user':request.user}, partial = True)
        if serializer.is_valid():
            if child.adder.id == request.user.id or request.user.type==2:
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

class AddDueAPIView(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [UserRenderer]
    
    def get(self, request, *args, **kwargs):
        posts = Due.objects.filter(child=request.child)
        if posts is None:
            return Response({'msg':'You Have not added any profiles'}, status = status.HTTP_404_NOT_FOUND)
        serializer = ChildSerializer(posts, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        serializer = DueSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'All dues added'}, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class DueDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [UserRenderer]
    
    def get_object(self, pk):
        try:
            return Due.objects.get(pk = pk)
        except Due.DoesNotExist:
            return None
        
    def get(self, request, pk, *args, **kwargs):
        due = self.get_object(pk)
        if due is None:
            return Response({'error': 'Due not found'}, status = status.HTTP_404_NOT_FOUND)
        if due:
            serializer = DueSerializer(due)
            return Response(serializer.data, status = status.HTTP_200_OK)
        return Response({'error':'You are not authorized to access the information'}, status = status.HTTP_401_UNAUTHORIZED)
    
    def put(self, request, pk, *args, **kwargs):
        due = self.get_object(pk)
        if due is None:
            return Response({'error': 'due not found'}, status = status.HTTP_404_NOT_FOUND)
        serializer = DueSerializer(due, data = request.data, partial = True)
        if serializer.is_valid():
            if request.user.type==2:
                serializer.save()
                return Response(serializer.data, status = status.HTTP_200_OK)
            return Response({"error": "You are not authorized to edit the details"}, status = status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class AddTakenAPIView(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [UserRenderer]
    
    def get(self, request, *args, **kwargs):
        taken = Taken.objects.filter(child=request.child)
        if taken is None:
            return Response({'msg':'No vaccines taken so far'}, status = status.HTTP_404_NOT_FOUND)
        serializer = TakenSerializer(taken, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        serializer = TakenSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'All dues added'}, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
class TakenAPIDetail(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    
    def get_object(self, pk):
        try:
            return Taken.objects.get(pk = pk)
        except Taken.DoesNotExist:
            return None
        
    def get(self, request, pk, *args, **kwargs):
        taken = self.get_object(pk)
        if taken is None:
            return Response({'error': 'Event not found'}, status = status.HTTP_404_NOT_FOUND)
        if taken:
            serializer = TakenSerializer(taken)
            return Response(serializer.data, status = status.HTTP_200_OK)
        return Response({'error':'You are not authorized to access the information'}, status = status.HTTP_401_UNAUTHORIZED)
    
    def put(self, request, pk, *args, **kwargs):
        taken = self.get_object(pk)
        if taken is None:
            return Response({'error': 'event not found'}, status = status.HTTP_404_NOT_FOUND)
        serializer = TakenSerializer(taken, data = request.data, partial = True)
        if serializer.is_valid():
            if request.user.type==2:
                serializer.save()
                return Response(serializer.data, status = status.HTTP_200_OK)
            return Response({"error": "You are not authorized to edit the details"}, status = status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)