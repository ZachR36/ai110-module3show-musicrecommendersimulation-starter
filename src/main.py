"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs, UserProfile, EXAMPLE_USER


def main() -> None:
    songs = load_songs("data/songs.csv")

    # Use the example user profile
    user_prefs = EXAMPLE_USER

    print(f"\n{'='*70}")
    print(f"🎵 Music Recommender for: {user_prefs.favorite_genre.title()} + {user_prefs.favorite_mood.title()}")
    print(f"{'='*70}")
    print(f"User preferences: {user_prefs.favorite_genre} music, {user_prefs.favorite_mood} mood, energy ~{user_prefs.target_energy:.1f}")
    print(f"Acoustic preference: {'Yes' if user_prefs.likes_acoustic else 'No'}")
    print(f"{'='*70}\n")

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("Top 5 Recommendations:\n")
    for rank, (song, score, reasons) in enumerate(recommendations, 1):
        print(f"{rank}. {song.title} by {song.artist}")
        print(f"   Genre: {song.genre} | Mood: {song.mood} | Energy: {song.energy:.2f}")
        print(f"   ⭐ Score: {score:.3f} / 1.000")
        print(f"   Why this song:")
        for reason in reasons:
            print(f"     • {reason}")
        print()


if __name__ == "__main__":
    main()
