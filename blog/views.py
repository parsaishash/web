from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, FileResponse
from django.urls import reverse

def home(request):
	return render(request, 'blog/home.html')

# Create your views here.
