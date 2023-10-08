import httpx
import json
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('API_KEY')
SYMBOL = os.getenv('SYMBOL')
YEAR = os.getenv('YEAR')
QUARTER = os.getenv('QUARTER')

URL = f"https://financialmodelingprep.com/api/v3/earning_call_transcript/{SYMBOL}?year={YEAR}&quarter={3}&apikey={API_KEY}"


# get data from api and save it as json
def get_data_from_api() -> dict:
    with httpx.Client() as client:
        response = client.get(url=URL)

    with open("data.json", "w") as file:
        data = response.json()
        json.dump(data, file)

    return response.json()


# count text duration by word per second
def count_block_duration(wpm: int, text: str) -> float:
    words = len(text.split())
    duration = (words / wpm) * 60

    return duration


# get speaker name from text block
def extract_speaker_name(dialogue) -> str | None:
    lines = dialogue.split('\n')
    speaker_name = None

    for line in lines:
        if ":" in line:
            speaker_name, _ = line.split(":", 1)
            break

    return speaker_name


def split_block(block: str, max_length: int) -> list[str]:
    blocks = []
    current_block = ""
    name = extract_speaker_name(dialogue=block)

    for char in block:
        current_block += char

        if len(current_block) >= max_length and char == ".":
            blocks.append(current_block.strip())
            current_block = f"{name}:"

    if current_block and len(current_block) > 15:
        blocks.append(current_block.strip())

    return blocks



# divide text on blocks by symbols count
def split_dialogue(dialogue: str, max_length: int) -> list[str]:
    splitted_dialogue = dialogue.split("\n")
    blocks = []

    for block in splitted_dialogue:
        blocks.extend(split_block(block, max_length))

    return blocks


def dialogues_to_webvtt(dialogues, timings) -> str:
    webvtt_content = "\n"

    for i, (start_time, end_time) in enumerate(timings):
        dialogue_text = dialogues[i]
        webvtt_content += f"{i+1}\n{start_time} --> {end_time}\n{dialogue_text}\n\n"

    return webvtt_content
