from django.urls import path
from rest_framework.routers import DefaultRouter

from materials.apps import MaterialsConfig
from materials.views import (CourseCreateAPIView, CourseDestroyAPIView, CourseListAPIView, CourseRetrieveAPIView,
                             CourseUpdateAPIView, CourseViewSet, LessonCreateAPIView, LessonDestroyAPIView,
                             LessonListAPIView, LessonRetrieveAPIView, LessonUpdateAPIView, LessonViewSet)

app_name = MaterialsConfig.name


router = DefaultRouter()
router.register(r"courses", CourseViewSet)
router.register(r"lessons", LessonViewSet)

urlpatterns = [
    path("lessons/", LessonListAPIView.as_view(), name="lessons_list"),
    path("lessons/<int:pk>/", LessonRetrieveAPIView.as_view(), name="lessons_retrieve"),
    path("lessons/create/", LessonCreateAPIView.as_view(), name="lessons_create"),
    path("lessons/<int:pk>/delete/", LessonDestroyAPIView.as_view(), name="lessons_delete"),
    path("lessons/<int:pk>/update/", LessonUpdateAPIView.as_view(), name="lessons_update"),
    path("courses/", CourseListAPIView.as_view(), name="courses_list"),
    path("courses/<int:pk>/", CourseRetrieveAPIView.as_view(), name="courses_retrieve"),
    path("courses/create/", CourseCreateAPIView.as_view(), name="courses_create"),
    path("courses/<int:pk>/delete/", CourseDestroyAPIView.as_view(), name="courses_delete"),
    path("courses/<int:pk>/update/", CourseUpdateAPIView.as_view(), name="courses_update"),
]

urlpatterns += router.urls
