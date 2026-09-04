from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from shop.models import Member, Banner


class MemberCreateSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField(required=True, write_only=True)
    password = serializers.CharField(required=True, write_only=True)
    first_name = serializers.CharField(required=True, write_only=True)
    last_name = serializers.CharField(required=True, write_only=True)
    address = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        if User.objects.filter(username=attrs['email']).exists():
            raise serializers.ValidationError({"email": "Duplicate email detected"})
        return attrs

    def create(self, validated_data):
        email = validated_data.pop('email')
        password = validated_data.pop('password')
        first_name = validated_data.pop('first_name')
        last_name = validated_data.pop('last_name')
        address = validated_data.pop('address')
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        return Member.objects.create(user=user, address=address)


class MemberSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')

    class Meta:
        model = Member
        fields = ['id', 'email', 'first_name', 'last_name', 'address']


class MemberLoginSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField(required=True, write_only=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('username', None)

    def validate(self, attrs):
        attrs['username'] = attrs.pop('email')
        data = super().validate(attrs)
        member = Member.objects.get(user=self.user)
        
        return {
            'token': data['access'],
            'user': MemberSerializer(member).data
        }


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = "__all__"
