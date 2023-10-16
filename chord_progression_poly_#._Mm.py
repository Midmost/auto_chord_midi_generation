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
    # Add more minor progressions here
]
# Define the list of notes
notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

# Create a dictionary to map note names to MIDI values
note_to_midi = {
    'C': 60, 'C#': 61, 'D': 62, 'D#': 63, 'E': 64, 'F': 65,
    'F#': 66, 'G': 67, 'G#': 68, 'A': 69, 'A#': 70, 'B': 71
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

all_chords = []

 # Choose the chord progression list based on major or minor
if major_progression:
    chord_progression_list = major_chord_progressions
    key_with_mode = key + " major"  # Change the key as needed for major
else:
    chord_progression_list = minor_chord_progressions
    key_with_mode = key + " minor"  # Change the key as needed for minor

for _ in range(4):
    while True:

        # Generate a random chord progression
        chord_progression = random.choice(chord_progression_list)
        print("Selected chord progression:", chord_progression)


        # Create a chord sequence
        chord_sequence = []
        for chord in chord_progression:
            # Convert lowercase Roman numeral to uppercase
            chord_degree = chord.upper()

            # Calculate the index of the chord within the notes list
            # if chord_degree in notes:
            chord_index = (key_index + scale_degrees[chord_degree]) % len(notes)
            chord_note = notes[chord_index]
            chord_sequence.append(chord_note)

        print("Generated chords:", chord_sequence)
    
        # Check for duplicates
        if len(chord_sequence) == len(set(chord_sequence)):
            break
    
    # Add the chords to the list of all chords
    all_chords.append(chord_sequence)

# Print all chords
print(all_chords)



# Add all chords to the MIDI file as polyphonic chords
time = 0
for chords in all_chords:
    for i, chord in enumerate(chords):
        # # Remove '#' from the chord to convert it to a valid note
        # chord = chord.replace('#', '')
        
        # Convert the chord to a list of MIDI pitch numbers
        pitches = []
        for note in chord.split('/'):
            if note in note_to_midi:
                pitch = note_to_midi[note]
                pitches.append(pitch)
            else:
                print(f"Invalid note in chord: {note}")
        
        # Add all notes in the chord to the MIDI file at the same time
        for pitch in pitches:
            midi.addNote(0, 0, pitch, time, duration, volume)
    
    # Increment time by the duration of one chord
    time += duration

# Save the MIDI file
filename = f'chords_{key_with_mode.replace(" ", "_")}.mid'
with open(filename, 'wb') as f:
    midi.writeFile(f)

print("MIDI file saved as:", filename)
