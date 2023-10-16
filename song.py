import os
import glob
from mido import MidiFile, MidiTrack, Message
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import random

# Set MIDI folder path
midi_folder = "./Unison MIDI Chord Pack"

def analyze_sentiment(text):
    # Initialize VADER sentiment analyzer
    nltk.download('vader_lexicon')
    sid = SentimentIntensityAnalyzer()

    # Calculate sentiment score
    sentiment_scores = sid.polarity_scores(text)
    return sentiment_scores['compound']

def select_random_midi_file(folder):
    midi_files = glob.glob(os.path.join(folder, "**/*.mid"), recursive=True)
    return random.choice(midi_files)

def process_text(text, beats_per_measure, note_values_mapping):
    # Analyze the sentiment of the given lyrics
    sentiment_score = analyze_sentiment(text)

    # Just use the base folder directly
    base_folder = midi_folder

    # Call the process_text_with_chord_folder() function with the selected folder
    process_text_with_chord_folder(text, beats_per_measure, note_values_mapping, base_folder, sentiment_score)

def process_text_with_chord_folder(text, beats_per_measure, note_values_mapping, chord_folder, sentiment_score):
    # Create MIDI file
    mid = MidiFile()
    output_track = MidiTrack()
    mid.tracks.append(output_track)

    # Initialize total time variable
    total_time = 0

    # Split text into sentences
    sentences = text.split(".")

    # Process each sentence
    for sentence in sentences:
        # Split sentence into words
        words = sentence.split()

        # Process each word
        for word in words:
            # Filter out punctuation and unwanted characters
            word = ''.join(c for c in word if c.isalpha())

            # Check if the word is not empty after filtering and has at least one character
            if word and len(word) > 0:
                # Check if the word is capitalized (Verse)
                if word[0].isupper():
                    # Select random MIDI file from the main MIDI folder
                    selected_midi_path = select_random_midi_file(midi_folder)
                else:
                    # Select random MIDI file from the main MIDI folder
                    selected_midi_path = select_random_midi_file(midi_folder)

                print(f"Selected MIDI file: {selected_midi_path}")

                # Read selected MIDI file
                selected_mid = MidiFile(selected_midi_path)

                # Calculate the duration of each character in the word using the note_values_mapping
                char_durations = [note_values_mapping.get(char, 1) * beats_per_measure for char in word]

                # Adjust the duration of the notes
                modified_messages = []
                current_time = total_time
                for msg in selected_mid.play():
                    for i, char_duration in enumerate(char_durations):
                        if msg.type == 'note_on':
                            note_off_msg = None
                            for modified_msg in modified_messages:
                                if modified_msg.type == 'note_off' and modified_msg.note == msg.note:
                                    note_off_msg = modified_msg
                                    break
                            if note_off_msg:
                                adjusted_duration = round(char_duration)
                                if adjusted_duration <= 0:
                                    adjusted_duration = 1  # Set a minimum duration of 1 tick to avoid negative duration
                                note_off_msg.time = msg.time + adjusted_duration

                    msg.time += current_time
                    msg.time = int(round(msg.time))
                    modified_messages.append(msg)

                # Append modified messages to the output track
                for msg in modified_messages:
                    output_track.append(msg)

                # Update total time variable
                total_time += sum(char_durations)

    # Save MIDI file
    mid.save('output_super.mid')

# Customization settings
lyrics = """
I'm super shy, super shy
But wait a minute while I make you mine, make you mine.
"""

beats_per_measure = 8
note_values_mapping = {
    't': 0.6667,  # Tuplet (2/3 times the base duration)
    'e': 0.5,     # Eighth note (0.5 beat)
    's': 0.25,    # Sixteenth note (0.25 beat)
    'q': 1,       # Quarter note (1 beat)
    'dq': 1.5,    # Dotted quarter note (1.5 beats)
    'h': 2,       # Half note (2 beats)
    'dh': 3,      # Dotted half note (3 beats)
    'w': 4        # Whole note (4 beats)
}

# Test the function with the given example
process_text(lyrics, beats_per_measure, note_values_mapping)
