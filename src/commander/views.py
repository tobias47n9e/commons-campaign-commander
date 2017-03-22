"""
Contains the views of the Campaign Commander.
"""

from commander.models import ImageRequest,\
                             RequestText,\
                             SubmittedImage
from commander.serializers import ImageRequestSerializer,\
                                  UserSerializer,\
                                  SubmittedImageSerializer

from rest_framework import generics
from rest_framework_gis.filters import DistanceToPointFilter
from django.shortcuts import render
from django.contrib.auth import login, logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch
from social_django.utils import psa


class ImageRequestList(generics.ListCreateAPIView):
    """
    REST API class for image requests.
    """
    queryset = ImageRequest.objects\
        .prefetch_related(Prefetch('request_texts',
                                   queryset=RequestText.objects
                                   .order_by('lang', 'image_request_id', '-revision')
                                   .distinct('lang', 'image_request_id')))\
        .prefetch_related(Prefetch('submitted_images',
                                   queryset=SubmittedImage.objects.all()))
    serializer_class = ImageRequestSerializer
    distance_filter_field = 'points'
    filter_backends = (DistanceToPointFilter,)
    distance_filter_convert_meters = True

    def perform_create(self, serializer):
        """
        Creates a new image request.

        The currently logged in user is added to the data
        and passed to the serializer.
        """
        serializer.save(creator=self.request.user)


class ImageRequestListByAuthor(generics.ListCreateAPIView):
    """
    REST API class for image requests from one user.
    """
    queryset = ImageRequest.objects.all()
    serializer_class = ImageRequestSerializer
    distance_filter_field = 'points'
    filter_backends = (DistanceToPointFilter,)

    def perform_create(self, serializer):
        """
        Creates a new image request.

        The currently logged in user is added to the data
        and passed to the serializer.
        """
        serializer.save(creator=self.request.user)

    def get_queryset(self):
        """
        Adds the queryset on the username.
        """
        username = self.kwargs['username']
        return ImageRequest.objects.filter(creator__username=username)


class ImageRequestDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    REST API view of a single image request.
    """
    queryset = ImageRequest.objects.all()
    serializer_class = ImageRequestSerializer


class SubmittedImageList(generics.ListCreateAPIView):
    """
    REST API list of submitted images.
    """
    queryset = SubmittedImage.objects.all()
    serializer_class = SubmittedImageSerializer

    def perform_create(self, serializer):
        """
        Handles creation of new submitted image.

        The currently logged in user and the image request ID
        is added to the data and passed to the serializer.
        """
        serializer.save(user=self.request.user,
                        image_request=self.request.data['request_id'])


def index(request):
    """
    Renders the landing page.
    """
    return render(request, 'commander/index.dtl', {})


def commander(request):
    objects = ImageRequest.objects
    related = objects.prefetch_related('request_texts')
    requested_images = related.all()

    context = {
        'requested_images': requested_images
    }

    return render(request, 'commander/commander.dtl', context)


def request_image(request):
    requested_images = ImageRequest.objects.all()

    context = {
        'requested_images': requested_images,
        'login_form': {
            'action': 'login/',
            'button_label': 'Login',
    }}

    if request.user.is_authenticated:
        context['login_form'] = {
            'action': 'logout/',
            'button_label': 'Logout'
        }

    return render(request, 'commander/request_image.dtl', context)


@login_required()
def user_overview(request):
    context = {}

    return render(request, 'commander/user.dtl', context)


@login_required()
def user_profile(request):
    context = {}

    return render(request, 'commander/user.dtl', context)


@psa('social:complete')
def register(request, backend):
    """
    Completes the social auth pipeline.
    """
    token = request.GET.get('access_token')
    user = request.backend.do_auth(token)

    if user:
        login(request, user)

    return render(request, 'commander/home.dtl', {})


def logout_oauth(request):
    logout(request)

    return HttpResponse("logout")


def login_oauth(request):
    return render(request, 'commander/login_oauth.dtl')


def home(request):
    """
    Home view where some basic information is displayed.
    """
    context = {}

    if request.user:
        context['user'] = request.user

    return render(request, 'commander/home.dtl', context)


def image_requests(request):
    """
    Displays all image requests.

    This is the main view for image requests. All requests
    are shown with their newest version of the request texts
    and all submitted images.
    """
    objects = ImageRequest.objects \
        .prefetch_related(Prefetch('request_texts',
                                   queryset=RequestText.objects
                                   .order_by('lang', 'image_request_id', '-revision')
                                   .distinct('lang', 'image_request_id')))\
        .prefetch_related(Prefetch('submitted_images',
                                   queryset=SubmittedImage.objects.all()))
    context = {
        'image_requests': objects
    }

    return render(request, 'commander/image_requests.dtl', context)


def user_image_request(request):
    """
    Displays a list of image request by a user.


    """
    creator_objects = ImageRequest.objects.filter(creator_id='2')
    objects = creator_objects\
        .prefetch_related(Prefetch('request_texts',
                                   queryset=RequestText.objects
                                   .order_by('lang', 'image_request_id', '-revision')
                                   .distinct('lang', 'image_request_id')))

    context = {
        'requested_images': objects
    }

    return render(request, 'commander/image_requests.dtl', context)


@login_required()
def add_image_request(request):
    """
    Request an image.
    """
    context = {}

    return render(request, 'commander/request_image.dtl', context)
