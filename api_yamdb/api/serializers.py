from django.core.validators import RegexValidator
from rest_framework import serializers
from titles.models import Categories, Genres, Titles
from users.models import ROLE, User


class UserViewSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(regex=r'^[\w.@+-]+$', max_length=150)
    first_name = serializers.CharField(max_length=150, required=False)
    last_name = serializers.CharField(max_length=150, required=False)
    email = serializers.CharField(max_length=254)
    role = serializers.ChoiceField(
        choices=ROLE,
        default='user',
        required=False
    )

    class Meta:
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role',
        )
        model = User

    def validate_username(self, username):
        if username == 'me':
            raise serializers.ValidationError(
                'Такое имя пользователя недоступно!'
            )
        if User.objects.filter(
            username=username
        ).exists():
            raise serializers.ValidationError(
                'Такое имя уже зарегистрировано!'
            )
        return username

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                'Такая почта уже зарегистрирована!'
            )
        return email


class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=254)
    username = serializers.CharField(
        validators=[RegexValidator(regex=r'^[\w.@+-]+$')],
        max_length=150
    )

    def validate_username(self, username):
        if username == 'me':
            raise serializers.ValidationError(
                'Такое имя пользователя недоступно!'
            )
        return username


class AuthenticatedSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Categories


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Genres


class TitlesSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Titles
