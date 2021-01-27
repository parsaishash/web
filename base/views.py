from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, FileResponse
from django.urls import reverse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib import messages


from PIL import Image
from io import BytesIO
from mutagen.mp3 import MP3 as mp3
from mutagen.id3 import ID3
from mutagen.easyid3 import EasyID3

import os
from pathlib import Path
import base64
from io import StringIO


users = [
	{'username': 'parsa', 'password': '1382'},
	{'username': 'danialbehzadi', 'password': 'danialbehzadi'},
	{'username': 'amirali', 'password': '1382'},
	{'username': 'main', 'password': 'main1234'},
]



home_dir = settings.BASE_DIR
files_dir = '{}/base/static/base/ser'.format(home_dir)

#if os.path.isdir('/media/parsa/Elements'):
#	files_dir = '/media/parsa/Elements'

def player(request, play_path):
	play_path = '/'.join(play_path.split(' > ')[8:])
	return render(request, 'base/player.html', {'path': play_path})

def upload(request):
	fs = FileSystemStorage()
	filename = fs.save(request.FILES['myfile'].name, request.FILES['myfile'])

	return render(request, 'base/wel.html')

def wel(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']

		if {'username': username, 'password': password} in users:
			messages.add_message(request, messages.INFO, 'login successful')
			return render(request, 'base/wel.html')

		else:
			return redirect('base:authen')
	else:
		return render(request, 'base/wel.html')


def authen(request):
	return render(request, 'base/authen.html')

def tet(request):
    return HttpResponse(settings.BASE_DIR)

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

			try:

				s = ID3(entry.path)
				for i in s:
					if i.startswith("APIC:"):
						img = Image.open(BytesIO(s.get(i).data))
						break

				name = '/home/parsa/web/base/static/base/music_image/' + entry.name[:-3] + 'png'
				img.thumbnail((125, 125))
				img.save(name)


				try:
					data = EasyID3(entry.path)
					name = data['title'][0]
					date = data['date'][0]
					artist = data['artist'][0]
					genre = data['genre'][0]
				except:
					name = entry.name[:-4]
					date =''
					artist = ''
					genre = ''

				image_str = entry.name[:-3] + 'png'
				musics.append({'name': name, 'title': entry.name, 'genre': genre, 'artist': artist, 'date': date, 'path': (' > ').join(entry.path.split('/')), 'format':file_format, 'image_str': image_str})



			except:

				try:
					data = EasyID3(entry.path)
					name = data['title'][0]
				except:
					name = entry.name[:-4]

				musics.append({'name': name, 'title': entry.name, 'path': (' > ').join(entry.path.split('/')), 'format':file_format, 'image_str': 'it.png'})



		elif file_format == 'video':
			video.append({'title': entry.name, 'path': (' > ').join(entry.path.split('/')), 'format':file_format})

		elif file_format == 'document':
			document.append({'title': entry.name, 'path': (' > ').join(entry.path.split('/')), 'format':file_format})

	def add_file_from(directory):
		for entry in os.scandir(directory):
			if entry.is_file():
				if entry.path[-3:] in ['mp3', 'm4a']:
					add_file(entry, 'mp3')

				elif entry.path.split('.')[-1] in ['png', 'jpeg', 'JPEG', 'jpg', 'PNG']:
					add_file(entry, 'image')

				elif entry.path[-3:] in ['mp4', 'mkv']:
					add_file(entry, 'video')

				elif entry.path[-3:] in ['pdf', 'out', 'py', 'cpp']:
					add_file(entry, 'document')

				elif entry.is_dir():
					add_file_from(entry.path)

	add_file_from(directory)

	files = sorted(files, key=lambda i: i['title'])
	musics = sorted(musics, key=lambda i: i['name'])
	images = sorted(images, key=lambda i: i['title'])
	video = sorted(video, key=lambda i: i['title'])
	document = sorted(document, key=lambda i: i['title'])

	return files, musics, images, video, document



# ser is for adding files for paths and movies
def ser(directory):

	video = []
	dir_path = []
	files = []
	sub = []
	print(directory)

	def add_file_ser(entry, file_format):

		files.append({'title': entry.name, 'relpath': entry.path, 'path': entry.path, 'format':file_format})

		# adding movies
		if file_format == 'video':
			
			if entry.name[-3:] in ['mp4', 'mkv']:
				video.append({'title': entry.name, 'relpath': entry.path, 'review': True, 'path': (' > ').join(entry.path.split('/')), 'format':file_format})
			else:
				video.append({'title': entry.name, 'relpath': entry.path, 'path': (' > ').join(entry.path.split('/')), 'format':file_format})


		# adding directory path's links
		elif file_format == 'directory':
			dir_path.append({'title': entry.name, 'path': (' > ').join(entry.path.split('/')), 'format':file_format})

		# adding subtitles
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


	# sorting all files for better view
	files = sorted(files, key=lambda i: i['title'])
	dir_path = sorted(dir_path, key=lambda i: i['title'])
	video = sorted(video, key=lambda i: i['title'])
	sub = sorted(sub, key=lambda i: i['title'])

	return files, dir_path, video, sub



# this func is for going in to the paths and serv the files on that directory with ser func
def go_to_directory(request, path, wich_type):

	files_dir = ('/').join(path.split(' > '))

	# folder type for viewin title in front & filtering data
	folder_type = wich_type[0].capitalize() + wich_type[1:]

	if wich_type == 'Serials':
		files, dir_path, video, sub = ser(files_dir)
		wich_type = video + dir_path + sub

	context = {
		'files': wich_type,
		'type': folder_type,
	}

	return render(request, 'base/home.html', context)




def home(request, wich_type):
	global files_dir

	# add all type files from directory
	files, musics, images, video, document = files_finder('{}/base/static/base/ed'.format(home_dir))

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
		files, dir_path, video, sub = ser('{}/web/base/static/base/ser'.format(home_dir))
		wich_type =  dir_path + video


	context = {
		'files': wich_type,
		'type': folder_type,
	}

	return render(request, 'base/home.html', context)


# this func response files for download
def down(request, path):
	print(path)
	global data

	#decode the path
	path = ('/').join(path.split(' > '))
	return FileResponse(open(path, 'rb'), as_attachment=True)


# Create your views here.
