from rest_framework import serializers
from .models import Category, Tag, News, Comment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'created_at']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']


class NewsSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    tags = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Tag.objects.all(), required=False
    )
    class Meta:
        model = News
        fields = ['id', 'title', 'slug', 'content',
                  'category', 'tags', 'image',
                  'views_count', 'is_published', 'created_at', 'updated_at']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        category = Category.objects.get(pk=representation.get('category'))
        representation['category'] = {
            'id': category.id,
            'name': category.name,
        }
        return representation



class CommentSerializer(serializers.ModelSerializer):
    news = serializers.PrimaryKeyRelatedField(queryset=News.objects.all())
    class Meta:
        model = Comment
        fields = ['id', 'news', 'author_name', 'author_email', 'content',
                  'is_published', 'created_at']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        news = News.objects.get(pk=representation.get('news'))
        representation['news'] = {
            'id': news.id,
            'name': news.title,
        }
        return representation