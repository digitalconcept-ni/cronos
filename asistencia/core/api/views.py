from rest_framework.generics import ListAPIView, CreateAPIView

from core.api.serializers import UserSerializer, ClassroomSerializer
from core.registration.models import Classroom
from core.user.models import User


class UserListAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ClassroomAPIView(ListAPIView):
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer

class ClassroomCreateAPIView(CreateAPIView):
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer