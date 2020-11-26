from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, FileResponse
from django.urls import reverse
from PIL import Image
from io import BytesIO
from mutagen.mp3 import MP3
import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from pathlib import Path


home_dir = home = str(Path.home())
files_dir = '{}/web/base/static/base/ser'.format(home_dir)

if os.path.isdir('/media/parsa/Elements'):
	files_dir = '/media/parsa/Elements'


def upload(request):
	fs = FileSystemStorage()
	filename = fs.save(request.FILES['myfile'].name, request.FILES['myfile'])

	return render(request, 'base/wel.html')






def authen(request):
	return render(request, 'base/authen.html')


def files_finder(directory):

	files = []
	musics = []
	video = []
	document = []
	images = []


	def add_file(entry, file_format):

	    files.append({'title': entry.name, 'path': entry.path, 'format':file_format})

	    if file_format == 'image':
	    	images.append({'title': entry.name, 'relpath': entry.path, 'path': (' > ').join(entry.path.split('/')), 'format':file_format})

	    elif file_format == 'mp3':
	    	musics.append({'title': entry.name, 'path': (' > ').join(entry.path.split('/')), 'format':file_format})

	    elif file_format == 'video':
	    	video.append({'title': entry.name, 'path': (' > ').join(entry.path.split('/')), 'format':file_format})

	    elif file_format == 'document':
	    	document.append({'title': entry.name, 'path': (' > ').join(entry.path.split('/')), 'format':file_format})

	def add_file_from(directory):
	    for entry in os.scandir(directory):

	        if entry.is_file():
	        	if entry.path[-3:] in ['mp3', 'm4a']:
	        		add_file(entry, 'mp3')

	        	elif entry.path[-3:] in ['png', 'jpeg', 'JPEG', 'jpg', 'PNG']:
	        		add_file(entry, 'image')

	        	elif entry.path[-3:] in ['mp4', 'mkv']:
	        		add_file(entry, 'video')

	        	elif entry.path[-3:] in ['pdf', 'out', 'py', 'cpp']:
	        		add_file(entry, 'document')


	        elif entry.is_dir():
	        	add_file_from(entry.path)


	add_file_from(directory)


	return files, musics, images, video, document




def wel(request):
	return render(request, 'base/wel.html')




def ser(directory):

	video = []
	dir_path = []
	files = []
	sub = []
	print(directory)

	def add_file_ser(entry, file_format):

	    files.append({'title': entry.name, 'relpath': entry.path, 'path': entry.path, 'format':file_format})

	    if file_format == 'video':
	    	video.append({'title': entry.name, 'relpath': entry.path, 'path': (' > ').join(entry.path.split('/')), 'format':file_format})

	    elif file_format == 'directory':
	    	dir_path.append({'title': entry.name, 'path': (' > ').join(entry.path.split('/')), 'format':file_format})

	    elif file_format == 'sub':
	    	sub.append({'title': entry.name, 'path': (' > ').join(entry.path.split('/')), 'format':file_format})

	def add_file_from_ser(directory):
		for entry in os.scandir(directory):

			if entry.is_file():
				if entry.path[-3:] in ['mp4', 'mkv']:
					add_file_ser(entry, 'video')

				elif entry.path[-3:] in ['srt', 'pdf']:
					add_file_ser(entry, 'sub')


			elif entry.is_dir():
				print(entry)
				add_file_ser(entry, 'directory')

	add_file_from_ser(directory)

	return files, dir_path, video, sub




def go_to_directory(request, path, wich_type):
	files_dir = ('/').join(path.split(' > '))

	folder_type = wich_type[0].capitalize() + wich_type[1:]

	if wich_type == 'Serials':
		files, dir_path, video, sub = ser(files_dir)
		wich_type = video + dir_path + sub


	context = {
		'files': wich_type,
		'type': folder_type,
	}

	#return HttpResponse(wich_type)
	return render(request, 'base/home.html', context)




def home(request, wich_type):
	global files_dir

	# add all type files from directory
	files, musics, images, video, document = files_finder('{}/web/base/static/base/ed'.format('/Users/pegah2'))

	# make title start with captal leter for templates
	folder_type = wich_type[0].capitalize() + wich_type[1:]

	# make var for send data to templates
	if wich_type == 'musics':
		wich_type = musics

	elif wich_type == 'files':
		wich_type = files

	elif wich_type == 'images':
		wich_type = images

	elif wich_type == 'video':
		wich_type = video

	elif wich_type == 'document':
		wich_type = document

	elif wich_type == 'serials':

		if os.path.isdir('/media/parsa/Elements'):
			files, dir_path, video, sub = ser('/media/parsa/Elements')
		else:
			files, dir_path, video, sub = ser('{}/web/base/static/base/ser'.format('/Users/pegah2'))

		wich_type =  dir_path


	context = {
		'files': wich_type,
		'type': folder_type,
	}

	return render(request, 'base/home.html', context)



def down(request, path):
	print(path)
	global data

	#decode the path
	path = ('/').join(path.split(' > '))
	return FileResponse(open(path, 'rb'), as_attachment=True)


# Create your views here.
