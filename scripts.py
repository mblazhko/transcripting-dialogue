import httpx
import json
import os
from dotenv import load_dotenv

load_dotenv()


# get data from api and save it as json
def get_data_from_api(
        symbol: str = input("Enter symbol of the data you want to have: "),
        year: int = input("Enter the year of the data you want to have: "),
        quarter: int = input(
            "Enter the quarter of the data you want to have: ")
) -> dict:
    api_key = os.getenv('API_KEY')
    url = ("https://financialmodelingprep.com/api/v3/earning_call_transcript/"
           f"{symbol}?year={year}&quarter={quarter}&apikey={api_key}"
           )
    try:
        with httpx.Client() as client:
            response = client.get(url=url)
        response.raise_for_status()
    except httpx.HTTPError as e:
        print(f"HTTPError: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

    with open("data.json", "w") as file:
        data = response.json()
        if not data:
            print("\nThere is no data on your request. Try another request."
                  "\nExit..."
                  )
            exit()
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
        webvtt_content += f"{i + 1}\n{start_time} --> {end_time}\n{dialogue_text}\n\n"

    print(
        "\nThe subtitle file has been successfully created and saved to root")
    return webvtt_content
