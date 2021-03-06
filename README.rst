Instructions
============
Follow the steps below to start a new project using this django template::

    Clone  this repository into directory toast
    cd into directory
    $ chmod +x start.sh
    $ ./start.sh
    $ workon toast
    $ ./manage.py runserver

Deployment
==========
Projects created using this template are meant to be deployed on heroku

Create a heroku application and push the code there. You will need to set:

- The DJANGO_SETTINGS_MODULE variable to either "{{project_name}}.settings.heroku" or heroku_staging
- The aws settings in AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME, AWS_ACCESS_KEY_ID
- and finally the SECRET_ACCESS_KEY which can be generated via ```python -c 'import random; print "".join([random.choice("abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)") for i in range(50)])'```

You can set the variables using the heroku command, the config:set argument and the --app flag:
```heroku config:set DJANGO_SETTINGS_MODULE={{project_name}}.settings.heroku-staging```
or
```heroku config:set SECRET_KEY=`python -c 'import random; print "".join([random.choice("abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)") for i in range(50)])'````

Use the Mandrill addon to setup email -
```$ heroku addons:add mandrill:starter```

Make sure to add psql backup
```$ heroku addons:add pgbackups```

Add in the newrelic addon:
```$ heroku addons:add newrelic```

After pushing the code, you'll need to syncdb and run the initial migrations:
```$ heroku run python manage.py syncdb --migrate```
