from django.test import TestCase, override_settings, modify_settings
from django.contrib.auth.models import User
from django.urls import reverse

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
            Set the default redirect login url to a test view in this app.
        modify_settings:
            Add the required login middleware class to the project's middleware.
    '''
    @override_settings( ROOT_URLCONF = test_urls,
                        LOGIN_REQUIRED_URLS = (r'^.*$',),
                        LOGIN_REQUIRED_URLS_EXCEPTIONS = (r'/accounts/login/*$',),
                        LOGIN_REDIRECT_URL = 'index',
                        LOGIN_URL = 'requirelogin:login')
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

        # --- Logged in as regular user
        if not self.client.login(username="ben", password="pass"):
            raise ValueError('Test user login failed.')

        response = self.client.get(reverse('index'))
        self.assertContains(response, 'index page')

        response = self.client.get(reverse('nested_redir'))
        self.assertContains(response, 'nested page')

        response = self.client.get(reverse('nested_forbidden'))
        self.assertEquals(response.status_code, 403)

        # --- Logged in as super user
        if not self.client.login(username="bensuper", password="pass1"):
            raise ValueError('Test superuser login failed.')

        response = self.client.get(reverse('index'))
        self.assertContains(response, 'index page')

        response = self.client.get(reverse('nested_redir'))
        self.assertContains(response, 'nested page')

        response = self.client.get(reverse('nested_forbidden'))
        self.assertContains(response, 'nested forbidden page')