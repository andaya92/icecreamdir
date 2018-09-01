from django.shortcuts import render, redirect
from django.views.generic import TemplateView

class Index(TemplateView):
	template_name = "icecreamshop/index.html"