from youtubesearchpython import VideosSearch  # library used to search youtube
from pytube import YouTube # used to download the videos
from pytube.cli import on_progress # to show the download progress
import os # to remove and rename files

filename = 'downloads.txt'
videoNum = 0


def searchYoutube(videoName):
    try:
        # Search Youtube by the video name and extracting the link of the first video
        videoLink = VideosSearch(videoName, limit=1).result()["result"][0]["link"] 
        return videoLink
    except:
        print("Error, Cannot search for the video.")
        return False

def getResolution(youtubeObject):
    video_resolutions = []
    # getting all the resolutions of the video
    for stream in youtubeObject.streams.order_by('resolution'):
        video_resolutions.append(stream.resolution)
    # Remove any duplicates in the list
    video_resolutions = list(set(video_resolutions))
    video_resolutions = [sub.replace('p', '') for sub in video_resolutions]
    video_resolutions = sorted(video_resolutions, key=int)
    video_resolutions = [sub + 'p' for sub in video_resolutions]

    while True:
        print("Choose the resolution you want to download: ")
        for i in range(1, len(video_resolutions) + 1):
            print(i, '-', video_resolutions[i - 1])
        choice = int(input("Your choice: "))
        if choice > 0 and choice <= len(video_resolutions):
            return video_resolutions[choice - 1]
        print("Please enter a valid choice!")


def Download(link, videoNum):
    youtubeObject = YouTube(link, on_progress_callback=on_progress)
    resolution = getResolution(youtubeObject)

    try:
        if youtubeObject.streams.filter(res=resolution, progressive=True).first() != None: # if the file is progressive (have both audio and video in one file)
            print("Downloading Your video")
            download = youtubeObject.download()
            fileName = "Video" + str(videoNum) + ".mp4"
            os.rename(download, fileName)

        else: # the file have separate audio and video
            print("Downloading your video")
            videoFile = youtubeObject.streams.filter(res=resolution).first().download() # download the video file
            os.rename(videoFile, 'video.mp4') # rename video file
            soundFile = youtubeObject.streams.filter(only_audio=True).first().download() # download audio file
            os.rename(soundFile, 'audio.mp3') # rename audio file
            
            os.system('cmd /c "ffmpeg -i video.mp4 -i audio.mp3 -c copy output.mp4"') # combining audio with video file using ffmpeg in command 
            os.remove('video.mp4') # delete video file
            os.remove('audio.mp3') # delete audio

            fileName = "Video" + str(videoNum) + ".mp4"
            os.rename("output.mp4", fileName)
        with open(filename, 'a') as f:
            if os.path.getsize(filename) > 0:
                f.write('\n')
            f.write(youtubeObject.streams[0].title) # adding video title to text file
        print("Download is completed successfully")
    except:
        print("An error has occurred, please try again later")


def main():
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            downloads = file.read()
        downloads = downloads.split('\n')
        videoNum = len(downloads) + 1
    else:
        videoNum = 1
    while True:
        choice = input('1- View previous downloads.\n2- Download new video.\n3- Exit.\nChoice: ')
        if choice == '1':
            if os.path.exists(filename):
                with open(filename, 'r') as file:
                    downloads = file.read()
                downloads = downloads.split('\n')
                print('\nPrevious downloads:')
                for i in range(1, len(downloads) + 1):
                    print(i, '-', downloads[i - 1])
                print('')
            else:
                print("No previous downloaded videos")
        elif choice == '2':
            videoName = input("Please enter video name: ")
            link = searchYoutube(videoName)
            if link != False:
                Download(link, videoNum)
                videoNum += 1
        elif choice == '3':
            print('GoodBye...')
            exit()
        else:
            print('Please enter a valid choice!')

main()