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
    final, original_files = query_maker(link)

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
            model = "openai/gpt-oss-120b"
        )

        answers.append(chat_completion.choices[0].message.content)

    tmp = []
    for batch in answers:
        songs = batch.split('\n')
        tmp.append(songs)

    tmp = list(itertools.chain.from_iterable(tmp))

    # name formatting of songs in downloads folder
    downloaded_songs = original_files
    print("Original files:", downloaded_songs)
    
    # clean up tmp (remove empty lines)
    tmp = [t.strip() for t in tmp if t.strip()]
    
    rename_count = min(len(tmp), len(downloaded_songs))
    final_names = []
    
    for i in range(rename_count):
        old_path = f"downloads/{downloaded_songs[i]}"
        # Ensure new name is a valid filename
        safe_new_name = tmp[i].replace("/", "-").replace("\\", "-").replace(":", "-").replace('"', "").replace("*", "").replace("?", "").replace("<", "").replace(">", "").replace("|", "")
        new_path = f"downloads/{safe_new_name}.mp3"
        print(f"Renaming {old_path} to {new_path}")
        try:
            os.rename(old_path, new_path)
            final_names.append(safe_new_name)
        except Exception as e:
            print(f"Error renaming {old_path}: {e}")
            final_names.append(downloaded_songs[i].replace(".mp3", ""))

    return final_names
