from rest_framework.generics import ListAPIView
from rest_framework.generics import RetrieveAPIView,RetrieveUpdateAPIView
from rest_framework.generics import UpdateAPIView
from rest_framework.generics import DestroyAPIView,CreateAPIView
from blog.models import *
from .serializers import *
from rest_framework.permissions import AllowAny,IsAuthenticated,IsAdminUser,IsAuthenticatedOrReadOnly
from .permissions import *

class bloglistAPIVIEW(ListAPIView):
    queryset = post.objects.all()
    serializer_class=postListSerializer

class blogdetailAPIVIEW(RetrieveAPIView):
    queryset = post.objects.all()
    serializer_class = postDetailSerializer
    lookup_field = 'slug'

class blogupdateAPIVIEW(RetrieveUpdateAPIView):
    queryset = post.objects.all()
    serializer_class = postCreateUpdateSerializer
    lookup_field = 'slug'
    permission_classes = [IsAuthenticatedOrReadOnly,OwnerorReadOnly]

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class blogdeleteAPIVIEW(DestroyAPIView):
    queryset = post.objects.all()
    serializer_class = postDetailSerializer
    lookup_field = 'slug'


class blogcreateAPIVIEW(CreateAPIView):
    queryset = post.objects.all()
    serializer_class = postCreateUpdateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
