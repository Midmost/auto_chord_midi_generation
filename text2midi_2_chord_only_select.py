
import os
import random
from mido import MidiFile, MidiTrack, Message
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Set MIDI folder path
midi_folder = "/Users/mac/git/privateGPT/gpt2music/Unison MIDI Chord Pack/01 - C Major - A Minor"

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

            # Select random MIDI file from selected folder
            midi_files = [f for f in os.listdir(base_folder) if f.endswith(".mid")]
            selected_midi_file = random.choice(midi_files)
            selected_midi_path = os.path.join(base_folder, selected_midi_file)

            print(f"Selected MIDI file: {selected_midi_path}")

            # Read and play selected MIDI file
            selected_mid = MidiFile(selected_midi_path)
            for msg in selected_mid.play():
                track.append(msg)

        break  # only process first sentence

    # Save MIDI file
    mid.save('output.mid')

process_text("You are a monster, why you always hit me? But still I love you so much")
