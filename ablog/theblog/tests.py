# from django.test import TestCase
# from django.urls import reverse
# from .models import Post
from django.contrib.auth.models import User
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By

class SeleniumUITest(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = webdriver.Firefox()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_ui_elements(self):
        # Navigate to the home page
        self.selenium.get(self.live_server_url)
        self.assertIn("Blogs", self.selenium.title)  # Check the title

        # Click on the "Add Post" button
        self.selenium.find_element(By.PARTIAL_LINK_TEXT, "Add Post").click()
        self.assertIn("Create a new blog", self.selenium.title)

        # Fill out the form to create a new post
        title_input = self.selenium.find_element(By.NAME, "title")
        title_input.send_keys("Test Post Title")

        title_tag_input = self.selenium.find_element(By.NAME, "title_tag")
        title_tag_input.send_keys("Test Title Tag")

        body_input = self.selenium.find_element(By.NAME, "body")
        body_input.send_keys("This is a test post body.")

        # Submit the form by clicking the "Post" button
        post_button = self.selenium.find_element(By.CSS_SELECTOR, "button[type='submit']")
        post_button.click()

        # Check if the post was successfully created
        success_message = self.selenium.find_element(By.CSS_SELECTOR, ".alert-success")
        self.assertTrue(success_message.is_displayed())

        # Navigate back to the home page
        self.selenium.find_element(By.PARTIAL_LINK_TEXT, "Blogs").click()
        self.assertIn("Blogs", self.selenium.title)

        # Click on links to view the newly created post
        self.selenium.find_element(By.PARTIAL_LINK_TEXT, "Test Post Title").click()
        self.assertIn("Test Post Title", self.selenium.title)

        # Verify the post details
        post_title = self.selenium.find_element(By.TAG_NAME, "h1")
        self.assertEqual(post_title.text, "Test Post Title")

        post_body = self.selenium.find_element(By.TAG_NAME, "p")
        self.assertEqual(post_body.text, "This is a test post body.")

if __name__ == '__main__':
    import unittest
    unittest.main()

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

# class SmokeTest(TestCase):

#     def setUp(self):
#         self.user = User.objects.create_user(username='testuser', password='testpassword')

#     def test_homepage(self):
#         response = self.client.get(reverse('home'))
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, 'Blogs')  

#     def test_create_post(self):
#         self.client.login(username='testuser', password='testpassword')
        
#         response = self.client.post(reverse('add_post'), {
#             'title': 'New Test Post',
#             'title_tag': 'New Test Tag',
#             'author': self.user.id,
#             'body': 'This is new test post',
#         })
        
#         self.assertEqual(response.status_code, 302)  # Expecting a redirect after creating a post
#         self.assertTrue(Post.objects.filter(title='New Test Post').exists())

#     def test_edit_post(self):
#         post = Post.objects.create(
#             title='Test Post',
#             title_tag='Test Tag',
#             author=self.user,
#             body='This is a test post content',
#         )
        
#         self.client.login(username='testuser', password='testpassword')
        
#         response = self.client.post(reverse('update_post', args=[post.pk]), {
#             'title': 'Updated Test Post',
#             'title_tag': 'Updated Test Tag',
#             'body': 'This is an updated test post content',
#         })
        
#         self.assertEqual(response.status_code, 302)  # Expecting a redirect after editing a post
#         post.refresh_from_db()
#         self.assertEqual(post.title, 'Updated Test Post')

#     def test_delete_post(self):
    
#         post = Post.objects.create(
#             title='Test Post to Delete',
#             title_tag='Test Tag',
#             author=self.user,
#             body='This is a test post content to delete',
#         )   
        
#         self.client.login(username='testuser', password='testpassword')
    
#         response = self.client.post(reverse('delete_post', args=[post.pk]))
    
#         self.assertEqual(response.status_code, 302)  # Expecting a redirect after deleting a post
#         self.assertFalse(Post.objects.filter(title='Test Post to Delete').exists())

# ---------------------------------------------------------------

# ----------------Database testing-----------------------------

# class BlogCRUDTests(TestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(
#             username='testuser',
#             password='testpassword',
#         )

#     def test_create_post(self):
#         self.client.login(username='testuser', password='testpassword')

#         response = self.client.post(reverse('add_post'), {
#             'title': 'New Test Post',
#             'title_tag': 'New Test Tag',
#             'author': self.user.id,
#             'body': 'This is a new test post content',
#         })

#         self.assertEqual(response.status_code, 302)  # Check for a successful redirect after creating a post
#         self.assertTrue(Post.objects.filter(title='New Test Post').exists())  # Check that the post was created in the database

#     def test_read_post(self):
#         post = Post.objects.create(
#             title='Test Post',
#             title_tag='Test Tag',
#             author=self.user,
#             body='This is a test post content',
#         )

#         response = self.client.get(reverse('article-detail', args=[post.id]))
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, 'Test Post')
#         self.assertContains(response, 'This is a test post content')

#     def test_update_post(self):
#         self.client.login(username='testuser', password='testpassword')

#         post = Post.objects.create(
#             title='Test Post',
#             title_tag='Test Tag',
#             author=self.user,
#             body='This is a test post content',
#         )

#         updated_title = 'Updated Test Post'
#         updated_body = 'This is an updated test post content'
#         response = self.client.post(reverse('update_post', args=[post.id]), {
#             'title': updated_title,
#             'title_tag': 'Test Tag',  
#             'body': updated_body,
#         })

#         self.assertEqual(response.status_code, 302)  # Check for a successful redirect after updating a post
#         post.refresh_from_db()  # Refresh the post instance from the database
#         self.assertEqual(post.title, updated_title)  # Check if the post was updated in the database
#         self.assertEqual(post.body, updated_body)

#     def test_delete_post(self):
#         self.client.login(username='testuser', password='testpassword')

#         post = Post.objects.create(
#             title='Test Post to Delete',
#             title_tag='Test Tag',
#             author=self.user,
#             body='This is a test post content to delete',
#         )

#         response = self.client.post(reverse('delete_post', args=[post.id]))
#         self.assertEqual(response.status_code, 302)  # Check for a successful redirect after deleting a post
#         self.assertFalse(Post.objects.filter(title='Test Post to Delete').exists()) # Check if the post was deleted in the database

