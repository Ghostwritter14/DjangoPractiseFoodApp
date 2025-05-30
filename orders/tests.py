from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from food.models import Item, CustomCombo, Category
from orders.models import Order, OrderItem


class OrdersViewsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client = Client()
        self.client.login(username='testuser', password='password')

        self.cat = Category.objects.create(name='TestCat', slug='testcat')
        self.item1 = Item.objects.create(
            item_name='One', item_description='Desc1',
            item_price=3.00, item_image='url1', category=self.cat
        )
        self.item2 = Item.objects.create(
            item_name='Two', item_description='Desc2',
            item_price=4.50, item_image='url2', category=self.cat
        )

        self.combo = CustomCombo.objects.create(user=self.user, name='MyCombo')
        self.combo.items.set([self.item1, self.item2])

    def test_add_to_cart_and_cart_detail(self):
        resp = self.client.post(reverse('orders:add_to_cart', args=[self.item1.id]), HTTP_REFERER='/food/')
        self.assertRedirects(resp, '/food/')
        session = self.client.session
        self.assertEqual(session['cart'][str(self.item1.id)], 1)

        resp = self.client.get(reverse('orders:cart_detail'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Your Cart')

        self.assertContains(resp, self.item1.item_name)
        self.assertContains(resp, '£3.0')

    def test_add_combo_to_cart(self):
        resp = self.client.post(reverse('orders:add_combo_to_cart', args=[self.combo.id]), HTTP_REFERER='/profile/')
        self.assertRedirects(resp, '/profile/')
        session = self.client.session

        self.assertEqual(session['cart'][str(self.item1.id)], 1)
        self.assertEqual(session['cart'][str(self.item2.id)], 1)

    def test_remove_from_cart(self):
        session = self.client.session
        session['cart'] = {str(self.item1.id): 2, str(self.item2.id): 1}
        session.save()

        resp = self.client.post(reverse('orders:remove_from_cart', args=[self.item1.id]))
        self.assertRedirects(resp, reverse('orders:cart_detail'))
        session = self.client.session
        self.assertNotIn(str(self.item1.id), session['cart'])
        self.assertIn(str(self.item2.id), session['cart'])

    def test_checkout_and_order_detail(self):
        session = self.client.session
        session['cart'] = {str(self.item1.id): 2, str(self.item2.id): 1}
        session.save()

        resp = self.client.post(reverse('orders:checkout'))

        order = Order.objects.get(user=self.user)
        self.assertRedirects(resp, reverse('orders:detail', args=[order.id]))

        items = list(order.items.all())
        self.assertEqual(len(items), 2 + 1)
        quantities = {oi.item.id: oi.quantity for oi in items}
        self.assertEqual(quantities[self.item1.id], 2)
        self.assertEqual(quantities[self.item2.id], 1)

        self.assertEqual(self.client.session.get('cart', {}), {})

        resp = self.client.get(reverse('orders:detail', args=[order.id]))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, f"Order #{order.id}")
        self.assertContains(resp, self.item1.item_name)
        self.assertContains(resp, self.item2.item_name)

    def test_invoice_view_renders_qr(self):
        order = Order.objects.create(user=self.user)
        OrderItem.objects.create(order=order, item=self.item1, quantity=1)

        resp = self.client.get(reverse('orders:invoice', args=[order.id]))
        self.assertEqual(resp.status_code, 200)

        self.assertContains(resp, 'data:image/png;base64')

        content = resp.content.decode()
        self.assertTrue(len(content.split('data:image/png;base64,')[1]) > 50)
