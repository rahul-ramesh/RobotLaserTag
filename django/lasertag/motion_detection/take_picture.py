import os
import process.py

def main():
	os.system("streamer -c /dev/video1 -f jpeg -o image.jpeg")
	analyze()


main()
