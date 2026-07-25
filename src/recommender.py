import csv
from dataclasses import dataclass
from typing import Dict, List, Tuple

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top k songs for a user, ordered by score."""
        if k <= 0:
            return []

        def ranking_key(song: Song) -> Tuple[float, float, int]:
            score, _ = score_song(_profile_to_dict(user), _song_to_dict(song))
            energy_distance = abs(song.energy - user.target_energy)
            return (-score, energy_distance, song.id)

        return sorted(self.songs, key=ranking_key)[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Explain which preferences contributed to a song's score."""
        _, reasons = score_song(_profile_to_dict(user), _song_to_dict(song))
        return ", ".join(reasons)

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file and convert numeric fields to numbers."""
    songs: List[Dict] = []
    float_fields = ("energy", "valence", "danceability", "acousticness")

    with open(csv_path, newline="", encoding="utf-8") as csv_file:
        for row in csv.DictReader(csv_file):
            row["id"] = int(row["id"])
            row["tempo_bpm"] = float(row["tempo_bpm"])
            for field in float_fields:
                row[field] = float(row[field])
            songs.append(row)

    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song and return both its score and an explanation list."""
    favorite_genre = user_prefs.get("favorite_genre", user_prefs.get("genre"))
    favorite_mood = user_prefs.get("favorite_mood", user_prefs.get("mood"))
    target_energy = float(
        user_prefs.get("target_energy", user_prefs.get("energy", 0.5))
    )

    score = 0.0
    reasons: List[str] = []

    if song["genre"].casefold() == str(favorite_genre).casefold():
        score += 1.0
        reasons.append("genre match (+1.0)")

    if song["mood"].casefold() == str(favorite_mood).casefold():
        score += 1.0
        reasons.append("mood match (+1.0)")

    energy_points = 2.0 * max(
        0.0, 1.0 - abs(float(song["energy"]) - target_energy)
    )
    score += energy_points
    reasons.append(f"energy similarity (+{energy_points:.2f})")

    if "likes_acoustic" in user_prefs:
        is_acoustic = float(song["acousticness"]) >= 0.60
        if is_acoustic == bool(user_prefs["likes_acoustic"]):
            score += 0.5
            reasons.append("acoustic preference match (+0.5)")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score every song and return the top k ranked recommendations."""
    if k <= 0:
        return []

    target_energy = float(
        user_prefs.get("target_energy", user_prefs.get("energy", 0.5))
    )
    ranked = []

    for song in songs:
        score, reasons = score_song(user_prefs, song)
        ranked.append((song, score, ", ".join(reasons)))

    return sorted(
        ranked,
        key=lambda item: (
            -item[1],
            abs(float(item[0]["energy"]) - target_energy),
            int(item[0]["id"]),
        ),
    )[:k]


def _song_to_dict(song: Song) -> Dict:
    """Convert a Song object to the dictionary used by the scoring function."""
    return {
        "id": song.id,
        "title": song.title,
        "artist": song.artist,
        "genre": song.genre,
        "mood": song.mood,
        "energy": song.energy,
        "tempo_bpm": song.tempo_bpm,
        "valence": song.valence,
        "danceability": song.danceability,
        "acousticness": song.acousticness,
    }


def _profile_to_dict(user: UserProfile) -> Dict:
    """Convert a UserProfile object to the dictionary used for scoring."""
    return {
        "favorite_genre": user.favorite_genre,
        "favorite_mood": user.favorite_mood,
        "target_energy": user.target_energy,
        "likes_acoustic": user.likes_acoustic,
    }
