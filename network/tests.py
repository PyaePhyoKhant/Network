from django.test import TestCase, Client
from django.urls import reverse

from .models import User, Post


class PostTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(username='User1')
        self.user2 = User.objects.create(username='User2')
        self.user3 = User.objects.create(username='User3')
        self.user4 = User.objects.create(username='User4')
        
        self.client = Client()
        self.client.force_login(self.user1)
        self.client.post(reverse('change_following'), {'user_id': self.user2.id})
        self.client.post(reverse('change_following'), {'user_id': self.user3.id})
        self.client.force_login(self.user2)
        self.client.post(reverse('post-add'), {'description': 'User 2 post'})
        self.client.post(reverse('post-add'), {'description': 'User 2 post 2'})
        self.client.force_login(self.user3)
        self.client.post(reverse('post-add'), {'description': 'User 3 post'})
        self.client.force_login(self.user4)
        self.client.post(reverse('post-add'), {'description': 'User 4 post'})
    
    def test_dummy(self):
        self.assertEqual(self.user1.username, 'User1')
        self.client.force_login(self.user1)
        res = self.client.get(reverse('following'))
        users_of_posts = set(res.context['object_list'].values_list('created_by', flat=True))
        self.assertEqual(users_of_posts, set([self.user2.id, self.user3.id]))
        # CI test on main branch
        self.assertEqual(1, 2)
        