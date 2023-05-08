import math
import openai
import numpy as np
import whisper
from datetime import datetime
from utils import saveTextAsCsv, calculateValuesForFile, drawAndSaveDiagram
from moviepy.editor import VideoFileClip

def debug(text):
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    print(str(formatted_datetime) + ': ' +str(text))

debug('mp4 to mp3...')
video_clip = VideoFileClip('meeting.mp4')
video_clip.audio.write_audiofile('meeting.mp3', codec='mp3')

debug('video to text....')
model = whisper.load_model("small")
output = model.transcribe('meeting.mp3', fp16=False, language='pl')
text = output['text']
debug('video to text finished')

timestamp = str(datetime.timestamp(datetime.now()))
debug(timestamp)

with open("fullText" +  timestamp + ".txt", "w") as file:
    # Write the text to the file
    file.write(text)

debug('text as csv...')
saveTextAsCsv(text, timestamp)

debug('values for file...')
calculateValuesForFile(timestamp)

debug('drawing diagram')
drawAndSaveDiagram(timestamp)

try:
    # https://colab.research.google.com/drive/15tr9FMCDuSO5Dahw8XMEkk2-p4CoR17s?usp=sharing
    debug('getting video description...')

    openai.api_key = 'sk-'
    words = text.split(" ")
    debug(math.ceil(len(words)/2000))
    chunks = np.array_split(words, math.ceil(len(words)/2000))
    sentences = ' '.join(list(chunks[0]))

    summary_responses = []

    for chunk in chunks:
        sentences = ' '.join(list(chunk))
        prompt = f"{sentences}\n\ntl;dr:"

        response = openai.Completion.create(
            engine="text-davinci-003", 
            prompt=prompt,
            temperature=0.3, # The temperature controls the randomness of the response, represented as a range from 0 to 1. A lower value of temperature means the API will respond with the first thing that the model sees; a higher value means the model evaluates possible responses that could fit into the context before spitting out the result.
            max_tokens=150,
            top_p=1, # Top P controls how many random results the model should consider for completion, as suggested by the temperature dial, thus determining the scope of randomness. Top P’s range is from 0 to 1. A lower value limits creativity, while a higher value expands its horizons.
            frequency_penalty=0,
            presence_penalty=1
        )

        response_text = response["choices"][0]["text"]
        summary_responses.append(response_text)

        full_summary = "".join(summary_responses)

        with open("summary" + timestamp + ".txt", "w") as file:
            # Write the text to the file
            file.write(full_summary)

except Exception as e:
    debug(e)

debug('finished..')