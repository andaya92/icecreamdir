from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.core import serializers

from django.contrib.auth import logout, login, authenticate
from django.contrib.auth import get_user_model

from .models import Icecreams, Comments
from .forms import IcecreamsForm, UserForm
from .serializer import IcecreamsSerializer

#===============================================================================
# REST FRAMEWORK IMPORTS
#===============================================================================

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework import generics
from rest_framework.renderers import JSONRenderer
from rest_framework import status

User = get_user_model()

def isFav(icecream, user):
	return True if user in icecream.favors.all() else False

def isHated(icecream, user):
	return True if user in icecream.haters.all() else False

def isSaved(icecream, user):
	return (isFav(icecream, user) or isHated(icecream, user))

def LogOutUser(request):
    logout(request)
    return redirect("/directory/login/")

class CreateUser(TemplateView):
    
    form_class = UserForm # forms.py
    template_name = 'directory/createuserform.html'
    
    #Display blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = self.form_class(request.POST)
        
        if form.is_valid():
            #Create object to save later (does not save to DB)
            user = form.save(commit = False)
            p_match = False

            #Clean and normalized data (proper formatting)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']    
            password1 = request.POST['password_check'] 

            if not password1:
                form.add_error("password","You must confirm your password")
            elif password != password1:
                print("passwords do not match")
       	        form.add_error("password", "Your passwords do not match")
            else:
                p_match = True
                try:
    	            user.set_password(password)
    	            user.save()
                    #Returns User object if credentials are correct
    	            user = authenticate(username=username, password=password)
                except:
                    print('Error creating user')
            # ## On a thread, create two subscriptions for a new user
            # # Website and Snapchat == Holds days left of membership etc...
            # try:
            #     kwargs ={}
            #     args = (user.id,None)
            #     mythread = _thread.start_new_thread(self.createSubs,args,kwargs)
            # except:
            #     print("Could not create user's subscriptions")

            if user is not None:
                print(user)
                if user.is_active and p_match:
                    print("is active")
                    login(request, user)
                    return redirect('index')

        return render(request, self.template_name, {'form': form})


class Index(TemplateView):
	template_name = "directory/index.html"
	def get(self, request):
		if(request.user.is_authenticated):
			return render(request, self.template_name)
		else:
			return HttpResponseRedirect("/directory/login")


#update an icecream's saved status

## Change to HTTP patch possibly (only updating a field)
class UpdateSavedIcecream(APIView):
	authentication_classes = (SessionAuthentication, BasicAuthentication)
	permission_classes = (IsAuthenticated,)
	def post(self, request):
		## Get icecream pk and user pk
		icecream, user = request.data["icecreamid"],request.data["userid"]
		# Favor or hated
		field = request.data['field']
		#Remove from or Add
		removeOrAdd = request.data['rmoradd']
		myresp = ""
		icecreamUpdate = Icecreams.objects.get(pk=icecream)
		try:
			if(field == "haters"):
				if(removeOrAdd == "add"):
					print("adding haters")
					icecreamUpdate.haters.add(user)
					myresp = "AH"
				else:
					print("removing haters")
					icecreamUpdate.haters.remove(user)
					myresp = "RH"
			elif(field == "favors"):
				if(removeOrAdd == "add"):
					print("Add favors")
					icecreamUpdate.favors.add(user)
					myresp = "AF"
				else:
					print("Remove favors")
					icecreamUpdate.favors.remove(user)
					myresp = "RF"
		except:
			return Response("{}".format("Could not update favorites"))
	
		return Response(myresp)

class IcecreamDetails(TemplateView):
	template_name = "directory/itemdetails.html"
	authentication_classes = (SessionAuthentication, BasicAuthentication)
	permission_classes = (IsAuthenticated,)
	# Displays information about an icecream relevant to the user
	# Allows user to see ice cream info
	# Their comments on the icecream
	# Whether or not it is faved or hated
	# Option to add(to fav or hate) or remove (from fav or hate)

	def get(self, request, pk, frompg):
		icecream = Icecreams.objects.get(pk=pk)
		comments = Comments.objects.filter(icecream=pk)
		faved = isFav(icecream, request.user) 
		hated = isHated(icecream, request.user) 
		saved = isSaved(icecream, request.user)
		print(faved, hated, saved)
		print(icecream)
		print(comments)
		print(frompg)
		return render(request, self.template_name, {"icecream":icecream, "comments": comments,\
		 "frompg":frompg, "faved":faved, "hated":hated})

