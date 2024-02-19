from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import SignupSerializer, LogininSerializer
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model


User = get_user_model()


class SignupView(APIView):
    permission_classes = [AllowAny]  # Allow anyone to signup

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = serializer.save()
            return Response({'message': 'User created successfully.'}, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({'errors': e.args[0]}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LogininSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = serializer.validated_data['user']
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)

        except (ValidationError, serializer.ValidationError) as e:
            return Response({'errors': e.args[0]}, status=status.HTTP_400_BAD_REQUEST)

        except User.DoesNotExist:
            # Handle user not found (e.g., inactive account)
            return Response({'error': 'Invalid username'}, status=status.HTTP_401_UNAUTHORIZED)

        except Exception as e:
            return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
