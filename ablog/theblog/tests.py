from django.test import TestCase
from django.urls import reverse
from .models import Post
from django.contrib.auth.models import User

class PostCRUDTests(TestCase):
    def setUp(self):
        # Create an admin user for testing
        self.user = User.objects.create_superuser(
            username='testadmin',
            password='testIsaF2004',
        )

        self.post = Post.objects.create(
            title="Test Post",
            title_tag="Test Tag",
            author=self.user,
            body="This is a test post content"
        )

    def test_create_post(self):
        self.client.login(username='testadmin', password='testIsaF2004')

        response = self.client.post(reverse('add_post'), {
            'title': 'New Test Post',
            'title_tag': 'New Test Tag',
            'author': self.user.id,
            'body': 'This is a new test post content'
        })

        self.assertEqual(response.status_code, 302)  # Check for a successful redirect after creating a post
        self.assertEqual(Post.objects.count(), 2)  # Check that the total number of posts has increased

    def test_read_post(self):
        response = self.client.get(reverse('article-detail', args=[self.post.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Post")
        self.assertContains(response, "Test Tag")
        self.assertContains(response, "This is a test post content")

    def test_update_post(self):
        self.client.login(username='testadmin', password='testIsaF2004')

        updated_title = "Updated Test Post"
        updated_body = "Updated test post content"
        response = self.client.post(reverse('update_post', args=[self.post.id]), {
            'title': updated_title,
            'title_tag': self.post.title_tag,
            'body': updated_body
        })

        self.assertEqual(response.status_code, 302)  # Check for a successful redirect after updating a post
        updated_post = Post.objects.get(id=self.post.id)
        self.assertEqual(updated_post.title, updated_title)
        self.assertEqual(updated_post.body, updated_body)

    def test_delete_post(self):
        self.client.login(username='testadmin', password='testIsaF2004')

        response = self.client.post(reverse('delete_post', args=[self.post.id]))
        self.assertEqual(response.status_code, 302)  # Check for a successful redirect after deleting a post
        self.assertEqual(Post.objects.count(), 0)  # Check that the post has been deleted
