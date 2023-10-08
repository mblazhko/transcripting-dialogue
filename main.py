import httpx
import json

API_KEY = "7e4eb134c8b3a36fa4e52de23f5f1c33"
SYMBOL = "AAPL"
YEAR = "2023"
QUARTER = "3"

URL = f"https://financialmodelingprep.com/api/v3/earning_call_transcript/{SYMBOL}?year={YEAR}&quarter={3}&apikey={API_KEY}"


# get data from api and save it as json
def get_data_from_api():
    with httpx.Client() as client:
        response = client.get(url=URL)

    with open("data.json", "w") as file:
        data = response.json()
        json.dump(data, file)

    return response.json()


# count text duration by word per second
def count_block_duration(wps: int, text: str) -> float:
    splited_text = text.split()
    duration = len(splited_text) / wps

    return duration


# divide text on blocks by symbols count
def split_dialogue(dialogue: str, max_length: int) -> list[str]:
    block = ""
    blocks = []
    for char in dialogue:
        block += char
        if len(block) >= max_length and char == ".":
            blocks.append(block)
            block = ""
    if block:
        blocks.append(block)

    return blocks


def dialogues_to_webvtt(dialogues, timings):
    webvtt_content = "WEBVTT\n\n"

    for i, (start_time, end_time) in enumerate(timings):
        dialogue_text = dialogues[i]
        webvtt_content += f"{start_time} --> {end_time}\n{dialogue_text}\n\n"

    return webvtt_content

if __name__ == '__main__':
    pass

