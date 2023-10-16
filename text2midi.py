import os
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# MIDI 파일 경로 설정
midi_folder = "/Users/mac/git/privateGPT/gpt2music/Unison MIDI Chord Pack"

def analyze_sentiment(text):
    """
    Analyze the sentiment of the given text using VADER sentiment analyzer.
    Returns the compound sentiment score.
    """
    # Initialize VADER sentiment analyzer
    nltk.download('vader_lexicon')
    sid = SentimentIntensityAnalyzer()

    # Calculate sentiment scores
    sentiment_scores = sid.polarity_scores(text)
    return sentiment_scores['compound']

def select_folder(text):
    """
    Select major or minor folder based on the sentiment of the given text.
    Returns the path of the selected folder.
    """
    # Analyze the sentiment of the text
    sentiment_score = analyze_sentiment(text)

    # Select major or minor folder
    folder = "major" if sentiment_score >= 0 else "minor"
    return os.path.join(midi_folder, folder)

def select_key_folder(text, base_folder):
    """
    Select key folder based on the length of the given text.
    Returns the path of the selected key folder.
    """
    # Select key based on the length of the text
    key_index = len(text) % 12 + 1
    key_folder = os.path.join(base_folder, f"{key_index:02} - {os.path.basename(base_folder)}")
    return key_folder

def select_chord_progression_folder(text, base_folder):
    """
    Select chord progression folder based on the alphabetical order of the first character of the given text.
    Returns the path of the selected chord progression folder.
    """
    # Select chord progression based on the alphabetical order of the first character
    chord_progression_index = (ord(text[0].lower()) - ord('a')) % 4 + 1
    chord_progression_folder = os.path.join(base_folder, f"{chord_progression_index:01} Triads")
    return chord_progression_folder

if __name__ == "__main__":
    # Input text
    text = "love"

    # Select major or minor folder
    base_folder = select_folder(text)
    
    # Select key folder
    key_folder = select_key_folder(text, base_folder)
