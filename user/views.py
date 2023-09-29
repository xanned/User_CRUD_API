from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, UserManager
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from user.serializer import UserSerializer


class UserViewSet(ModelViewSet):
    search = openapi.Parameter('search', openapi.IN_QUERY,
                               description="Поиск пользователя по имени",
                               type=openapi.TYPE_STRING)
    order_by = openapi.Parameter('order_by', openapi.IN_QUERY,
                                 description="Сортировка по имени",
                                 type=openapi.TYPE_BOOLEAN)

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    objects = UserManager()
    serializer_class = UserSerializer

    # queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        request.data['password'] = make_password(request.data['password'])
        response = super().create(request)
        return response

    @swagger_auto_schema(manual_parameters=[search, order_by])
    def list(self, request, search=None, *args, **kwargs):
        response = super().list(request, search, *args, **kwargs)
        return response

    def get_queryset(self):
        queryset = User.objects.all()
        search = self.request.query_params.get('search', None)
        order_by = self.request.query_params.get('order_by', None)
        if search:
            queryset = User.objects.filter(username__contains=search)
        if order_by == 'true':
            queryset = queryset.order_by('username')
        return queryset
