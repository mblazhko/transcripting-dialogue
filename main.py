from scripts import (
    get_data_from_api,
    count_block_duration,
    split_dialogue,
    dialogues_to_webvtt,
)
import datetime


def make_subtitles(wpm: int, max_length: int) -> str:
    data = get_data_from_api()
    blocks = split_dialogue(data[0]["content"], max_length)
    current_time = datetime.datetime.strptime(
        data[0]["date"], "%Y-%m-%d %H:%M:%S"
    )
    timings = []
    for block in blocks:
        duration = count_block_duration(wpm=wpm, text=block)
        start_time = current_time
        end_time = start_time + datetime.timedelta(seconds=duration)
        timings.append(
            (start_time.strftime("%H:%M:%S"), end_time.strftime("%H:%M:%S"))
        )
        current_time = end_time

    return dialogues_to_webvtt(dialogues=blocks, timings=timings)


if __name__ == "__main__":
    subtitles = make_subtitles(wpm=60, max_length=800)
    with open("subtitles.vtt", "w") as file:
        file.write(subtitles)
