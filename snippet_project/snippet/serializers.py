from rest_framework import serializers
from .models import Snippet, Tag

class TagSerializer(serializers.ModelSerializer):

	class Meta:
		model = Tag
		fields = '__all__'


class SnippetSerializer(serializers.ModelSerializer):
	snippet_url = serializers.HyperlinkedIdentityField(view_name='snippet-detail')

	class Meta:
		model = Snippet
		fields = ['title', 'content', 'timestamp', 'snippet_url']


	# def __init__(self, *args, **kwargs):
	# 	super().__init__(*args, **kwargs)

	# 	# Check if the user is a superuser
	# 	request = self.context.get('request')
	# 	if request.method == 'POST':
	# 		kwargs['data']['created_user'] = request.user.id
	# 	# if request and request.user.is_superuser:
	# 	# 	self.Meta.depth = 1

	def create(self, validated_data):
		tag, created = Tag.objects.get_or_create(title=validated_data['title'])
		validated_data['tag'] = tag
		return Snippet.objects.create(**validated_data)

	def update(self, instance, validated_data):
		tag, created = Tag.objects.get_or_create(title=validated_data['title'])
		if created:
			validated_data['tag'] = tag
		return super().update(instance, validated_data)