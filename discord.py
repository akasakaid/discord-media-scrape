import os
import time
import json
import requests
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()


def get_content(url: str, filename: str, output: str):
    if not os.path.exists(output):
        os.makedirs(output)
    res = requests.get(url, stream=True)
    content_length = int(res.headers.get("Content-Length", 0))
    start = 1
    while True:
        print(f"    Output name : {filename} ", flush=True, end="\r")
        if os.path.exists(f"{output}/{filename}"):
            size = os.path.getsize(f"{output}/{filename}")
            if size == content_length:
                print(f"    Content {filename} already exists")
                return
            _path = Path(f"{output}/{filename}")
            basename = _path.stem
            split_name = basename.split("_")
            if len(split_name) == 2:
                if split_name[-1].isdigit():
                    filename = split_name[0] + "_" + str(start) + _path.suffix
            elif len(split_name) > 2:
                if split_name[-1].isdigit():
                    split_name.remove(split_name[-1])
                temp_name = "_".join(split_name)
                filename = temp_name + "_" + str(start) + _path.suffix
            else:
                filename = basename + "_" + str(start) + _path.suffix
            start += 1
            continue
        break
    print(f"    Output name : {filename}    ")
    current_length = 0
    with open(f"{output}/{filename}", "wb") as write:
        try:
            for chunk in res.iter_content(chunk_size=1024):
                write.write(chunk)
                percent = round(current_length / content_length * 100)
                print(f"    Downloading {filename} {percent}% ", flush=True, end="\r")
                current_length += len(chunk)
            print(f"    Downloading {filename} Complete !    ")
        except Exception as e:
            print("url", url)
            print(e)


def main():
    global output
    banner = """
--------------------------------------
    > Discord Media Scraper
    > @AkasakaID
--------------------------------------    
    """
    os.system("cls" if os.name == "nt" else "clear")
    print(banner)
    output = input("input channel id : ")
    url = f"https://discord.com/api/v9/channels/{output}/messages"
    params = {"limit": 50}
    headers = {
        "Authorization": os.getenv("DISCORD_AUTHORIZATION"),
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
    }
    params = {"limit": 50}
    while True:
        result = requests.get(url, headers=headers, params=params)
        if len(result.json()) == 0:
            break
        for no, content in enumerate(result.json()):
            print("~" * 50)
            msg_id = content.get("id", 0)
            msg_date = content.get("timestamp")
            print(f"message id : {msg_id}")
            print(f"message date : {msg_date}")
            if (no + 1) == len(result.json()):
                params["before"] = msg_id
            if msg_id in open("already_dump.txt").read().splitlines():
                print("message id content already download !")
                continue
            for attachment in content.get("attachments"):
                media_url = attachment.get("url")
                filename = attachment.get("filename")
                print(f"    get media : {msg_id}")
                get_content(media_url, filename, output)
            open("already_dump.txt", "a").write(f"{msg_id}\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit()
