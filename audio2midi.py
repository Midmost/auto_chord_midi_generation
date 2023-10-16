import librosa

# Load the audio file
audio_file = 'path/to/your/audio/file.mp3'
y, sr = librosa.load(audio_file)

# Perform pitch detection
pitches, magnitudes = librosa.piptrack(y=y, sr=sr)

# Perform onset detection
onset_frames = librosa.onset.onset_detect(y=y, sr=sr)
onset_times = librosa.frames_to_time(onset_frames, sr=sr)

# Segment notes based on onsets and offsets
notes = []
for i in range(len(onset_times) - 1):
    start_time = onset_times[i]
    end_time = onset_times[i + 1]
    duration = end_time - start_time
    pitch = pitches[:, i].argmax()  # Get the pitch with the highest magnitude
    notes.append((start_time, duration, pitch))

from magenta.protobuf import music_pb2

def create_midi(notes):
    # Create a new MIDI sequence
    sequence = music_pb2.NoteSequence()

    # Set the time signature and tempo (adjust as needed)
    sequence.time_signatures.add(numerator=4, denominator=4)
    sequence.tempos.add(qpm=120)

    # Add notes to the sequence
    for start_time, duration, pitch in notes:
        note = sequence.notes.add()
        note.start_time = start_time
        note.end_time = start_time + duration
        note.pitch = pitch
        note.velocity = 64  # Adjust the velocity as needed

    return sequence

# Create MIDI sequence
midi_sequence = create_midi(notes)

# Save MIDI file
output_file = 'audio2midi.mid'
with open(output_file, 'wb') as f:
    f.write(midi_sequence.SerializeToString())
