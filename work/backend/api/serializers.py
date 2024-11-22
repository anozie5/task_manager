from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


# user serializer
# user creation
class CreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email", "password"]
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 8}
        }

    def validate_password(self, value):
        if not re.search(r'[a-zA-Z]', value) and not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise serializers.ValidationError("Password must contain at least one letter and or one symbol.")
        
        return value
    
    def create(self, validated_data):
        user = super().create(validated_data)            
        user.set_password(validated_data['password'])
        user.save()
        return(user)

# user login
class LoginSerializer(TokenObtainPairSerializer):
    username = serializers.CharField(required=True)

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token
    class Meta:
        model = User
        fields = ["username", "password"]

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                raise serializers.ValidationError('User with this username does not exist.')

            if not user.check_password(password):
                raise serializers.ValidationError('Incorrect password.')
            
            attrs['user'] = user
        else:
            raise serializers.ValidationError('Both email and password are required.')

        return attrs

# for the jobs
# for job
class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'
        exclude = ['owner',]

# for pay
class PaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Pay
        fields = '__all__'