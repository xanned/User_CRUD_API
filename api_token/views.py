from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import authentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken

from api_token.serializers import Response201AuthTokenSerializer


class CustomAuthToken(ObtainAuthToken):
    authentication_classes = [authentication.BasicAuthentication]

    @swagger_auto_schema(responses={
        "201": openapi.Response(
            description=_("User has got Token"),
            schema=Response201AuthTokenSerializer,
        )
    })
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        response201 = Response201AuthTokenSerializer(data={"token": token.key, "user_id": user.pk})
        response201.is_valid(raise_exception=True)
        return JsonResponse(response201.data)
