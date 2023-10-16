import random

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
#notes = ['도','도#','레','레#','미','파','파#','솔','솔#','라','라#','시']
notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

# Define the key (e.g. "A") 
key = "A"

# Find the index of the key in the list of notes
key_index = notes.index(key)

# Define the scale degrees
scale_degrees = {
    'I': 0,
    'ii': 2,
    'iii': 4,
    'IV': 5,
    'V': 7,
    'vi': 9,
    'VII': 11,
    'Ib': 11,  # Flat version of 'I'
    'II': 2,   # Upper case 'II' (different from 'ii')
    'III': 4,  # Upper case 'III' (different from 'iii')
    'VI': 9,   # Upper case 'VI' (different from 'vi')
    'I#': 1,   # Sharp version of 'I'
}

# Choose a random chord progression
chord_progression = random.choice(chord_progressions)

# Generate the chords
chords = []
for degree in chord_progression:
    # Calculate the index of the chord
    chord_index = (key_index + scale_degrees[degree]) % len(notes)
    
    # Get the chord
    chord = notes[chord_index]
    
    # Add the chord to the list of chords
    chords.append(chord)

# Print the chords
print(chords)

from midiutil import MIDIFile

# Create a new MIDI file with one track
midi = MIDIFile(1)

# Set the tempo (in beats per minute)
tempo = 120
midi.addTempo(0, 0, tempo)

# Define the duration of each chord (in beats)
duration = 1

# Define the volume of each chord (0-127)
volume = 100

# Add the chords to the MIDI file
for i, chord in enumerate(chords):
    # Convert the chord to a MIDI pitch number
    pitch = notes.index(chord) + 60
    
    # Add the note to the MIDI file
    midi.addNote(0, 0, pitch, i * duration, duration, volume)

# Save the MIDI file
with open('chords_mono.mid', 'wb') as f:
    midi.writeFile(f)