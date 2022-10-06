from django.test import TestCase, override_settings, modify_settings
from django.contrib.auth.models import User
from django.urls import reverse

from http import HTTPStatus

from . import test_urls

# Create your tests here.

def setup_valid_user(username="ben",password="pass"):
    user = User.objects.create_user(username=username, password=password)
    return user

def setup_valid_superuser(username="bensuper", password="pass1"):
    user = User.objects.create_superuser(username=username, password=password)
    return user


class LoginTest(TestCase):
    
    ''' override_settings:
            Modify the project URL patterns to include the standard login pages for the login_required decorator.
            Modify the project URL patterns to include links to test views in this app.
            Set the restricted and allowed URLs settings.
            Set the default redirect login and logout urls to a test view in this app.
        modify_settings:
            Add the required login middleware class to the project's middleware.
    '''
    @override_settings( ROOT_URLCONF = test_urls,
                        LOGIN_REQUIRED_URLS = (r'^.*$',),
                        LOGIN_REQUIRED_URLS_EXCEPTIONS = (r'/accounts/login/*$',),
                        LOGIN_REDIRECT_URL = 'index',
                        LOGIN_URL = 'requirelogin:login',
                        LOGOUT_URL = 'requirelogin:logout')
    @modify_settings( MIDDLEWARE = { 'append': 'requirelogin.middleware.RequireLoginMiddleware'}) 
    def test_login_requirement(self):
        #Modify django settings to isolate the requirelogin app, and then test authentication requirements imposed by the middleware.        
        
        setup_valid_user()
        setup_valid_superuser()

        # --- Not logged in
        response = self.client.get(reverse('index'))
        self.assertRedirects(response,'/accounts/login/?next=/')

        response = self.client.get(reverse('nested_redir'))
        self.assertRedirects(response,'/accounts/login/?next=/nested/nested_redir/')

        response = self.client.get(reverse('nested_forbidden'))
        self.assertRedirects(response,'/accounts/login/?next=/nested/nested_forbidden/')

        response = self.client.get(reverse('requirelogin:logout'))
        self.assertRedirects(response,'/accounts/login/?next=/accounts/logout/')

        response = self.client.get(reverse('requirelogin:change_password'))
        self.assertRedirects(response,'/accounts/login/?next=/accounts/change_password/')

        # --- Logged in as regular user
        if not self.client.login(username="ben", password="pass"):
            raise ValueError('Test user login failed.')

        response = self.client.get(reverse('index'))
        self.assertContains(response, 'index page')

        response = self.client.get(reverse('nested_redir'))
        self.assertContains(response, 'nested page')

        response = self.client.get(reverse('nested_forbidden'))
        self.assertEquals(response.status_code, 403)

        # --- Change password as a regular user
        response = self.client.get(reverse('requirelogin:change_password'))
        self.assertContains(response, "Changing password")
        response = self.client.post(
            reverse('requirelogin:change_password'),
            data={'old_password': 'pass', 'new_password1': 'pass12345', 'new_password2': 'pass12345'})
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response["Location"], "/accounts/change_password/done/")

        response = self.client.get(reverse('index'))
        self.assertContains(response, 'index page')

        # --- Log out as regular user
        response = self.client.get(reverse('requirelogin:logout'))
        self.assertContains(response, "You have been logged out")

        response = self.client.get(reverse('index'))
        self.assertRedirects(response,'/accounts/login/?next=/')

        # --- Log in with new password as regular user
        if not self.client.login(username="ben", password="pass12345"):
            raise ValueError('Test user re-login failed.')

        response = self.client.get(reverse('index'))
        self.assertContains(response, 'index page')

        # --- Logged in as super user
        if not self.client.login(username="bensuper", password="pass1"):
            raise ValueError('Test superuser login failed.')

        response = self.client.get(reverse('index'))
        self.assertContains(response, 'index page')

        response = self.client.get(reverse('nested_redir'))
        self.assertContains(response, 'nested page')

        response = self.client.get(reverse('nested_forbidden'))
        self.assertContains(response, 'nested forbidden page')

        # --- Change password as a super user
        response = self.client.get(reverse('requirelogin:change_password'))
        self.assertContains(response, "Changing password")
        response = self.client.post(
            reverse('requirelogin:change_password'),
            data={'old_password': 'pass1', 'new_password1': 'pass23456', 'new_password2': 'pass23456'})
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response["Location"], "/accounts/change_password/done/")

        response = self.client.get(reverse('index'))
        self.assertContains(response, 'index page')

        # --- Log out as super user
        response = self.client.get(reverse('requirelogin:logout'))
        self.assertContains(response, "You have been logged out")

        response = self.client.get(reverse('index'))
        self.assertRedirects(response,'/accounts/login/?next=/')

        # --- Log in with new password as super user
        if not self.client.login(username="bensuper", password="pass23456"):
            raise ValueError('Test user re-login failed.')

        response = self.client.get(reverse('index'))
        self.assertContains(response, 'index page')