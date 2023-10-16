import random
from midiutil import MIDIFile

# Define the list of chord progressions
major_chord_progressions = [
    ['I', 'IV', 'V'],
    ['I', 'vi', 'IV', 'V'],
    ['I', 'IV', 'vi', 'V'],
    ['I', 'V', 'vi', 'IV'],
    ['IV', 'I', 'V', 'VI'],
    ['IV', 'I', 'VI', 'V'],
    ['I', 'V', 'IV', 'V'],
    ['I', 'IV', 'IV', 'V'],
    ['II', 'V', 'I', 'IV'],
    ['I', 'IV', 'V', 'IV'],
    ['I', 'ii', 'IV', 'V'],
    ['I', 'IV', 'vi', 'IV', 'V'],
    ['I', 'V', 'IV', 'I', 'V'],
    ['V', 'IV', 'I', 'IV'],
    ['I', 'IV', 'V', 'vi'],
    ['I', 'V', 'IV', 'IV'],
    ['II', 'IV', 'I', 'V'],
    # Add more major progressions here
]

minor_chord_progressions = [
    ['ii', 'V', 'I'],
    ['iii', 'vi', 'ii', 'V'],
    ['I', 'vi', 'iii', 'IV'],
    ['iii', 'vi', 'IV', 'V'],
    ['I', 'vi', 'II', 'V'],
    ['iii', 'vi', 'II', 'III'],
    ['ii', 'V', 'vi', 'IV'],
    ['i', 'iv', 'v', 'i'],
    ['i', 'VII', 'III', 'VI'],
    ['iv', 'i', 'VI', 'V'],
    ['ii', 'iii', 'vi', 'V'],
    ['iv', 'v', 'i', 'iv'],
    ['i', 'III', 'VI', 'VII'],
    ['iv', 'VII', 'III', 'VI'],
    ['ii', 'V', 'i', 'iv'],
    ['i', 'VI', 'iv', 'V'],
    # Add more minor progressions here
]

# Define the list of notes
notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

# Create a dictionary to map note names to MIDI values
note_to_midi = {
    'C': 60, 'C#': 61, 'D': 62, 'D#': 63, 'E': 64, 'F': 65,
    'F#': 66, 'G': 67, 'G#': 68, 'A': 69, 'A#': 70, 'B': 71
}

# Define a dictionary to map scale degrees to intervals
scale_degrees_intervals = {
    'I': [0, 4, 7],   # Major Chord: 1, 3, 5
    'ii': [2, 5, 9],  # Minor Chord: 1, b3, 5
    # Define more scale degrees and their intervals as needed
}

# Define the scale degrees
scale_degrees = {
    'I': 0,
    'I#': 1,   # Sharp version of 'I'
    'ii': 2,
    'II': 2,   # 'II' 코드 정의
    'III': 3,  # Sharp version of 'ii'
    'III#': 4, # Sharp version of 'iii'
    'IV': 5,
    'IV#': 6,  # Sharp version of 'IV'
    'V': 7,
    'V#': 8,   # Sharp version of 'V'
    'vi': 9,
    'VI#': 10, # Sharp version of 'VI'
    'VII': 11,
    'VII#': 0, # Sharp version of 'VII', wraps around to 'I'
    'iii': 3,  # 'iii' 코드 정의
    'VI': 9,   # 'VI' 코드 정의
}

# Create a new MIDI file with one track
midi = MIDIFile(1)

# Set the tempo (in beats per minute)
tempo = 60
midi.addTempo(0, 0, tempo)

# Define the duration of each chord (in beats)
duration = 1

# Define the volume of each chord (0-127)
volume = 100

# Define the key (e.g. "A")
key = input("Enter a key (e.g. A#): ")

# Find the index of the key in the list of notes
key_index = notes.index(key)

# Specify whether you want a major or minor progression
major_progression_input = input("Type True or False (T: major, F: minor) ").strip().lower()
major_progression = major_progression_input == 'true'  # Convert to boolean

# Define the key and mode based on user input
key_with_mode = key + (" major" if major_progression else " minor")


all_chords = []
previous_chord = None
previous_progression = None 

# Choose the chord progression list based on major or minor
if major_progression:
    chord_progression_list = major_chord_progressions
else:
    chord_progression_list = minor_chord_progressions


# Create a function to find a chord progression that avoids dissonance and is unique
def find_chord_progression(previous_chord, progression_list):
    while True:
        chord_progression = random.choice(progression_list)
        # Check if the chord progression contains dissonant intervals
        dissonant = False
        if previous_chord is not None:
            for chord_degree in chord_progression:
                if chord_degree in scale_degrees_intervals:
                    chord_intervals = scale_degrees_intervals[chord_degree]
                    if any(interval in chord_intervals for interval in previous_chord):
                        dissonant = True
                        break
        if not dissonant:
            return chord_progression

# Create a function to find a chord progression that is not the same as the previous one
def find_unique_chord_progression(previous_progression, progression_list):
    while True:
        chord_progression = random.choice(progression_list)
        if chord_progression != previous_progression:
            return chord_progression

# Create a function to generate chords for a given note (root) and chord type (major or minor)
def generate_chords(root, chord_type):
    chord = []
    if chord_type == 'major':
        chord = [root, notes[(notes.index(root) + 4) % 12], notes[(notes.index(root) + 7) % 12]]
    elif chord_type == 'minor':
        chord = [root, notes[(notes.index(root) + 3) % 12], notes[(notes.index(root) + 7) % 12]]
    return chord

# Generate chords and add to the list
for _ in range(4):
    # Generate a random chord progression that avoids dissonance and is unique
    chord_progression = find_unique_chord_progression(previous_progression, chord_progression_list)
    previous_progression = chord_progression

    # Iterate through each chord in the progression
    for chord_degree in chord_progression:
        # Convert lowercase Roman numeral to uppercase
        chord_degree_upper = chord_degree.upper()

        # Calculate the index of the chord within the notes list
        chord_index = (key_index + scale_degrees[chord_degree_upper]) % len(notes)
        root_note = notes[chord_index]

        # Generate the chord for the root note based on major or minor progression
        chord_type = 'major' if major_progression else 'minor'
        generated_chord = generate_chords(root_note, chord_type)

        # Add the generated chord to the list of all chords
        all_chords.append(generated_chord)

# Add all chords to the MIDI file as polyphonic chords
time = 0
for chords in all_chords:
    for i, chord_note in enumerate(chords):
        # Convert the chord to a list of MIDI pitch numbers
        pitch = note_to_midi[chord_note]
        midi.addNote(0, 0, pitch, time, duration, volume)
    
    # Increment time by the duration of one chord
    time += duration

# Save the MIDI file
filename = f'chords_{key_with_mode.replace(" ", "_")}.mid'
with open(filename, 'wb') as f:
    midi.writeFile(f)

print("MIDI file saved as:", filename)
