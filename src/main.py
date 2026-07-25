"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


def main() -> None:
    """Run the recommender against several contrasting taste profiles."""
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    profiles = {
        "High-Energy Pop": {
            "favorite_genre": "pop",
            "favorite_mood": "happy",
            "target_energy": 0.90,
            "likes_acoustic": False,
        },
        "Chill Lofi": {
            "favorite_genre": "lofi",
            "favorite_mood": "chill",
            "target_energy": 0.30,
            "likes_acoustic": True,
        },
        "Deep Intense Rock": {
            "favorite_genre": "rock",
            "favorite_mood": "intense",
            "target_energy": 0.90,
            "likes_acoustic": False,
        },
        "Conflicted Blues Workout": {
            "favorite_genre": "blues",
            "favorite_mood": "melancholy",
            "target_energy": 0.95,
            "likes_acoustic": False,
        },
    }

    for profile_name, user_prefs in profiles.items():
        print(f"\nProfile: {profile_name}")
        print("-" * (9 + len(profile_name)))
        recommendations = recommend_songs(user_prefs, songs, k=5)

        for position, (song, score, explanation) in enumerate(
            recommendations, start=1
        ):
            print(f"{position}. {song['title']} by {song['artist']}")
            print(f"   Score: {score:.2f}")
            print(f"   Reasons: {explanation}")


if __name__ == "__main__":
    main()
