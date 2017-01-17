import speech_recognition as sr
from collections import Counter
from nltk.corpus import stopwords
import numpy as np


def speech_to_text(audio_file):
    # recognize speech using Sphinx
    r = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        duration = source.DURATION // 1
        audio = r.record(source)  # read the entire audio file
    try:
        return r.recognize_sphinx(audio), duration
    except sr.UnknownValueError:
        print("Sphinx could not understand audio")
    except sr.RequestError as e:
        print("Sphinx error; {0}".format(e))


def detect_keywords(text):
    # delete the stop words in the text
    s = set(stopwords.words('english'))
    words = list(filter(lambda w: w not in s, text.split()))
    # find the 20 most common words
    return Counter(words).most_common(20)


def get_words_weight(text, count):
    # put keywords in a list
    keywords = []
    for i in range(len(count)):
        keywords.append(count[i][0])

    # get keywords position in the text
    tokens = text.split()  # split on whitespace
    words_weight = np.zeros(len(tokens))
    for i in range(len(tokens)):
        if tokens[i] in keywords:
            words_weight[i] = count[keywords.index(tokens[i])][1]

    return words_weight


def get_highlights(x):
    threshold = 4 * max(x)
    window_weight = len(x) // 20

    score = 0
    highlights_moments = []
    highlights_start = []
    highlights_end = []
    highlights_duration = np.zeros(len(x))

    # get the highlights moments in the transcript by calculating
    # the score of the keywords in window_weight duration
    for i in range(len(x) - window_weight):
        for j in range(window_weight):
            score += x[i + j]

        if score > threshold:
            highlights_moments.append(i)

        score = 0

    # get the highlights in duration
    highlights = np.zeros(len(x))
    counter = 0
    while counter < len(x):
        if counter in highlights_moments:
            for j in range(window_weight):
                highlights[counter + j] = x[counter + j]
                highlights_duration[counter + j] = 1
            counter += window_weight
        counter += 1

    # get the highlights start and end time
    for i in range(len(highlights_duration) - 1):
        if (highlights_duration[i + 1] != 0) & (highlights_duration[i] == 0):
            highlights_start.append(i + 1)
        if (highlights_duration[i] != 0) & (highlights_duration[i + 1] == 0):
            highlights_end.append(i)

    if len(highlights_start) > len(highlights_end):
        highlights_end.append(len(x))
    if len(highlights_start) < len(highlights_end):
        highlights_start.insert(1, 1)

    # get the highlights number in the transcript
    nb_highlights = len(highlights_start)

    return nb_highlights, highlights, highlights_start, highlights_end
