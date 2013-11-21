bootstrap3-django-admin
=======================

Bootstrap3 for Django admin

## Description

There are a few packages out there to apply Bootstrap styling and markup for Django admin, but so far none of them were using Bootstrap 3.


## Installation 

1.  pip install -e git://github.com/jonashagstedt/bootstrap3-django-admin.git#egg=admin_bootstrap

2. Make sure you put ```'admin_bootstrap3',``` before django.contrib.admin in installed apps.


        INSTALLED_APPS = (
            ...
            'admin_bootstrap3',
            'django.contrib.admin',

            'compressor',
         )

3. If you already have compressor setup, ignore the next steps

4. Add ```compressor``` to installed apps

5. Add COMPRESS_PRECOMPILERS to your settings

        COMPRESS_PRECOMPILERS = (
            ('text/less', 'lessc {infile} {outfile}'),
        )

6. Add ```'compressor.finders.CompressorFinder'``` to your STATICFILES_FINDERS

        STATICFILES_FINDERS = (
            ...
            'compressor.finders.CompressorFinder',
        )



## Configuration

There isn't much to configure.
If you want to add your own styles to the admin section, you can add ```ADMIN_LESS_FILE``` to setting.

i.e: ```ADMIN_LESS_FILE = 'mystyles.less'``` or ```ADMIN_LESS_FILE = 'admin/mystyles.less'``` depending on where you put your file.

Make sure the file exists within your ```static``` folder.



## Additional notes
Bootstrap is great, however [Font Awesome](http://fontawesome.io) is nicer.

If you want to use Bootstraps default icons, just udpate the remplates and replace all "fa" classes with "glyphicons"

If you can't see the icons while debugging, add this to your settings.py ```COMPRESS_OUTPUT_DIR = ''```

## Credits

*  bootstrap-datepicker by Stefan Petre, with improvements by Andrew Rowls
(http://www.eyecon.ro/bootstrap-datepicker)

* bootstrap-timepicker by Joris de Wit (http://jdewit.github.com/bootstrap-timepicker)

* Chosen select box enhancement by Patrick Filler (https://github.com/harvesthq/chosen)
