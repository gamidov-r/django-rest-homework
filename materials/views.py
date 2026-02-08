from rest_framework import status
from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from materials.models import Course, Lesson, Subscription
from materials.serializers import CourseDetailSerializer, CourseSerializer, LessonDetailSerializer, LessonSerializer
from users.permissions import IsOwner, IsModer
from .paginations import CustomPagination

class LessonViewSet(ModelViewSet):
    queryset = Lesson.objects.all()
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.action == "retrieve":
            return LessonDetailSerializer
        return LessonSerializer

    def perform_create(self, serializer):
        lesson = serializer.save(owner=self.request.user)
        lesson.owner = self.request.user
        lesson.save()

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (~IsModer,)
        elif self.action in ["retrieve", "retrieve"]:
            self.permission_classes = (IsModer | IsOwner,)
        elif self.action == "destroy":
            self.permission_classes = (IsModer | ~IsOwner,)
        return super().get_permissions()


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CourseDetailSerializer
        return CourseSerializer

    def perform_create(self, serializer):
        course = serializer.save(owner=self.request.user)
        course.owner = self.request.user
        course.save()

    def get_permissions(self):
        if self.action in ("create", "destroy"):
            self.permission_classes = (~IsModer,)
        elif self.action in ("retrieve", "retrieve"):
            self.permission_classes = (IsModer,)
        return super().get_permissions()


class LessonCreateAPIView(CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (~IsModer | IsOwner, )

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()

class CourseCreateAPIView(CreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = (~IsModer, IsAuthenticated)

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()


class LessonListAPIView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModer]
    pagination_class = CustomPagination

class LessonRetrieveAPIView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsModer | IsOwner)


class LessonUpdateAPIView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsModer | IsOwner)


class LessonDestroyAPIView(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsOwner | ~IsModer)


class CourseListAPIView(ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsModer]
    pagination_class = CustomPagination


class CourseRetrieveAPIView(RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = (IsAuthenticated, IsModer | IsOwner)


class CourseUpdateAPIView(UpdateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = (IsAuthenticated, IsModer | IsOwner)


class CourseDestroyAPIView(DestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = (IsAuthenticated, IsOwner | ~IsModer)


class SubscribeView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, pk):
        course = Course.objects.get(id=pk)
        Subscription.objects.get_or_create(user=request.user, course=course)
        return Response({"detail": "subscribed"}, status=status.HTTP_201_CREATED)


class UnSubscribeView(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request, pk):
        Subscription.objects.filter(user=request.user, id=pk).delete()
        return Response({"detail": "unsubscribed"}, status=status.HTTP_204_NO_CONTENT)