
import random
from midiutil import MIDIFile

# Define the list of chord progressions
chord_progressions = [
    ['I', 'IV', 'V'],
    ['ii', 'V', 'I'],
    ['I', 'vi', 'IV', 'V'],
    ['I', 'IV', 'vi', 'V'],
    ['I', 'V', 'vi', 'IV'],
    ['IV', 'I', 'V', 'VI'],
    ['ii', 'IV', 'V'],
    ['iii', 'vi', 'ii', 'V'],
    ['IV', 'I', 'IV', 'V'],
    ['I', 'vi', 'iii', 'IV'],
    ['iii', 'vi', 'IV', 'V'],
    ['IV', 'I', 'IV', 'VII'],
    ['I', 'vi', 'II', 'V'],
    ['IV', 'I', 'VI', 'V'],
    ['ii', 'IV', 'I', 'V'],
    ['iii', 'vi', 'I', 'IV'],
    ['IV', 'I', 'II', 'V'],
    ['I', 'vi', 'IV', 'II'],
    ['iii', 'vi', 'II', 'V'],
    ['IV', 'I', 'III', 'VI'],
    ['ii', 'IV', 'II', 'V'],
    ['iii', 'vi', 'III', 'IV'],
    ['IV', 'I', 'III', 'VII'],
    ['I', 'vi', 'II', 'III'],
    ['iii', 'vi', 'II', 'III'],
    ['IV', 'I', 'II', 'III'],
    ['ii', 'IV', 'II', 'III'],
    ['iii', 'vi', 'II', 'II'],
    ['IV', 'I', 'II', 'II'],
    ['I', 'vi', 'II', 'II']
]


# Define the list of notes
notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']


# Define the key (e.g. "A")
key = "A#"

# Find the index of the key in the list of notes
key_index = notes.index(key)

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

# Generate multiple chord progressions
all_chords = []
for _ in range(8):
    while True:
        # Choose a random chord progression
        chord_progression = random.choice(chord_progressions)
        print("Selected chord progression:", chord_progression)

        # Generate the chords
        chords = []
        for degree in chord_progression:
            # Calculate the index of the chord
            chord_index = (key_index + scale_degrees[degree]) % len(notes)
            
            # Get the chord
            chord = notes[chord_index]
            
            # Add the chord to the list of chords
            chords.append(chord)

        print("Generated chords:", chords)
        
        # Check for duplicates
        if len(chords) == len(set(chords)):
            break
    
    # Add the chords to the list of all chords
    all_chords.append(chords)

# Print all chords
print(all_chords)

# Create a dictionary to map note names to MIDI values
note_to_midi = {
    'C': 60, 'C#': 61, 'D': 62, 'D#': 63, 'E': 64, 'F': 65,
    'F#': 66, 'G': 67, 'G#': 68, 'A': 69, 'A#': 70, 'B': 71
}


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
with open('chords_poly_A#_5.mid', 'wb') as f:
    midi.writeFile(f)