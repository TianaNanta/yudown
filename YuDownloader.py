# importing the module
from pytube import exceptions, YouTube, Playlist, Search
from pytube.cli import on_progress


def SingleDownload():
	# link of the video to be downloaded
	link=[]
	ln = input("Enter the video link: ")
	while ln != "":
		link.append(ln)
		ln = input("Enter the next link: (Just enter if finished) ")
	#where to save
	locate=input("\nWhere to save it ? ")

	for i in link:
		try:
			# object creation using YouTube
			# which was imported in the beginning
			yt = YouTube(i, on_progress_callback=on_progress)
		except exceptions.VideoPrivate:
			print("Video is private !") #to handle exception
		except exceptions.VideoRegionBlocked:
			print("Video is blocked !")
		except exceptions.VideoUnavailable:
			print("Video is not available !")
		else:
			print("1- Audio\n2- Video\n3- All")
			format = int(input("Select format: "))
			print()

			if format == 1:
				fileExtension = []
				fileAudio = []
				audio = []
     
				for stream in yt.streams.order_by('mime_type').filter(type='audio'):
					fileExtension.append(stream.mime_type)
					fileAudio.append(stream.audio_codec)
					audio.append(stream)
     
				i = 1
				for extension in fileExtension:
					print(f'{i}- Extension: {extension} -> Audio: {fileAudio[i-1]}')
					i += 1

				# To Download the video with the users Choice of resolution
				strm = int(input('\nChoose a resolution please: '))
				
				if 1 <= strm < i:
					try:
						# To validate if the user enters a number displayed on the screen...
							extension_to_download = fileExtension[strm-1]
							print(f"You're now downloading the audio with extension {extension_to_download}...")

							# command for downloading the video
							audio[strm-1].download(locate)
					except:
						print("Some Error, download not completed !")
					else:
						print("\nDownloaded successfully !")
						break
				else:
					print("Invalid choice !!\n\n")

			elif format == 2:
				dwn = yt.streams.filter(type="video", progressive="True", file_extension='mp4')
				print("\n1- Highest resolution\n2- Lowest resolution\n3- See all available")
				res = int(input("Choose resolution: "))
				print()
    
				if res == 1:
					try:
						print(f"Downloading {yt.title} {dwn.get_highest_resolution().resolution}")
						dwn.get_highest_resolution().download(locate)
					except:
						print(f"Error while downloading the video !")
					else:
						print("\nDownload success !!")
						break
				elif res == 2:
					try:
						print(f"Downloading {yt.title} {dwn.get_lowest_resolution().resolution}")
						dwn.get_lowest_resolution().download(locate)
					except:
						print(f"Error while downloading the video !")
					else:
						print("\nDownload success !!")
						break

				elif res == 3:
        
					video_resolutions = []
					fileExtension = []
					videos = []
		
					for stream in yt.streams.order_by('resolution').filter(progressive="True"):
						video_resolutions.append(stream.resolution)
						fileExtension.append(stream.mime_type)
						videos.append(stream)
		
					i = 1
					for resolution in video_resolutions:
						print(f'{i}- {resolution} -> Extension: {fileExtension[i-1]}')
						i += 1

					# To Download the video with the users Choice of resolution
					strm = int(input('\nChoose a resolution please: '))
					
					if 1 <= strm < i:
						try:
							# To validate if the user enters a number displayed on the screen...
								resolution_to_download = video_resolutions[strm-1]
								print(f"You're now downloading the video with resolution {resolution_to_download}...")

								# command for downloading the video
								videos[strm-1].download(locate)
						except:
							print("Some Error, download not completed !")
						else:
							print("\nDownloaded successfully !")
							break
					else:
						print("Invalid choice !!\n\n")
 
				else:
					print("Error ! Enter a valid number !!")
					break
    
			elif format == 3:
    
				file_resolutions = []
				fileExtension = []
				fileAudio = []
				files = []
     
				for stream in yt.streams.order_by('mime_type'):
					file_resolutions.append(stream.resolution)
					fileExtension.append(stream.mime_type)
					fileAudio.append(stream.audio_codec)
					files.append(stream)
     
				i = 1
				for resolution in file_resolutions:
					print(f'{i}- {resolution} -> Extension: {fileExtension[i-1]} -> Audio: {fileAudio[i-1]}')
					i += 1

				# To Download the file with the users Choice of resolution
				strm = int(input('\nChoose a resolution please: '))
				
				if 1 <= strm < i:
					try:
							print(f"You're now downloading {yt.title}...")
							# command for downloading the file
							files[strm-1].download(locate)
					except:
						print("Some Error, download not completed !")
					else:
						print("\nDownloaded successfully !")
						break
				else:
					print("Invalid choice !!\n\n")
			else:
				print("Choose a valid number !!")

def PlaylistDownload():
    # link of the video to be downloaded
	link=input("Enter the playlist link: ")

	#where to save
	locate=input("\nWhere to save it ? ")

	try:
		# object creation using YouTube
		# which was imported in the beginning
		pylst = Playlist(link)
	except exceptions.VideoPrivate:
		print("Video is private !") #to handle exception
	except exceptions.VideoRegionBlocked:
		print("Video is blocked !")
	except exceptions.VideoUnavailable:
		print("Video is not available !")
	else:
		try:
			# downloading the playlist
			print(f"Downloading {pylst.title}")
			for video in pylst.videos:
				video.streams.first().download(locate)
		except:
			print("Some Error, download not completed !")
		else:
			print("Downloaded successfully !")

def Research():
    search_query = input("Enter what you are searching for: ")
    
    s = Search(search_query)
    print(f"\n{len(s.results)} results founded\n")
    for i in s.results:
        print(i)
    
    print(f"\n{len(s.completion_suggestions)} suggestions founded\n")
    for i in s.completion_suggestions:
        print(i)

print("Welcome !!\n\n1- Single/Multiple youtube download\n2- Playlist download\n3- Research\n")
choosed = int(input("Enter the desired action: "))

if choosed == 1:
    SingleDownload()
elif choosed == 2:
    PlaylistDownload()
elif choosed == 3:
    Research()
else:
    print("Error !! Enter a valid number !!")