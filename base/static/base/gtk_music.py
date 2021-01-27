import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib, GdkPixbuf
import os

def image_define(filename,w,h):
    return Gtk.Image.new_from_pixbuf(GdkPixbuf.Pixbuf.new_from_file_at_scale(filename=filename,width=w,height=h,preserve_aspect_ratio=True))

image_list = []

win = Gtk.Window()
win.set_title("Music")
win.set_default_size(600, 600)
scrolledwin = Gtk.ScrolledWindow()


listbox = Gtk.ListBox()


for entry in os.scandir('music_image/'):
	if entry.is_file() and entry.path.endswith('.png'):
		box = Gtk.HBox(spacing=5)

		img = image_define(entry.path, 50, 50)
		image_list.append(img)

		image = Gtk.Button(icon=img, xalign=0, label=entry.name)

		#label = Gtk.Label(label=entry.name, xalign=0)

		box.pack_start(image, True, True, 0)
		#box.pack_start(label, True, True, 0)

		
		listbox.add(box)


scrolledwin.add(listbox)
win.add(scrolledwin)
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()