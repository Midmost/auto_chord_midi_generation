

#beats_per_measure = 32
##note_values_mapping = {
##    't': 0.6667,  # Tuplet (2/3 times the base duration)
##    'e': 0.5,     # Eighth note (0.5 beat)
##    's': 0.25,    # Sixteenth note (0.25 beat)
##    'q': 1,       # Quarter note (1 beat)
##    'dq': 1.5,    # Dotted quarter note (1.5 beats)
##    'h': 2,       # Half note (2 beats)
##    'dh': 3,      # Dotted half note (3 beats)
##    'w': 4        # Whole note (4 beats)
##}


import os
import random
from mido import MidiFile, MidiTrack
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import glob

# Set MIDI folder path
midi_folder = "./Unison MIDI Chord Pack"

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
    try:
        # Select chord progression randomly
        folders = [f for f in os.listdir(base_folder) if os.path.isdir(os.path.join(base_folder, f))]
        selected_folder = random.choice(folders)
        return os.path.join(base_folder, selected_folder)
    except FileNotFoundError:
        print(f"Folder not found: {base_folder}")
        return None

def process_text(text, beats_per_measure, note_values_mapping):
    # Create MIDI file
    mid = MidiFile()
    output_track = MidiTrack()
    mid.tracks.append(output_track)

    # Initialize total time variable
    total_time = 0

    # Split text into sentences (verse/chorus)
    sentences = text.split("\n\n")

    # Process each sentence (verse/chorus)
    for sentence in sentences:
        # Split sentence into lines (words and punctuation)
        lines = sentence.split("\n")

        # Process each line (word or punctuation)
        for line in lines:
            words = line.strip().split()
            for word in words:
                # Filter out punctuation and unwanted characters
                word = ''.join(c for c in word if c.isalpha())

                # Check if the word is not empty after filtering and has at least one character
                if word and len(word) > 0:
                    # Check if the word is capitalized (Verse)
                    if word[0].isupper():
                        # Enter 4 Progressions folder (1st step)
                        base_folder = os.path.join(midi_folder, "4 Progressions")
                        # Enter random chord progression folder (2nd step)
                        base_folder = select_chord_progression_folder(base_folder)

                        if base_folder is None:
                            print(f"No chord progression folder found for '{word}'")
                            continue
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

                        if base_folder is None:
                            print(f"No major/minor folder found for '{word}'")
                            continue

                    print(f"Selected folder for '{word}': {base_folder}")


                    # Search for MIDI files within selected folder and its subfolders
                    midi_files = glob.glob(os.path.join(base_folder, "**/*.mid"), recursive=True)

                    # Select random MIDI file from list of MIDI files
                    selected_midi_path = random.choice(midi_files)

                    print(f"Selected MIDI file: {selected_midi_path}")

                    # Read selected MIDI file
                    selected_mid = MidiFile(selected_midi_path)

                    # Calculate total time of selected MIDI file
                    midi_time = 0
                    for msg in selected_mid.play():
                        midi_time += msg.time

                    # Calculate word duration based on the number of characters in the word
                    word_duration = midi_time / len([c for c in word if c.strip()])  # Exclude spaces from the count

                    # Adjust the duration of the notes
                    modified_messages = []
                    for msg in selected_mid.play():
                        msg.time += total_time
                        msg.time = round(msg.time)
                        modified_messages.append(msg)

                    for i in range(len(modified_messages) - 1):
                        msg = modified_messages[i]
                        if msg.type == 'note_on':
                            note_off_msg = None
                            for j in range(i + 1, len(modified_messages)):
                                if modified_messages[j].type == 'note_off' and modified_messages[j].note == msg.note:
                                    note_off_msg = modified_messages[j]
                                    break
                            if note_off_msg:
                                char_duration = note_values_mapping.get(word[i], 1)  # Each character represents a duration
                                adjusted_duration = round(word_duration * char_duration * beats_per_measure)
                                if adjusted_duration <= 0:
                                    adjusted_duration = 1  # Set a minimum duration of 1 tick to avoid negative duration
                                note_off_msg.time = msg.time + adjusted_duration

                    # Append modified messages to the output track
                    for msg in modified_messages:
                        output_track.append(msg)

                    # Update total time variable
                    total_time += midi_time

    # Save MIDI file
    mid.save('output6.mid')

# Customization settings
lyrics = """
(Verse 1)
In a world of sunshine, we dance hand in hand,
Underneath the moonlight, we'll build a castle in the sand.
You and me, together, like birds of a feather,
Our love's a melody, that'll last forever.

(Chorus)
You're my sunshine, my sweet delight,
With you, every day feels so bright.
When you smile, the world comes alive,
You're the magic in my life.
"""

beats_per_measure = 16  # Custom beats per measure (you can change this to 32 or any other value)
note_values_mapping = {
    't': 1/3,   # Tuplet (1/3 times the base duration)
    'e': 0.5,   # Eighth note (0.5 beat)
    's': 0.25,  # Sixteenth note (0.25 beat)
    'q': 1,     # Quarter note (1 beat)
    'h': 2,     # Half note (2 beats)
    'w': 4      # Whole note (4 beats)
}

# Test the function with the given example
process_text(lyrics, beats_per_measure, note_values_mapping)