## Query all Icecream
class QueryIce(APIView):
	authentication_classes = (SessionAuthentication, BasicAuthentication)
	permission_classes = (IsAuthenticated,)
	## icecreams/<str:name>/<str:flavor>/<str:kin>/<str:style>/<str:price>'
	def get(self, request, name, flavor, kin, style, price):
		results, start, end= None, 0, 10000
		if(name=="_"):
			name = ""
		if(flavor=="_"):
			flavor = ""
		if(kin=="_" or kin == "All"):
			kin = ""
		if(style=="_"):
			style = ""
		if(not price=="-1"):
			start, end = int(price)-2, int(price)+2

		## Filter by all fields, if empty, returns all.
		## Query built using underscores as empty indicators
		results = Icecreams.objects.filter(name__icontains=name, flavor__icontains=flavor, kin__icontains=kin, style__icontains=style, price__range=(start, end))\
		.only('name', 'image', 'kin', 'price', 'favors','haters','parlors')

		if(results):
			data = serializers.serialize( "python", results, fields=('name', 'image', 'kin', 'price', 'favors','haters', 'parlors'))
			return Response(data)
		return Response("ERROR: directory.views.QueryIce::{}:{} error serializing".format(name, kin))

class QueryComments(APIView):
	authentication_classes = (SessionAuthentication, BasicAuthentication)
	permission_classes = (IsAuthenticated,)
	## directory/query/comments/<str:field>/<str:value>
	def get(self, request, field, value):
		"""
			Get Comment by field and value
		"""
		results = None
		## Return all comments for a specific user
		if(field == "user"):
			results = Comments.objects.filter(user=value)
		## Return all comments for an icecream
		elif(field == "icecream"):
			results = Comments.objects.filter(icecream=value)
		if(serializer):
			return Response(serializers.serialize("python", results))
		return Response("directory.views.QueryComments::{}:{} error serializing".format(field, value))

	def post(self, request):
		"""
			Add Comment
		"""
		update_id, user = request.data["update_id"], request.data["userid"]
		update_cmt_id = request.data["update_cmt_id"]
		comment_text = request.data['c_text']
		
		print("Trying to update")
		print("ID:"+update_id, user, comment_text)
		myresp = ""

		comment = Comments()
		try:
			print("adding comment")
			comment.user_id = user
			comment.icecream_id = update_id
			comment.comment = comment_text
			comment.save()
			myresp = "AC"
		except :
			return Response("{}".format("Failed, token good"))
		return Response(myresp)

	def delete(self, request):
		"""
			Remove Comment
		"""
		update_id, user = request.data["update_id"], request.data["userid"]
		update_cmt_id = request.data["update_cmt_id"]
		comment_text = request.data['c_text']
		
		print("Trying to update")
		print("ID:"+update_id, user, comment_text)
		myresp = ""
		try:
			print("removing comment")
			comment_to_rm = Comments.objects.get(pk=update_cmt_id)
			comment_to_rm.delete()
			myresp = "RC"
		except :
			return Response("{}".format("Failed removing comment"))
		return Response(myresp)

class GetUserCommentOnIceCream(APIView):
	authentication_classes = (SessionAuthentication, BasicAuthentication)
	permission_classes = (IsAuthenticated,)
	## directory/query/comments/<int:user>1/<int:icecream>1
	def get(self, request, user, icecream):
		comments = Comments.objects.filter(user=user, icecream=icecream)
		data = serializers.serialize( "python", comments )
		print(data)
		if(data):
			return Response(data)
		return Response("directory.views.GetUserCommentOnIceCream::{}:{} error serializing".format(user, icecream))

class GetUserTried(APIView):
	authentication_classes = (SessionAuthentication, BasicAuthentication)
	permission_classes = (IsAuthenticated,)
	## query/user/triedicecream/<int:user>/<str:field>
	def get(self, request, user, field):
		user = get_user_model().objects.get(pk=user)
		if(user):
			data = None
			if(field=="favorites"):
				data = serializers.serialize("python", user.favors.all(), fields=('name', 'image', 'flavor', 'kin', 'style', 'price', 'favors', 'haters'))
			elif(field=="dislikes"):
				data = serializers.serialize("python", user.haters.all(), fields=('name', 'image', 'flavor', 'kin', 'style', 'price', 'favors', 'haters'))
			if(data):
				return Response(data)
		return Response("ERROR directory.views.GetUserCommentOnIceCream::{}error serializing".format(user))		