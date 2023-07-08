from rest_framework import serializers
from .models import Post
from taggit_serializer.serializers import TaggitSerializer
from django.contrib.auth.models import User
from taggit.models import Tag
from django.contrib.auth.models import User

class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ("name", "slug")
        lookup_field = 'name'
        extra_kwargs = {
            'url': {'lookup_field': 'name'}
        }


class PostSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    author = serializers.SlugRelatedField(slug_field="username", queryset=User.objects.all())

    class Meta:
        model = Post
        fields = ("id", "title", "slug", "content", "image", "published", "created_at", "updated_at", "author", "tags")
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }



class ContactSerializer(serializers.Serializer):
    name = serializers.CharField()
    email = serializers.CharField()
    subject = serializers.CharField()
    message = serializers.CharField()


class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "email",
            "password",
            "password2",
        ]
        extra_kwargs = {"password": {
         "write_only": True
        }}

    def create(self, validated_data):
        email = validated_data["email"]
        password = validated_data["password"]
        password2 = validated_data["password2"]
        if password != password2:
            raise serializers.ValidationError({"password": "Пароли не мовпадают"})
        user = User(username=email, email=email)
        user.set_password(password)
        user.save()
        return user
    



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'




from .models import Comment


class CommentSerializer(serializers.ModelSerializer):

    username = serializers.SlugRelatedField(slug_field="username", queryset=User.objects.all())
    post = serializers.SlugRelatedField(slug_field="slug", queryset=Post.objects.all())

    class Meta:
        model = Comment
        fields = ("id", "post", "username", "text", "created_at")
        lookup_field = 'id'
        extra_kwargs = {
            'url': {'lookup_field': 'id'}
        }
