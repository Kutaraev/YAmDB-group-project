from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Category, Comment, Genre, Review, Title, UserRegistration

User = get_user_model()


class RoleField(serializers.ChoiceField):
    def to_representation(self, value):
        return self._choices[value]

    def to_internal_value(self, data):
        for key, value in self._choices.items():
            if value == data:
                return key
        self.fail('invalid_choice', input=data)
        return 1


class UserSerializer(serializers.ModelSerializer):
    role = RoleField(choices=User.USER_ROLE_CHOICES)

    class Meta:
        fields = (
            'username', 'email', 'role', 'first_name', 'last_name', 'bio',
        )
        model = User


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('email',)
        model = UserRegistration

    def save(self):
        email = self.validated_data['email']
        confirmation_code = get_random_string(length=16)
        UserRegistration.objects.create(
            email=email, confirmation_code=confirmation_code
        )
        send_mail(
            'YaMDb Registration',
            f'Your Confirmation Code: {confirmation_code}',
            settings.DEFAULT_FROM_EMAIL,
            (email,)
        )


class TokenObtainSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255, write_only=True)
    confirmation_code = serializers.CharField(max_length=16, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get('email')
        confirmation_code = data.get('confirmation_code')
        registration_record = get_object_or_404(
            UserRegistration, email=email
        )
        if registration_record.confirmation_code == confirmation_code:
            user, created = User.objects.get_or_create(email=email)
            if created:
                user.username = email
                user.save()
            token = RefreshToken.for_user(user)
            return {
                'token': str(token.access_token),
            }
        raise serializers.ValidationError('Wrong Confirmation Code')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ('id',)
        model = Category


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ('id',)
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        many=True, slug_field='slug', queryset=Genre.objects.all()
    )

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre', 'category',)
        read_only_fields = ('id',)
        model = Title


class TitlesListSerializer(serializers.ModelSerializer):
    genre = GenresSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.FloatField()

    class Meta:
        fields = (
            'id', 'name', 'year', 'description', 'genre', 'category', 'rating'
        )
        read_only_fields = ('id', 'rating',)
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = '__all__'
        read_only_fields = ('title',)
        model = Review

    def validate(self, data):
        my_view = self.context['view']
        title_id = my_view.kwargs.get('title_id')
        user = self.context['request'].user

        if self.context['request'].method == 'POST' and Review.objects.filter(
                author__username=user.username,
                title__id=title_id
        ).exists():
            raise serializers.ValidationError(
                'Вы уже оставили свой отзыв.'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment
