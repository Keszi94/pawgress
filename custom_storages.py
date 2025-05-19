from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage

print(
    "STATICFILES_LOCATION:",
    getattr(settings, 'STATICFILES_LOCATION', 'Not found')
    )


class StaticStorage(S3Boto3Storage):
    location = settings.STATICFILES_LOCATION
    default_acl = 'public-read'


class MediaStorage(S3Boto3Storage):
    location = settings.MEDIAFILES_LOCATION
    file_overwrite = False
    default_acl = 'public-read'
