bootstrap3-django-admin
=======================

Bootstrap3 for Django admin

## Installation 

1.  pip install -e git://github.com/jonashagstedt/bootstrap3-django-admin.git#egg=admin_bootstrap

2. Make sure you put ```'admin_bootstrap3',``` before django.contrib.admin in installed apps

    INSTALLED_APPS = (
    	...
        'admin_bootstrap3',
        'django.contrib.admin',
     )

3. That's it!

