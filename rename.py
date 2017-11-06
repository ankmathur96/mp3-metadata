import os
from mutagen.id3 import ID3, TPE1
BASE_DIR = 'om_shanti_om/'
ARTIST_PROMPT = True
def print_meta(a):
	for x in a.keys():
		if 'APIC' not in x:
			print(x, a[x])

for f in os.listdir(BASE_DIR):
	if f.split('.')[1] == 'mp3':
		print(f)
		audio_file = ID3(BASE_DIR + f)
		print('*****State of the metadata before adjustment:*****')
		print_meta(audio_file)
		# adjust Title
		if 'TIT2' in audio_file.keys():
			title_obj = audio_file['TIT2']
			tokens = title_obj.text[0].split()
			tokens = [x for x in tokens if not '.com' in x.lower()]
			title = ' '.join(tokens)
			audio_file['TIT2'].text[0] = title
		# adjust Album name (usually has other trash in it)
		if 'TALB' in audio_file.keys():
			alb_obj = audio_file['TALB']
			tokens = alb_obj
			tokens = alb_obj.text[0].split()
			tokens = [x for x in tokens if x.isalpha() and '.com' not in x.lower()]
			album_tit = ' '.join(tokens)
			audio_file['TALB'].text[0] = album_tit
		# This is the artist - prompt if you want to, but otherwise, it's usually full of crap.
		if ARTIST_PROMPT:
			artist_name = input('Artist name: ')
			audio_file['TPE1'] = TPE1(encoding=3, text=[artist_name])
		else:
			audio_file.delall('TPE1')
		# This is the composer field - it tends to be full of crap - override if you want.
		if 'TCOM' in audio_file.keys():
			audio_file.delall('TCOM')
		# This is the publisher field - almost always full of crap.
		if 'TPUB' in audio_file.keys():
			audio_file.delall('TPUB')
		# This is the subtitle field - full of crap.
		if 'TIT3' in audio_file.keys():
			audio_file.delall('TIT3')
		# Song comment field - full of crap.
		if 'COMM::eng' in audio_file.keys():
			audio_file.delall('COMM::eng')

		audio_file.save()
		print('*****State of the metadata AFTER adjustment:*****')
		print_meta(audio_file)