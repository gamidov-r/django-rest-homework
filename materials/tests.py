from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson
from users.models import User


class LessonTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="test@school.ru", password="test")
        self.course = Course.objects.create(name="Test Course", description="This is a test course")
        self.lesson = Lesson.objects.create(
            course=self.course, name="Test Lesson", description="This is a test lesson", owner=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        url = reverse("materials:lessons_retrieve", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), self.lesson.name)

    def test_lesson_create(self):
        url = reverse("materials:lessons_create")
        data = {"name": "test lesson", "description": "test description", "video_url": "https://youtubekids.com"}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_lesson_update(self):
        patched_name = f"{self.lesson.name} updated"
        patched_description = f"{self.lesson.description} updated"
        url = reverse("materials:lessons_update", args=(self.lesson.pk,))
        data = {"name": patched_name, "description": patched_description}
        response = self.client.patch(url, data=data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), patched_name)
        self.assertEqual(data.get("description"), patched_description)

    def test_lesson_delete(self):
        url = reverse("materials:lessons_delete", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)
        # self.assertEqual(data.get("description"), patched_description)

    def test_lesson_create_reject_video_url(self):
        url = reverse("materials:lessons_create")
        data = {
            "name": "test lesson",
            "description": "test description",
            "video_url": "http://myvideohosting.ddns.net",
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # 2nd arg is host name from response message
        self.assertEqual(data["video_url"], response.json()["video_url"][0].split(" ")[0])

    def test_lesson_create_reject_video_description(self):
        url = reverse("materials:lessons_create")
        data = {"name": "test lesson", "description": "test www.lookmyvideo.ucoz.ru description"}
        response = self.client.post(url, data=data)
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # get and assert hosts from descriptions
        self.assertEqual(data["description"].split(" ")[1], response.json()["description"][0].split(" ")[1])
