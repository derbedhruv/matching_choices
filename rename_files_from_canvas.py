# canvas provides weird prefixes to file names
import os,sys

folder = "/Users/derbedhruv/Downloads/submissions/"	# Be inside the folder you want to rename the files

for filename in os.listdir(folder):
       infilename = os.path.join(folder,filename)
       if not os.path.isfile(infilename): continue
       try:
       	newname = "STLP" + filename.split("_STLP")[1]
       	print newname
       except:
       	# these are the assholes that can't follow instructions
       	print filename
       output = os.rename(infilename, os.path.join(folder,newname))