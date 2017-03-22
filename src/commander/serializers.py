"""
Campaign Commander serializers.

Contains the serializers for the different Campaign
Commander models.
"""

from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from commander.models import ImageRequest,\
                             RequestText, \
                             SubmittedImage
from django.contrib.auth.models import User


class SubmittedImageSerializer(serializers.ModelSerializer):
    """
    Serializes the submitted image model.
    """
    user = serializers.ReadOnlyField(source='user.username')
    image_request = serializers. \
        ReadOnlyField(source='image_request.id')

    class Meta:
        """
        Serialized model and fields.
        """
        model = SubmittedImage
        fields = ('filename', 'user',
                  'submitted', 'image_request')
        extra_kwargs = {'image_request': {'write_only': True}}

    def create(self, validated_data):
        request_object = ImageRequest.objects.get(
            pk=validated_data['image_request'])
        validated_data['image_request'] = request_object
        instance = SubmittedImage.objects.create(**validated_data)
        return instance


class RequestTextSerializer(serializers.ModelSerializer):
    """
    Serializes the image request texts.
    """
    class Meta:
        """
        Serialized model and fields.
        """
        model = RequestText
        fields = ('lang', 'text')


class ImageRequestSerializer(GeoFeatureModelSerializer,
                             serializers.HyperlinkedModelSerializer):
    """
    Serializers the image requests.
    """
    request_texts = RequestTextSerializer(many=True)
    submitted_images = SubmittedImageSerializer(many=True)
    creator = serializers.ReadOnlyField(source='creator.username')
    url = \
        serializers.HyperlinkedIdentityField(view_name='api_image_requests_detail',
                                             format='html')

    class Meta:
        """
        Serialized model and fields.

        The geo field is used for the spatial queries.
        """
        model = ImageRequest
        geo_field = 'points'
        fields = ('id', 'created', 'url', 'submitted_images',
                  'wikidata_id', 'points', 'request_texts',
                  'creator')

    def create(self, data):
        """
        Create a new image request.

        Iterates over the request texts and builds the
        relation to the image request object.
        """
        request_texts = data.pop('request_texts')
        submitted_images = data.pop('submitted_images')
        image_request_object = ImageRequest.objects.create(**data)

        for text in request_texts:
            RequestText.objects.create(image_request=image_request_object,
                                       **text)
        return image_request_object


class UserSerializer(serializers.ModelSerializer):
    """
    Serializes the user model.
    """
    image_request = \
        serializers.PrimaryKeyRelatedField(many=True,
        queryset=ImageRequest.objects.all())
    creator = serializers.ReadOnlyField(source='creator.username')

    class Meta:
        """
        Serialized model and fields.
        """
        model = User
        fields = ('id', 'username', 'image_request')
