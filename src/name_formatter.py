from groq import Groq
from dotenv import load_dotenv
from query_maker import query_maker
import os
import itertools

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
print(api_key)
client = Groq(api_key = api_key)

setting = """
given is a list of songs title, and your vast knowledge of songs, format the songs titles in the strict
title as follows:
'<lead singer's name> - <song name> - <featuring artist name (if any)>'
if you have any doubt in the name of the song, then DO NOT FORMAT IT.
always keep the whole name of the song and main artist.
the output should not contain any other text, just the formatted song names in separate lines
keep the results baised towards rap in case you have any confusions.
the output must contain as many songs names as the input
the maximum length for a song name should be strictly limited to 44 characters
"""

def name_formatter(link):
    answers = []
    final = query_maker(link)

    for batch in final:
        chat_completion = client.chat.completions.create(
            messages = [
                {
                    "role" : "system",
                    "content" : "you are highly knowledgable in music, and provide highly structured outputs, keep the outputs baised towards rap"
                },
                {
                    "role" : "user",
                    "content" : f"{setting}\n{batch}"
                }
            ],
            model = "llama-3.3-70b-versatile"
        )

        answers.append(chat_completion.choices[0].message.content)

    tmp = []
    for batch in answers:
        songs = batch.split('\n')
        tmp.append(songs)

    tmp = list(itertools.chain.from_iterable(tmp))

    # name formatting of songs in downloads folder not working
    downloaded_songs = os.listdir(f"downloads/")
    print(downloaded_songs)
    for i in range(len(tmp)):
        print(downloaded_songs[i])
        print(tmp[i])
        print()
        os.rename(f"downloads/{downloaded_songs[i]}", f"downloads/{tmp[i]}.mp3")

    return tmp
