
from django.contrib.auth.models import User, Group
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse


class RoleAccessTests(TestCase):
    def setUp(self):
        call_command('setup_roles')

        self.member = User.objects.create_user(
            'mem', password='pass12345'
        )
        self.member.groups.add(
            Group.objects.get(name='Member')
        )

        self.librarian = User.objects.create_user(
            'lib', password='pass12345'
        )
        self.librarian.groups.add(
            Group.objects.get(name='Librarian')
        )

        self.url = reverse('library:book-create')

    def test_anonymous_is_redirected_to_login(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_member_cannot_create_books(self):
        self.client.login(
            username='mem', password='pass12345'
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_librarian_can_open_create_form(self):
        self.client.login(
            username='lib', password='pass12345'
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_registration_assigns_member_role(self):
        self.client.post(reverse('library:register'), {
            'username': 'newbie',
            'email': 'n@example.com',
            'password1': 'Str0ngPass!234',
            'password2': 'Str0ngPass!234',
        })

        user = User.objects.get(username='newbie')
        self.assertTrue(
            user.groups.filter(name='Member').exists()
        )
