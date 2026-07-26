from groq import Groq
from dotenv import load_dotenv
from query_maker import query_maker
import os

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
print(api_key)
client = Groq(api_key = api_key)

setting = """
given is a list of songs title, and your vast knowledge of songs, format the songs titles in the strict
title as follows:
'<lead singer's name> - <song name> - <featuring artist name (if any)>'
the output should not contain any other text, just the formatted song names in separate lines
keep the results baised towards rap in case you have any confusions
"""

def name_formatter():
    answers = []
    final = query_maker()

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


    for ans in answers:
        print(ans)


name_formatter()