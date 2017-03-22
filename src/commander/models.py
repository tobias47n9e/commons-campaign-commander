"""
Campaign Commander models.

This module contains the classes for the OAuth Wikimedia
users, the requested images, the request texts, and the
submitted image model.
"""

from django.contrib.gis.db import models
from commander.validators import validate_wikidata_id
from django.contrib.auth.models import User


class WikimediaUser(models.Model):
    """
    Model for Wikimedia users.

    Each Wikimedia user is related with a one-to-one relation
    to Django's User model.
    """
    wikimedia_id = models.OneToOneField(User, on_delete=models.CASCADE)


class ImageRequest(models.Model):
    """
    Model for image requests.

    Image requests have a date of creation, a related
    wikidata item ID, a geographic point for the request
    and a creator.
    """
    created = models.DateTimeField(auto_now_add=True)
    wikidata_id = models.CharField(max_length=100,
                                   validators=[validate_wikidata_id])
    points = models.MultiPointField()
    creator = models.ForeignKey('auth.User',
                                related_name='image_request',
                                on_delete=models.CASCADE)


class RequestText(models.Model):
    """
    Model for the texts that belong to a image request.

    The texts that go with each image request have a reference
    to the image request, the language of the text and the
    text itself.
    """
    image_request = models.ForeignKey(ImageRequest,
                                      related_name='request_texts',
                                      on_delete=models.CASCADE)
    lang = models.CharField(max_length=20)
    text = models.CharField(max_length=200)
    revision = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}: {}'.format(lang, text)


class SubmittedImage(models.Model):
    """
    Model for submitted images.

    Submitted images have a user that submitted the image,
    the image request for which the image is submitted,
    the submission data and the filename on Commons.
    """
    user = models.ForeignKey('auth.User', related_name='submitted_images',
                             on_delete=models.CASCADE)
    image_request = models.ForeignKey(ImageRequest,
                                      related_name='submitted_images',
                                      on_delete=models.CASCADE)
    submitted = models.DateTimeField(auto_now_add=True)
    filename = models.CharField(max_length=500, blank=True, null=True)
