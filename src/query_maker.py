import os
from downloader import download_playlist

def query_maker(link):
    download_playlist(link)
    
    batches = []
    batch = []
    count = 0

    original_files = sorted(os.listdir("downloads"))
    for file in original_files:
        batch.append(file)
        count += 1
        if count == 5:
            batches.append(batch)
            batch = []
            count = 0

    if (len(batch) != 0):
        batches.append(batch)

    tmp = ""
    count = 1
    final = []
    for batch in batches:
        for string in batch:
            tmp += f"{count}. {string}\n"
            count += 1
        final.append(tmp)
        tmp = ""
        count = 1

    return final, original_files


