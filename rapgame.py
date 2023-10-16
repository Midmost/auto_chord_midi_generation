import mido

def note_to_name(note):
    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    return notes[note % 12] + str(note // 12 - 1)

def load_midi_file(file_path):
    try:
        midi_file = mido.MidiFile(file_path)
        return midi_file
    except FileNotFoundError:
        print("Error: MIDI file not found.")
        return None

# Path to the MIDI file
midi_file_path = "/Users/mac/git/privateGPT/gpt2music/rapgame.mid"

# Load the MIDI file
midi_file = load_midi_file(midi_file_path)

# Check if the file was loaded successfully
if midi_file:
    
    midi_file.save('/Users/mac/rapgame.mid')

    # Example: Print all MIDI messages in the file in the desired format
    for message in midi_file:
        if message.type == 'note_on':
            print(f"Note\t\t{message.channel + 1}\t\t{note_to_name(message.note)}\t\t{message.velocity}")
        elif message.type == 'note_off':
            print(f"Note\t\t{message.channel + 1}\t\t{note_to_name(message.note)}\t\t{message.velocity}")

else:
    # Handle the case when the file couldn't be loaded
    print("Error loading MIDI file.")
