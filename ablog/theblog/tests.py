from django.test import TestCase
from django.urls import reverse
from .models import Post
from django.contrib.auth.models import User

# ---------------Unit test--------------
# class PostCRUDTests(TestCase):
#     def setUp(self):
#         # Create an admin user for testing
#         self.user = User.objects.create_superuser(
#             username='testadmin',
#             password='testIsaF2004',
#         )

#         self.post = Post.objects.create(
#             title="Test Post",
#             title_tag="Test Tag",
#             author=self.user,
#             body="This is a test post content"
#         )

#     def test_create_post(self):
#         self.client.login(username='testadmin', password='testIsaF2004')

#         response = self.client.post(reverse('add_post'), {
#             'title': 'New Test Post',
#             'title_tag': 'New Test Tag',
#             'author': self.user.id,
#             'body': 'This is a new test post content'
#         })

#         self.assertEqual(response.status_code, 302)  # Check for a successful redirect after creating a post
#         self.assertEqual(Post.objects.count(), 2)  # Check that the total number of posts has increased

#     def test_read_post(self):
#         response = self.client.get(reverse('article-detail', args=[self.post.id]))
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, "Test Post")
#         self.assertContains(response, "Test Tag")
#         self.assertContains(response, "This is a test post content")

#     def test_update_post(self):
#         self.client.login(username='testadmin', password='testIsaF2004')

#         updated_title = "Updated Test Post"
#         updated_body = "Updated test post content"
#         response = self.client.post(reverse('update_post', args=[self.post.id]), {
#             'title': updated_title,
#             'title_tag': self.post.title_tag,
#             'body': updated_body
#         })

#         self.assertEqual(response.status_code, 302)  # Check for a successful redirect after updating a post
#         updated_post = Post.objects.get(id=self.post.id)
#         self.assertEqual(updated_post.title, updated_title)
#         self.assertEqual(updated_post.body, updated_body)

#     def test_delete_post(self):
#         self.client.login(username='testadmin', password='testIsaF2004')

#         response = self.client.post(reverse('delete_post', args=[self.post.id]))
#         self.assertEqual(response.status_code, 302)  # Check for a successful redirect after deleting a post
#         self.assertEqual(Post.objects.count(), 0)  # Check that the post has been deleted


# -------------Integration testing------------

# class BlogCRUDIntegrationTestCase(TestCase):

#     def setUp(self):
#         # Created a user for testing
#         self.user = User.objects.create_user(
#             username='testuser',
#             password='testIsaF2004',
#         )

#     def test_blog_crud_workflow(self):
#         self.client.login(username='testuser', password='testIsaF2004')

#         # Created a post
#         create_url = reverse('add_post')
#         create_data = {
#             'title': 'New Test Post',
#             'title_tag': 'New Test Tag',
#             'author': self.user.id,
#             'body': 'This is a new test post content'
#         }
#         response = self.client.post(create_url, create_data)
#         self.assertEqual(response.status_code, 302)  # Expecting a redirect
#         self.assertEqual(Post.objects.count(), 1)  # Check that the total number of posts has increased

#         # Retrieved the created post
#         created_post = Post.objects.first()
#         self.assertEqual(created_post.title, 'New Test Post')
#         self.assertEqual(created_post.title_tag, 'New Test Tag')
#         self.assertEqual(created_post.author, self.user)
#         self.assertEqual(created_post.body, 'This is a new test post content')

#         # Updated the post
#         update_url = reverse('update_post', args=[created_post.id])
#         updated_data = {
#             'title': 'Updated Test Post',
#             'title_tag': 'Updated Test Tag',
#             'body': 'Updated test post content'
#         }
#         response = self.client.post(update_url, updated_data)
#         self.assertEqual(response.status_code, 302)  # Expecting a redirect
#         created_post.refresh_from_db()
#         self.assertEqual(created_post.title, 'Updated Test Post')
#         self.assertEqual(created_post.title_tag, 'Updated Test Tag')
#         self.assertEqual(created_post.body, 'Updated test post content')

#         # Delete the post
#         delete_url = reverse('delete_post', args=[created_post.id])
#         response = self.client.post(delete_url)
#         self.assertEqual(response.status_code, 302)  # Expecting a redirect
#         self.assertFalse(Post.objects.filter(pk=created_post.id).exists())

# -------------------------------------------------------------

# -------------------Smoke testing------------------------------------------

class SmokeTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_homepage(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Blogs')  

    def test_create_post(self):
        self.client.login(username='testuser', password='testpassword')
        
        response = self.client.post(reverse('add_post'), {
            'title': 'New Test Post',
            'title_tag': 'New Test Tag',
            'author': self.user.id,
            'body': 'This is new test post',
        })
        
        self.assertEqual(response.status_code, 302)  # Expecting a redirect after creating a post
        self.assertTrue(Post.objects.filter(title='New Test Post').exists())

    def test_edit_post(self):
        post = Post.objects.create(
            title='Test Post',
            title_tag='Test Tag',
            author=self.user,
            body='This is a test post content',
        )
        
        self.client.login(username='testuser', password='testpassword')
        
        response = self.client.post(reverse('update_post', args=[post.pk]), {
            'title': 'Updated Test Post',
            'title_tag': 'Updated Test Tag',
            'body': 'This is an updated test post content',
        })
        
        self.assertEqual(response.status_code, 302)  # Expecting a redirect after editing a post
        post.refresh_from_db()
        self.assertEqual(post.title, 'Updated Test Post')

    def test_delete_post(self):
    
        post = Post.objects.create(
            title='Test Post to Delete',
            title_tag='Test Tag',
            author=self.user,
            body='This is a test post content to delete',
        )   
        
        self.client.login(username='testuser', password='testpassword')
    
        response = self.client.post(reverse('delete_post', args=[post.pk]))
    
        self.assertEqual(response.status_code, 302)  # Expecting a redirect after deleting a post
        self.assertFalse(Post.objects.filter(title='Test Post to Delete').exists())


