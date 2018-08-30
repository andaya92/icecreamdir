from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect

# Create your views here.

class Index(TemplateView):
	template_name = 'myprofile/index.html'
	def get(self, request):
		if(request.user.is_authenticated):
			return render(request, self.template_name)
		else:
			return HttpResponseRedirect("/directory/login")