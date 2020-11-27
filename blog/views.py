from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, FileResponse
from django.urls import reverse


def home(request):
	return HttpResponse('hello to my blog')

# Create your views here.
