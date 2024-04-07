from django.urls import path
from .views import UserRegistrationView, UserDetailsView, ReferralsEndpoint

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('details/', UserDetailsView.as_view(), name='user-details'),
    path('referrals/', ReferralsEndpoint.as_view(), name='referrals'),
]
