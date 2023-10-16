
import os
import random
from mido import MidiFile, MidiTrack, Message
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Set MIDI folder path
midi_folder = "/Users/mac/git/privateGPT/gpt2music"

def analyze_sentiment(text):
    """
    Analyze the sentiment of the given text.
    Returns the sentiment score.
    """
    # Initialize VADER sentiment analyzer
    nltk.download('vader_lexicon')
    sid = SentimentIntensityAnalyzer()

    # Calculate sentiment score
    sentiment_scores = sid.polarity_scores(text)
    return sentiment_scores['compound']

def select_folder(base_folder, sentiment):
    """
    Select major or minor folder based on the sentiment of the given text.
    Returns the path of the selected folder.
    """
    # Select major or minor folder
    folder = "Major" if sentiment >= 0 else "Minor"
    for subfolder in os.listdir(base_folder):
        if folder in subfolder:
            return os.path.join(base_folder, subfolder)

def select_chord_progression_folder(base_folder):
    """
    Select chord progression folder randomly.
    Returns the path of the selected chord progression folder.
    """
    # Select chord progression randomly
    folders = [f for f in os.listdir(base_folder) if os.path.isdir(os.path.join(base_folder, f))]
    selected_folder = random.choice(folders)
    return os.path.join(base_folder, selected_folder)

def process_text(text):
    # Create MIDI file
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)

    # Split text into sentences
    sentences = text.split(".")

    # Process each sentence
    for sentence in sentences:
        # Split sentence into words
        words = sentence.split()

        # Process each word
        for word in words:
            # Check if word is capitalized
            if word.istitle():
                # Enter 4 Progressions folder
                base_folder = os.path.join(midi_folder, "4 Progressions")
            else:
                # Enter random key folder (1st step)
                key_folders = [f for f in os.listdir(midi_folder) if os.path.isdir(os.path.join(midi_folder, f))]
                key_folder = random.choice(key_folders)
                base_folder = os.path.join(midi_folder, key_folder)

                # Enter random chord progression folder (2nd step)
                base_folder = select_chord_progression_folder(base_folder)

                # Check sentiment of word
                sentiment_score = analyze_sentiment(word)

                # Enter major or minor folder (3rd step)
                base_folder = select_folder(base_folder, sentiment_score)

            print(f"Selected folder for '{word}': {base_folder}")

            # Check length of word
            if len(word) > 3:
                duration = 160  # triple 16th note
            elif len(word) > 2:
                duration = 240  # 16th note
            elif len(word) < 2:
                duration = 480  # 8th note
            else:
                duration = 120

            # Play MIDI chords for each character in word
            for char in word:
                note = ord(char) % 12 + 60  # map character to MIDI note number
                track.append(Message('note_on', note=note, velocity=64, time=0))                
                track.append(Message('note_off', note=note, velocity=64, time=duration))

        # Check if sentence ends with punctuation
        if not sentence.endswith((".", ",", "?")):
            # Add pause to MIDI track
            track.append(Message('note_off', note=0, velocity=0, time=960))  # half note pause

        break  # only process first sentence

    # Save MIDI file
    mid.save('output.mid')

process_text("I love you, I hate you.")
