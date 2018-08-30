from rest_framework import serializers
from django.contrib.auth import get_user_model

from directory.models import Icecreams, Parlor, Comments


class UserSerializer(serializers.ModelSerializer):
	favors = serializers.PrimaryKeyRelatedField(many=True, queryset=get_user_model().objects.all())
	haters = serializers.PrimaryKeyRelatedField(many=True, queryset=get_user_model().objects.all())
	parlors = serializers.PrimaryKeyRelatedField(many=True, queryset=Parlor.objects.all())
	comments = serializers.PrimaryKeyRelatedField(many=True, queryset=Comments.objects.all())
	class Meta:
		model = get_user_model()
		fields = ('username', 'friends', 'DOB', 'token_user_auth', 'favors', 'haters', 'parlors', 'comments')