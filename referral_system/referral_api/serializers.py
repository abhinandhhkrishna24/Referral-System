from rest_framework import serializers
from .models import User



class UserRegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)
    referral_code = serializers.CharField(write_only=True, required=False) 

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password','confirm_password', 'referral_code')

        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, attrs):
        if User.objects.filter(username=attrs['username']).exists():
            raise serializers.ValidationError("This username is already in use. Please try another one.")

        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError("Both passwords must match.")

        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password', None)
        referral_code = validated_data.get('referral_code')
        user = User.objects.create_user(**validated_data)
        if referral_code:
            try:
                referrer = User.objects.get(referral_code=referral_code)
                referrer.referral_points += 1
                referrer.save()
            except User.DoesNotExist:
                raise serializers.ValidationError({'referral_code': 'Invalid referral code.'})
        return user


class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'referral_code', 'date_joined')



class ReferralSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'referral_code', 'date_joined']