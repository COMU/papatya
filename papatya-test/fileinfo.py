import os
import sys
import magic
#from songs.models import *
from mutagen.mp3 import MP3
from mutagen.flac import FLAC
from mutagen.oggvorbis import OggVorbis
from mutagen.asf import ASF

class MusicInfo:
	def __init__(self,filesrc):
		folderpaths = [path for (path, folders, files) in os.walk(filesrc)]
		filenames = [files for (path, folders, files) in os.walk(filesrc)]
		for i in range(len(folderpaths)):
			for j in range(len(filenames[i])):
				if(i==0):
					filenames[i][j] = folderpaths[i] + filenames[i][j]
				else:
					filenames[i][j] = folderpaths[i] + "/"+ filenames[i][j]

		for i in range(len(folderpaths)):
			for j in range(len(filenames[i])):
				if len(filenames[i]) == 0:
					continue
				temp = i
				src = filenames[i][j]
				mime = magic.open(magic.MAGIC_MIME)
				mime.load()
				mime = mime.file(src).split(";")[0]
				mp3Type = ['audio/mpeg', 'audio/mpeg3', 'audio/x-mpeg', 'audio/x-mpeg-3']
				flacType = ['audio/x-flac', 'audio/flac']
				oggType = ['application/ogg', 'audio/vorbis', 'audio/x-vorbis', 'application/ogg', 'application/x-ogg', 'application/octet-stream', 'audio/ogg', 'video/ogg']
				wmaType = ['video/x-ms-asf','audio/x-ms-wma', 'audio/x-ms-wmv', 'audio/x-wma', 'video/x-wmv', 'application/octet-stream']
				found = 0
				filetype = ""
				if found==0:
					for i in range(len(mp3Type)):
						if mime == mp3Type[i]:
							audio = MP3(src)
							found = 1
							filetype = "mp3"
							break
					for i in range(len(flacType)):
						if mime == flacType[i]:
							audio = FLAC(src)
							found = 1
							filetype = "flac"
							break
					for i in range(len(oggType)):
						if mime == oggType[i]:
							audio = OggVorbis(src)
							found = 1
							filetype = "ogg"
							break
					for i in range(len(wmaType)):
						if mime == wmaType[i]:
							audio = ASF(src)
							found = 1
							filetype = "wma"

				if found!=1:
					print "Data type is not found."
					return
				filedict = dict()
				if filetype == "mp3":
					audioprop = audio.pprint().split("\n")
					fileprop = audioprop[0].split(", ") #fileprop:  u'MPEG 1 layer 3, 320000 bps, 44100 Hz, 246.73 seconds (audio/mp3)'
					filedict['Audio Codec'] = fileprop[0]
					filedict['Bitrate'] = fileprop[1]
					filedict['Sample Rate'] = fileprop[2]
					filedict['Length'] = fileprop[3].split(" (")[0]
					audioprop = audioprop[1:]
					for i in audioprop:
						values = i.split("=")
						filedict[values[0]] = values[1]

					if filedict.has_key("UFID"):
						filedict["Unique File Identifier"] = filedict["UFID"]
						del filedict["UFID"]
					
					if filedict.has_key("TIT1"): 
						filedict["Content group description"] = filedict["TIT1"]
						del filedict["TIT1"]
					
					if filedict.has_key("TIT2"):     
						filedict["Title"] = filedict["TIT2"]
						del filedict["TIT2"]
					
					if filedict.has_key("TIT3"):     
						filedict["Subtitle/Description refinement"] = filedict["TIT3"]
						del filedict["TIT3"]
					
					if filedict.has_key("TPE1"):     
						filedict["Artist"] = filedict["TPE1"]
						del filedict["TPE1"]
					
					if filedict.has_key("TPE2"):     
						filedict["Band"] = filedict["TPE2"]
						del filedict["TPE2"]		 
					
					if filedict.has_key("TPE3"):     
						filedict["Conductor"] = filedict["TPE3"]
						del filedict["TPE3"]		
					
					if filedict.has_key("TPE4"):     
						filedict["Remixer"] = filedict["TPE4"]
						del filedict["TPE4"]
					
					if filedict.has_key("TCOM"):     
						filedict["Composer"] = filedict["TCOM"]
						del filedict["TCOM"]
					
					if filedict.has_key("TEXT"):     
						filedict["Lyricist"] = filedict["TEXT"]
						del filedict["TEXT"]
					
					if filedict.has_key("TLAN"):     
						filedict["Audio Language"] = filedict["TLAN"]
						del filedict["TLAN"]
					
					if filedict.has_key("TCON"):     
						filedict["Genre"] = filedict["TCON"]
						del filedict["TCON"]
					
					if filedict.has_key("TALB"):     
						filedict["Album"] = filedict["TALB"]
						del filedict["TALB"]
					
					if filedict.has_key("TPOS"):     
						filedict["Part of set"] = filedict["TPOS"]
						del filedict["TPOS"]
					
					if filedict.has_key("TRCK"):     
						filedict["Track Number"] = filedict["TRCK"]
						del filedict["TRCK"]
					
					if filedict.has_key("TSRC"):     
						filedict["International Standard Recording Code (ISRC)"] = filedict["TSRC"]
						del filedict["TSRC"]
					
					if filedict.has_key("TYER"):     
						filedict["Recording Year"] = filedict["TYER"]
						del filedict["TYER"]
					
					if filedict.has_key("TDAT"):
						filedict["Recording Date (DDMM)"] = filedict["TDAT"]
						del filedict["TDAT"]
					
					if filedict.has_key("TDRC"):
						filedict["Recording Time"] = filedict["TDRC"]
						del filedict["TDRC"]

					if filedict.has_key("TRDA"):
						filedict["Recording Dates"] = filedict["TRDA"]
						del filedict["TRDA"]
					
					if filedict.has_key("TMED"):
						filedict["Source Media Type"] = filedict["TMED"]
						del filedict["TMED"]
					
					if filedict.has_key("TFLT"):
						filedict["File Type"] = filedict["TFLT"]
						del filedict["TFLT"]
					
					if filedict.has_key("TBPM"):
						filedict["Beats per minute"] = filedict["TBPM"]
						del filedict["TBPM"]

					if filedict.has_key("TCOP"):
						filedict["Copyright"] = filedict["TCOP"]
						del filedict["TCOP"]

					if filedict.has_key("TPUB"):
						filedict["Publisher"] = filedict["TPUB"]
						del filedict["TPUB"]

					if filedict.has_key("TENC"):
						filedict["Encoder"] = filedict["TENC"]
						del filedict["TENC"]

					if filedict.has_key("TSSE"):
						filedict["Encoder settings"] = filedict["TSSE"]
						del filedict["TSSE"]

					if filedict.has_key("TOFN"):
						filedict["Original Filename"] = filedict["TOFN"]
						del filedict["TOFN"]

					if filedict.has_key("TLEN"):
						filedict["Audio Length(ms)"] = filedict["TLEN"]
						del filedict["TLEN"]

					if filedict.has_key("TSIZ"):
						filedict["Audio Data size (bytes)"] = filedict["TSIZ"]
						del filedict["TSIZ"]

					if filedict.has_key("TDLY"):
						filedict["Audio Delay (ms)"] = filedict["TDLY"]
						del filedict["TDLY"]

					if filedict.has_key("TKEY"):
						filedict["Starting Key"] = filedict["TKEY"]
						del filedict["TKEY"]

					if filedict.has_key("TOAL"):
						filedict["Original Album"] = filedict["TOAL"]
						del filedict["TOAL"]

					if filedict.has_key("TOPE"):
						filedict["Original Artist/Perfomer"] = filedict["TOPE"]
						del filedict["TOPE"]

					if filedict.has_key("TOLY"):
						filedict["Original Lyricist"] = filedict["TOLY"]
						del filedict["TOLY"]

					if filedict.has_key("TORY"):
						filedict["Original Release Year"] = filedict["TORY"]
						del filedict["TORY"]

					if filedict.has_key("TXXX"):
						filedict["User-defined Text"] = filedict["TXXX"]
						del filedict["TXXX"]

					if filedict.has_key("WOAF"):
						filedict["Official File Information"] = filedict["WOAF"]
						del filedict["WOAF"]

					if filedict.has_key("WOAR"):
						filedict["Official Artist/Performer Information"] = filedict["WOAR"]
						del filedict["WOAR"]

					if filedict.has_key("WOAS"):
						filedict["Official Source Information"] = filedict["WOAS"]
						del filedict["WOAS"]

					if filedict.has_key("WCOM"):
						filedict["Commercial Information"] = filedict["WCOM"]
						del filedict["WCOM"]

					if filedict.has_key("WCOP"):
						filedict["Copyright Information"] = filedict["WCOP"]
						del filedict["WCOP"]

					if filedict.has_key("WPUB"):
						filedict["Official Publisher Information"] = filedict["WPUB"]
						del filedict["WPUB"]

					if filedict.has_key("WXXX"):
						filedict["User-defined URL"] = filedict["WXXX"]
						del filedict["WXXX"]

					if filedict.has_key("IPLS"):
						filedict["Involved people list"] = filedict["IPLS"]
						del filedict["IPLS"]

					if filedict.has_key("MCDI"):
						filedict["Binary dump of CD's TOC"] = filedict["MCDI"]
						del filedict["MCDI"]

					if filedict.has_key("ETCO"):
						filedict["Event timing codes"] = filedict["ETCO"]
						del filedict["ETCO"]

					if filedict.has_key("MLLT"):
						filedict["MPEG location lookup table"] = filedict["MLLT"]
						del filedict["MLLT"]

					if filedict.has_key("SYTC"):
						filedict["Synced tempo codes"] = filedict["SYTC"]
						del filedict["SYTC"]

					if filedict.has_key("USLT"):
						filedict["Unsychronised lyrics/text transcription"] = filedict["USLT"]
						del filedict["USLT"]

					if filedict.has_key("SYLT"):
						filedict["Synchronised lyrics/text"] = filedict["SYLT"]
						del filedict["SYLT"]

					if filedict.has_key("COMM"):
						filedict["Comment"] = filedict["COMM"]
						del filedict["COMM"]

					if filedict.has_key("RVRB"):
						filedict["Reverb"] = filedict["RVRB"]
						del filedict["RVRB"]
				  
					if filedict.has_key("APIC"):
						filedict["Attached Picture"] = filedict["APIC"]
						del filedict["APIC"]

					if filedict.has_key("GEOB"):
						filedict["General Encapsulated Object"] = filedict["GEOB"]
						del filedict["GEOB"]

					if filedict.has_key("PCNT"):
						filedict["Play counter"] = filedict["PCNT"]
						del filedict["PCNT"]

					if filedict.has_key("POPM"):
						filedict["Popularimeter"] = filedict["POPM"]
						del filedict["POPM"]

					if filedict.has_key("RBUF"):
						filedict["Recommended buffer size"] = filedict["RBUF"]
						del filedict["RBUF"]

					if filedict.has_key("Frame"):
						filedict["Encrypted meta frame"] = filedict["Frame"]
						del filedict["Frame"]

					if filedict.has_key("AENC"):
						filedict["Audio encryption"] = filedict["AENC"]
						del filedict["AENC"]

					if filedict.has_key("LINK"):
						filedict["Linked information"] = filedict["LINK"]
						del filedict["LINK"]
						
					for i in filedict:
						print i, ": ",filedict[i]
				
				if filetype == "flac":
					audioprop = audio.pprint().split("\n")
					fileprop = audioprop[0].split(", ") #fileprop:  u'MPEG 1 layer 3, 320000 bps, 44100 Hz, 246.73 seconds (audio/mp3)'
					tempdict = dict()
					tempdict['Audio Codec'] = fileprop[0]
					tempdict['Length'] = fileprop[1]
					tempdict['Sample Rate'] = fileprop[2].split(" (")[0]
					audioprop = audioprop[1:]	
					for i in audioprop:
						values = i.split("=")
						filedict[values[0]] = values[1]
	
					if filedict.has_key("title"):
						tempdict["Title"] = filedict["title"]

					if filedict.has_key("date"):
						tempdict["Year"] = filedict["date"]

					if filedict.has_key("composer"):
						tempdict["Composer"] = filedict["composer"]
					
					if filedict.has_key("style"):
						tempdict["Style"] = filedict["style"]
					
					if filedict.has_key("album"):
						tempdict["Album"] = filedict["album"]
					
					if filedict.has_key("genre"):
						tempdict["Genre"] = filedict["genre"]
					
					if filedict.has_key("artist"):
						tempdict["Artist"] = filedict["artist"]
						
					if filedict.has_key("rating"):
						tempdict["Rating"] = filedict["rating"]
					
					if filedict.has_key("tracknumber"):
						tempdict["Track Number"] = filedict["tracknumber"]
					
					if filedict.has_key("totaltracks"):
						tempdict["Total Tracks"] = filedict["totaltracks"]

					if filedict.has_key("discnumber"):
						tempdict["Disc Number"] = filedict["discnumber"]

					if filedict.has_key("totaldiscs"):
						tempdict["Total Discs"] = filedict["totaldiscs"]
			
					filedict.clear()
					for i in tempdict:
						print i, ": ", tempdict[i]		

				if filetype == "ogg":
					audioprop = audio.pprint().split("\n")
					fileprop = audioprop[0].split(", ") #fileprop:  u'MPEG 1 layer 3, 320000 bps, 44100 Hz, 246.73 seconds (audio/mp3)'
					tempdict = dict()
					tempdict['Audio Codec'] = fileprop[0]
					tempdict['Length'] = fileprop[1]
					tempdict['Bitrate'] = fileprop[2].split(" (")[0]
					audioprop = audioprop[1:]
					for i in audioprop:
						values = i.split("=")
						filedict[values[0]] = values[1]
					
					if filedict.has_key("title"):
						tempdict["Title"] = filedict["title"]

					if filedict.has_key("date"):
						tempdict["Year"] = filedict["date"]

					if filedict.has_key("composer"):
						tempdict["Composer"] = filedict["composer"]
					
					if filedict.has_key("style"):
						tempdict["Style"] = filedict["style"]
					
					if filedict.has_key("album"):
						tempdict["Album"] = filedict["album"]
					
					if filedict.has_key("genre"):
						tempdict["Genre"] = filedict["genre"]
					
					if filedict.has_key("artist"):
						tempdict["Artist"] = filedict["artist"]
						
					if filedict.has_key("rating"):
						tempdict["Rating"] = filedict["rating"]

					if filedict.has_key("tracknumber"):
						tempdict["Track Number"] = filedict["tracknumber"]

					if filedict.has_key("totaltracks"):
						tempdict["Total Tracks"] = filedict["totaltracks"]
					
					if filedict.has_key("discnumber"):
						tempdict["Disc Number"] = filedict["discnumber"]

					if filedict.has_key("totaldiscs"):
						tempdict["Total Discs"] = filedict["totaldiscs"]

					filedict.clear()
					for i in tempdict:
						print i, ": ", tempdict[i]			
				"""if filetype == "wma":
					tempdict = dict()
					filedict = audio
					tempdict["Audio Codec"] = "Wma"
					if filedict.has_key("Author"):
						tempdict["Artist"] = filedict["Author"]			
					
					if filedict.has_key('Title'):
						tempdict['Title'] = filedict['Title']          

					if filedict.has_key("'WM/AlbumArtist'"):
						tempdict["Artist"] = filedict["'WM/AlbumArtist'"]


					if filedict.has_key("WM/AlbumTitle"):
						tempdict["Album"] = filedict["WM/AlbumTitle"]


					if filedict.has_key("WM/Composer"):
						tempdict["Composer"] = filedict["WM/Composer"]


					if filedict.has_key("WM/Genre"):
						tempdict["Genre"] = filedict["WM/Genre"]


					if filedict.has_key("'WM/Lyrics'"):
						tempdict["Lyrics"] = filedict["'WM/Lyrics'"]


					if filedict.has_key("WM/Provider"):
						tempdict["Provider"] = filedict["WM/Provider"]


					if filedict.has_key("WM/Publisher"):
						tempdict["Publisher"] = filedict["WM/Publisher"]


					if filedict.has_key("WM/TrackNumber"):
						tempdict["Track Number"] = filedict["WM/TrackNumber"]


					if filedict.has_key("WM/Track"):
						tempdict["Disc Number"] = filedict["WM/Track"]
					
					if filedict.has_key("WM/Year"):
						tempdict["Year"] = filedict["WM/Year"]

					filedict.clear()
					for i in tempdict:
						if tempdict[i] == 
						print i , ":", tempdict[i]
				"""	
				i = temp
				print "------------------------------"
if __name__ == '__main__':
    if len(sys.argv) == 2:
        MusicInfo(sys.argv[1])
    else:
        print 'Usage: %s /home/user/media/file' % sys.argv[0]
