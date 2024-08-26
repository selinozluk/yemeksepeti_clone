# users/tests.py
from django.test import TestCase
from users.models import User

class UserTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            firstName="Selin",
            lastName="Özlük",
            email="selinozluk@gmail.com",
            birthDate="2002-04-10"
        )

    def test_user_creation(self):
        """Kullanıcı doğru şekilde oluşturulmalı"""
        user = User.objects.get(email="selinozluk@gmail.com")
        self.assertEqual(user.firstName, "Selin")
        self.assertEqual(user.lastName, "Özlük")
        self.assertEqual(user.email, "selinozluk@gmail.com")
        self.assertEqual(user.birthDate.strftime('%Y-%m-%d'), "2002-04-10")

    def test_user_email_uniqueness(self):
        """Aynı email ile kullanıcı oluşturulamayacağını doğrulama"""
        with self.assertRaises(Exception):
            User.objects.create(
                firstName="Nehir",
                lastName="Su",
                email="selinozluk@gmail.com",  # Aynı email ile kullanıcı oluşturma denemesi
                birthDate="2006-08-07"
            )
