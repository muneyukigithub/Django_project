from rest_framework import generics,permissions
from .models import Snippet
from .serializers import SnippetSerializer,UserSerializer
from django.contrib.auth.models import User
from .permissions import IsOwnerOrReadOnly
from rest_framework.decorators import api_view  # 追加
from rest_framework.response import Response  # 追加
from rest_framework.reverse import reverse  # 追加

@api_view(['GET'])  # 追加
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'snippets': reverse('snippet-list', request=request, format=format)
    })

class SnippetList(generics.ListCreateAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,) # 追加

    def perform_create(self, serializer): # 追加
        serializer.save(owner=self.request.user)

class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly
    ) # 追加

class UserList(generics.ListAPIView): # 追加
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView): # 追加
    queryset = User.objects.all()
    serializer_class = UserSerializer