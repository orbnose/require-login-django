# require-login-django
Templates and middleware to allow requiring login, housed in a Django app.

The middleware code and description comes from [This stackoverflow thread](https://stackoverflow.com/questions/2164069/best-way-to-make-djangos-login-required-the-default).

The middleware wraps view calls in the [login_required](https://docs.djangoproject.com/en/4.1/topics/auth/default/#the-login-required-decorator) decorator from Django.
By default, it looks for a URL pattern of */accounts/login/*, etc., and looks for templates in */registration/*.

Note that the URLConf for this app assumes a view with name of **'index'**. The app will offer a link back to the assumed index after changing a password.

Quick start
-----------
1. Run python -m pip install git+https://github.com/orbnose/require-login-django#egg=require-login-django

2. Add "requirelogin" to your INSTALLED_APPS Django setting:

```
    INSTALLED_APPS = [
        ...
        'requirelogin.apps.RequireloginConfig',
    ]
```
3. Add the RequireLoginMiddleware class to your MIDDLEWARE setting:
```
MIDDLEWARE = [
    ...
    'requirelogin.middleware.RequireLoginMiddleware',
]
```
4. Include the login views URLconf in your project urls.py:
```
urlpatterns = [
    ...
    path('accounts/', include('requirelogin.urls'))
]
```
5. Define restricted and restiction exception URLs in the LOGIN_REQUIRED_URLS and LOGIN_REQUIRED_URLS_EXCEPTIONS settings to match the URLconf.
   LOGIN_REQUIRED_URLS is where you define URL patterns; each pattern must be a valid regex.
   LOGIN_REQUIRED_URLS_EXCEPTIONS is where you explicitly define any exceptions (like login and logout URLs).
```
LOGIN_REQUIRED_URLS = (r'^.*$',) #restrict any possible URL
LOGIN_REQUIRED_URLS_EXCEPTIONS = (r'/accounts/login/.*$',)
```
6. Define the [LOGIN_URL](https://docs.djangoproject.com/en/4.1/ref/settings/) setting to point to the login view:
```
LOGIN_URL = 'requirelogin:login'
```
Define the LOGOUT_URL and CHANGE_PASSWORD_URL settings to point to the logout and change password views.
These are intended to allow easier access to the account functions from other apps. 
(Note: these are not build-in Django settings; the other app must load the settings itself. See the [rosegarden custom tag](https://github.com/orbnose/rose-garden/blob/main/rosegarden/templatetags/settings_tag.py) for an example.
```
LOGOUT_URL = 'requirelogin:logout'
CHANGE_PASSWORD_URL = 'reuqirelogin:change_password'
```

7. It may be a good idea to define the [LOGIN_REDIRECT_URL](https://docs.djangoproject.com/en/4.1/ref/settings/#login-redirect-url) setting if restricting everything except the login page.
```
LOGIN_REDIRECT_URL = 'index'
```
