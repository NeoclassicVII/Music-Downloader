# Music Downloader by Neoclassic VII for Metalheads!
# Enjoy!

import time
import os
import sys
import webbrowser
import requests
import difflib
import youtube_dl
import colorama
import pyfiglet
from colorama import Fore
from youtubesearchpython import VideosSearch
from bs4 import BeautifulSoup

colorama.init()

def main():
  # Song Downloader 
  def songDownloader():
    ydl_opts = {
      'format':'bestaudio/best',
      'keepvideo':False,
      'outtmpl': os.environ['USERPROFILE'] + '\\Music\\' + filename
      }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
      ydl.download([link])
      print()
      print(Fore.GREEN + "[+] " + Fore.WHITE + "Song successfully downloaded!")
      time.sleep(1.2)
      print()
      startagain = print(Fore.YELLOW + "Click ENTER to start again!" + Fore.WHITE, end="")
      again = input()
      main()

  # LastFM URL's
  LASTFM_URL = "https://www.last.fm"
  searchURL = "https://www.last.fm/search?q="

  # Genres (Tags) [HERE YOU CAN ADD YOUR OWN TAGS/GENRES]
  genres = [
  "deathcore","power metal","heavy metal","death metal","black metal","thrash metal","alternative metal","nu metal","folk black metal",
  "trve kvlt","symphonic black metal","ambient black metal","technical deathcore","blackened technical death metal","norwegian black metal","brutal death metal",
  "neoclassical death metal","neoclassical metal","electronicore","doom metal","gothic metal","djent","glam metal","metalcore","groove metal","progressive metal",
  "prog metal","avant garde metal","folk metal","grindcore","melodic black metal","cyber metal","melodic death metal","mathcore","white metal","industrial metal",
  "symphonic deathcore","melodic deathcore","slamming deathcore","beatdown deathcore","slamming beatdown deathcore","magical death metal",
  "neoclassical deathcore","pornogore","folk deathcore","folk death metal","slamming brutal death metal","powerviolence","crossover","shitgrind",
  "pirate metal","kawaii metal","drone metal","drone","math metal","neue deutsche härte","ndh","technical death metal","black death metal","metal",
  "blackened deathcore"
  ]

  time.sleep(0.7)
  os.system("cls")
  print(Fore.MAGENTA + pyfiglet.figlet_format("Music Downloader") + Fore.WHITE)
  time.sleep(0.4)
  print()
  time.sleep(0.6)
  print("[" + Fore.BLUE + "!" + Fore.WHITE + "] " + Fore.YELLOW + "Type the name of the band" + Fore.RED + " and " + Fore.YELLOW + "the song fully and correctly!" + Fore.WHITE)
  print()
  time.sleep(1.7)
  print(Fore.YELLOW + "[EXAMPLE]" + Fore.WHITE)
  print("- Lorna Shore Death Portrait")
  time.sleep(1.1)
  print()
  songSearch = print(Fore.CYAN + "- Which song? " + Fore.WHITE, end="")

  # The song
  song = input()
  print()

  # Finds the song in LastFM
  try:
    source = requests.get(searchURL+song).text
  except (requests.ConnectionError, requests.Timeout) as exception:
    time.sleep(0.7)
    nl()
    print(Fore.RED + "[-] No Internet Connection!")
    print(Fore.WHITE)
    time.sleep(1.7)
    main()

  soup = BeautifulSoup(source, "lxml")
  findSongList = soup.find("tbody")

  if findSongList == None:
    time.sleep(0.7)
    print(Fore.RED + "[-]" + Fore.WHITE + " No song found! ")
    time.sleep(1.2)
    os.system("cls")
    main()

  findSong = findSongList.find("tr")
  findUrl = findSong.find("td", class_="chartlist-name").a

  # The song URL (If it did find one)
  songURL = findUrl ["href"]

  # Checks the genre of song
  genreRequest = requests.get(LASTFM_URL+songURL).text
  soupCheck = BeautifulSoup(genreRequest, "lxml")
  findTag = soupCheck.find("section", class_="catalogue-tags").ul

  if findTag == None:
    time.sleep(0.7)
    print()
    print(Fore.RED + "[-] No song found!" + Fore.WHITE)
    time.sleep(1.1)
    main()

  tags = findTag.find_all("li", class_="tag")

  for tag in tags:
    if tag.text in genres:
      def youtubeFinder(song):
        os.system("cls")
        time.sleep(0.4)
        print(Fore.RED + pyfiglet.figlet_format("Choose the song"))
        search = VideosSearch(song, limit = 6).result()

        for results in range(6):
          songTitle = search ['result'][results]['title']
          print(Fore.BLUE + "[","{}".format(results),"] " + Fore.YELLOW,songTitle)

        print()
        choose = print(Fore.GREEN + "Choose the one, that you want to download: " + Fore.WHITE, end="")
        thechoice = input()

        if thechoice <= str(6):
          try:
            global link,filename
            link = search ['result'][int(thechoice)]['link']
            filename = f"{search ['result'][int(thechoice)]['title']}.mp3"
            print()
          except ValueError:
            print()
            time.sleep(0.6)
            print(Fore.RED + "Choose the right one!" + Fore.WHITE)
            time.sleep(0.8)
            youtubeFinder(song)
        else:
          print()
          time.sleep(0.6)
          print(Fore.RED + "Choose the right one!" + Fore.WHITE)
          time.sleep(0.8)
          youtubeFinder(song)

      youtubeFinder(song)

      # Downloads the song
      songDownloader()

  # If not supported genre (if not metal)
  if tags[-1].text not in genres:
    time.sleep(0.7)
    print()
    print(Fore.RED + "[-] No song found!" + Fore.WHITE)
    time.sleep(1.1)
    main()

try:
  main()
except KeyboardInterrupt:
  sys.exit()
