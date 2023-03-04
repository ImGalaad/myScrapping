from pytube import Playlist
import os
import string
import re
from pydub import AudioSegment


def remove_parentheses(string):
    result = ""
    in_parentheses = False
    for char in string:
        if char == "(":
            in_parentheses = True
        elif char == ")":
            in_parentheses = False
        elif not in_parentheses:
            result += char
    return result


def remove_useless_spaces(string):
    if string[0] == " ":
        string = string[1:]
    if string[-1] == " ":
        string = string[:-1]
    return string


def get_song_info(title, description):

    for separator in ["-", "–", "~", ","]:
        if separator in title:
            singer_title = title.split(separator)
            title_ = singer_title[1]
            singer_ = singer_title[0]

            return {
                "title": remove_useless_spaces(remove_parentheses(title_)),
                "singer": singer_,
            }

    else:
        title_ = re.search(r"^(.*?)\s·", description, re.MULTILINE)
        singer_ = re.search(r"·\s(.*?)\s", description, re.MULTILINE)

        if title_ is None or singer_ is None:
            return f"Description and title error in the song {title}"

        else:
            title_ = title_.group(1)
            singer_ = singer_.group(1)
            return {
                "title": remove_useless_spaces(remove_parentheses(title_)),
                "singer": singer_,
            }


if not os.path.exists("music"):
    os.makedirs("music")

__url__ = ""
playlist = Playlist(__url__)


for song in playlist.videos:
    description = song.description
    title = song.title
    data = get_song_info(title, description)
    if isinstance(data, dict):
        filename = data["title"] + ".mp4"
        song.streams.filter(only_audio=True).first().download(
            "music", filename=filename
        )

        audio = AudioSegment.from_file("music/" + filename, format="mp4")
        audio.export(f"music/{data['title']}.mp3", format="mp3")
        os.remove("music/" + filename)

    else:
        print(data)
