from rest_framework import serializers

from blogs.blg.models import BlogTags, BlogCategories, Blogs, BlogComments


class BlogTagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogTags
        fields = '__all__'


class BlogCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogCategories
        fields = '__all__'



class BlogsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blogs
        fields = '__all__'



class BlogCommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogComments
        fields = '__all__'



