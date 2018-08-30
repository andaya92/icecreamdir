from rest_framework import serializers
from .models import Parlor, HOOperation, Icecreams, Comments
from myfriends.serializer import UserSerializer

class ParlorSerializer(serializers.ModelSerializer):
	class Meta:
		model = Parlor
		fields = "__all__"

class HOOperationSerializer(serializers.ModelSerializer):
	business = ParlorSerializer(read_only=True)
	class Meta:
		model = HOOperation
		fields = "__all__"


class IcecreamsSerializer(serializers.ModelSerializer):
	favors = UserSerializer(read_only=True, many=True)
	haters = UserSerializer(read_only=True, many=True)
	parlors = ParlorSerializer(read_only=True, many=True)
	price = serializers.DecimalField(max_digits=4, decimal_places=2, read_only=True)
	
	class Meta:
		model = Icecreams
		fields = ('id','name', 'flavor', 'kin', 'style', 'price', 'favors', 'haters', 'parlors')




class CommentSerializer(serializers.ModelSerializer):
	user = UserSerializer(read_only=True)
	icecream = IcecreamsSerializer(read_only = True)
	parlor = ParlorSerializer(read_only = True)
	class Meta:
		model = Comments
		fields = "__all__"
