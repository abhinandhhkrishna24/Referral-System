from rest_framework import generics, status, permissions
from .models import User
from .serializers import UserRegistrationSerializer, UserDetailsSerializer, ReferralSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from .pagination import CustomPagination

class UserRegistrationView(generics.CreateAPIView):
    """
    User Registration Endpoint:
    - Accepts POST requests
    - Required fields: username, email, password and confirm password
    - Optional field: referral_code
    - Returns a unique user ID and a success message , the unique user ID user as new users refferal ID
    """

    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):


        """
        Create a new user

        Returns:
        - user_id: The unique ID of the newly created user (integer)
        - referral_code: The referral code assigned to the user (string)
        - message: A success message indicating that the user was created (string)
        - token: JWT token for authentication (string)
        """
       
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        user = serializer.instance

        refresh = RefreshToken.for_user(user)
        token = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

        return Response({
            'user_id': user.id,
            'referral_code': user.referral_code,
            'message': 'User created successfully',
            'token': token,
        }, status=status.HTTP_201_CREATED)


class UserDetailsView(generics.RetrieveAPIView):
    """
    User Details Endpoint:
    - Accepts GET requests
    - Requires an Authorization header with a valid token
    - Returns the user's details
    """

    queryset = User.objects.all()
    serializer_class = UserDetailsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve user details
        """
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class ReferralsEndpoint(generics.ListAPIView):
    """
    Referrals Endpoint:
    - Accepts GET requests
    - Requires an Authorization header with a valid token
    - Returns a list of users who registered using the current user's referral code
    - Returns the timestamp of registration for each referral
    """

    queryset = User.objects.all()
    serializer_class = ReferralSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        """
        Retrieve user's referrals.
        """
        referral_code = self.request.user.referral_code
        return User.objects.filter(referral_code=referral_code).order_by('-date_joined')
