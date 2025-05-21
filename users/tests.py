from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from food.models import Category, Item
from users.models import Profile
from users.forms import RegisterForm
from users.views import register, profile as profile_view
from users.forms import RegisterForm
from food.models import CustomCombo


class UsersViewsTestCase(TestCase):
    def setUp(self):
        # Prepare client and a default category & items
        self.client = Client()
        self.cat1 = Category.objects.create(name='Cat1', slug='cat1')
        self.cat2 = Category.objects.create(name='Cat2', slug='cat2')
        self.item1 = Item.objects.create(
            item_name='I1', item_description='D1',
            item_price=1.0, item_image='url1', category=self.cat1
        )
        self.item2 = Item.objects.create(
            item_name='I2', item_description='D2',
            item_price=2.0, item_image='url2', category=self.cat2
        )

    def test_register_get_and_post(self):
        url = reverse('Register')
        # GET shows form
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertIsInstance(resp.context['form'], RegisterForm)

        # POST valid data
        data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'complexPassword123',
            'password2': 'complexPassword123'
        }
        resp = self.client.post(url, data)
        # should redirect to login
        self.assertRedirects(resp, reverse('login'))
        # user created
        u = User.objects.get(username='newuser')
        # profile auto-created
        self.assertTrue(hasattr(u, 'profile'))
        self.assertIsInstance(u.profile, Profile)

    def test_profile_requires_login(self):
        url = reverse('profile')
        resp = self.client.get(url)
        # should redirect to login
        self.assertRedirects(resp, f"{reverse('login')}?next={url}")

    def test_profile_set_favorite(self):
        u = User.objects.create_user(username='u2', password='pass')
        self.client.login(username='u2', password='pass')
        # choose cat1 as favorite
        resp = self.client.post(
            reverse('profile'),
            {'favorite': self.cat1.id}
        )
        self.assertRedirects(resp, reverse('profile'))
        u.refresh_from_db()
        self.assertEqual(u.profile.favorite, self.cat1)

    def test_profile_create_combo(self):
        u = User.objects.create_user(username='u3', password='pass')
        self.client.login(username='u3', password='pass')
        # POST combo name and items
        resp = self.client.post(
            reverse('profile'),
            {
                'name': 'ComboX',
                'items': [self.item1.id, self.item2.id]
            }
        )
        self.assertRedirects(resp, reverse('profile'))
        # combo created for user
        combos = u.custom_combos.all()
        self.assertEqual(combos.count(), 1)
        combo = combos.first()
        self.assertEqual(combo.name, 'ComboX')
        ids = list(combo.items.values_list('id', flat=True))
        self.assertCountEqual(ids, [self.item1.id, self.item2.id])
