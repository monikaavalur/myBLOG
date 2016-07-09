from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField
from blog.models import post

class postListSerializer(serializers.ModelSerializer):
    user=SerializerMethodField()
    class Meta:
        model=post
        fields=[
            'user',
            'id',
            'title',
            'slug',
            'content',
            'publish'
        ]

    def get_user(self,obj):
        return str(obj.user.username)

class postDetailSerializer(serializers.ModelSerializer):
    user = SerializerMethodField()
    image = SerializerMethodField()
    markdown=SerializerMethodField()
    class Meta:
        model=post
        fields=[
            'id',
            'user',
            'image',
            'title',
            'slug',
            'content',
            'markdown',
            'publish'
        ]
    def get_markdown(self, obj):
        return obj.get_markdown()

    def get_user(self, obj):
        return str(obj.user.username)

    def get_image(self,obj):
        try:
            image=obj.image.url
        except:
            image=None
        return image

class postCreateUpdateSerializer(serializers.ModelSerializer):
            class Meta:
                model = post
                fields = [
                    'title',
                    'content',
                    'publish'
                ]