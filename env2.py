"""-----------------------------------------------
	| Lists Involving Storing File Information |
	| 		  According to Category		   	   |
	--------------------------------------------------"""
"""
[[name, size,  filetype, index], .....]
index: index at which the file is located in 
"""

music = []
image = []
video = []
text = []
pdf = []
empty = []
other = []

music2 = []
image2 = []
video2 = []
text2 = []
pdf2 = []
empty2 = []
other2 = []

#Lists storing information about files to be copied
cp_filetype = [music, image, video, text, pdf, empty, other]

#Lists storing information about files to be deleted
del_filetype = [music2, image2, video2, text2, pdf2, empty2, other2]

#Name of all the filetypes to be displayed in dock1
type_name = ["Audio", "Image", "Video", "Text", "PDF", "Empty", "Other"]
