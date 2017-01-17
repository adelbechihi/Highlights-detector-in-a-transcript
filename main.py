from os import path
from elasticsearchClient import elasticsearch_store
import matplotlib.pyplot as plt
import numpy as np
from functions import *


# choose any youtube podcast
# convert the video in a .wav file
# put it in the same folder as this script
# rename it "test.wav"
# run the script

FILE_NAME = "python.wav"

# obtain path to the audio file in the same folder as this script
AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), FILE_NAME)

# convert the audio into a text
text, duration = speech_to_text(AUDIO_FILE)

# store the text in an elasticsearch index
# uncomment the next line to store the transcript on the elastic search index
# run bin/elasticsearch

# elasticsearch_store("my-index", text)


# find keywords in the text
count = detect_keywords(text)
print("The keywords occurrence:")
print(*count,  sep='\n')

# visualize keywords occurrence and position in the text
X = get_words_weight(text, count)

# get highlights in the text
nb_highlights, highlights, highlights_start, highlights_end = get_highlights(X)

# get time in seconds
# hypothesis: duration is proportional to the number of words
time_sec = np.multiply(np.round(duration/len(X), 2), range(len(X)))
highlights_start_sec = np.multiply(np.round(duration/len(X), 2), highlights_start)
highlights_end_sec = np.multiply(np.round(duration/len(X), 2), highlights_end)


# visualize results
print("The highlights number is %d" % nb_highlights)
for i in range(len(highlights_start_sec)):
    print("{}- starts at: {}s, ends at: {}s".format((i+1), highlights_start_sec[i], highlights_end_sec[i]))


f, ax = plt.subplots(2, sharex=True)
ax[0].bar(time_sec, X, 0.5, color='b', edgecolor="none")
ax[0].set_title('Words weight in the transcript')
ax[0].set_xlabel('Time in sec')
ax[0].set_ylabel('Word occurrence')
ax[1].bar(time_sec, X, 0.5, color='b', edgecolor="none")
ax[1].bar(time_sec, highlights, 0.5, color='r', edgecolor="none")
ax[1].set_title('Highlights in the transcript')
ax[1].set_xlabel('Time in sec')
ax[1].set_ylabel('Word occurrence')

plt.show()
