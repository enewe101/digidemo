# These settings need to be eddited on new dev installations
PROJECT_DIR = '/Users/enewe101/projects/digidemo'

# These settings don't normally need to be edited on new dev installations
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
		'NAME': 'digidemo',
		'USER': 'digidemo',
		'PASSWORD':'devpass',
		'HOST':'localhost'
    }
}
SECRET_KEY = 'dev_key_do_not_use_in_production__t7665_02i)odqry33bn3q$n_&7i8'
ALLOWED_HOSTS = ['localhost']
EMAIL_HOST_USER = "USER"
EMAIL_HOST_PASSWORD = "PASSWORD"
DEBUG = True
STRICT_TEMPLATE = False
