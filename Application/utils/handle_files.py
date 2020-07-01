from Application import app
import os
from PIL import Image
from random import randint
from werkzeug.utils import secure_filename

def save_picture(picture,directory,x,y):
	f_name, f_ext = os.path.splitext(picture.filename)
	picture_fn = "".join([f_name,str(randint(1000000,1000000000000)),f_ext])
	picture_path = os.path.join(app.root_path, directory , picture_fn)
	output_size = (x,y)
	i = Image.open(picture)
	i.thumbnail(output_size)
	i.save(picture_path)
	return picture_fn

def save_document(form_document):
	f_name, f_ext = os.path.splitext(form_document.filename)
	document = "".join([f_name,str(randint(1000000,1000000000000)),f_ext]).replace(' ','_')
	form_document.save(os.path.join(app.root_path, 'static/vendor_documents', secure_filename(document)))
	return document