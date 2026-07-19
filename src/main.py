"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs, UserProfile, EXAMPLE_USER


# Define distinct user preference profiles for testing
USER_PROFILES = {
    "Chill Lofi Lover": EXAMPLE_USER,

    "High-Energy Pop Fan": UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.85,
        likes_acoustic=False
    ),

    "Intense Metal Head": UserProfile(
        favorite_genre="metal",
        favorite_mood="aggressive",
        target_energy=0.95,
        likes_acoustic=False
    ),

    "Happy but Exhausted": UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.2,
        likes_acoustic=True
    ),

    "Loud & Acoustic Metal": UserProfile(
        favorite_genre="metal",
        favorite_mood="aggressive",
        target_energy=0.9,
        likes_acoustic=True
    ),

    "Genre Agnostic Mediator": UserProfile(
        favorite_genre="jazz",
        favorite_mood="focused",
        target_energy=0.5,
        likes_acoustic=True
    ),
}


def display_recommendations(user_name: str, user_prefs: UserProfile, songs, k: int = 5) -> None:
    """Display recommendations for a given user profile."""
    print(f"\n{'='*70}")
    print(f"🎵 Music Recommender for: {user_name}")
    print(f"{'='*70}")
    print(f"User preferences: {user_prefs.favorite_genre} music, {user_prefs.favorite_mood} mood, energy ~{user_prefs.target_energy:.1f}")
    print(f"Acoustic preference: {'Yes' if user_prefs.likes_acoustic else 'No'}")
    print(f"{'='*70}\n")

    recommendations = recommend_songs(user_prefs, songs, k=k)

    print("Top 5 Recommendations:\n")
    for rank, (song, score, reasons) in enumerate(recommendations, 1):
        print(f"{rank}. {song.title} by {song.artist}")
        print(f"   Genre: {song.genre} | Mood: {song.mood} | Energy: {song.energy:.2f}")
        print(f"   ⭐ Score: {score:.3f} / 1.000")
        print(f"   Why this song:")
        for reason in reasons:
            print(f"     • {reason}")
        print()


def main() -> None:
    songs = load_songs("data/songs.csv")

    # Test with all profiles
    for profile_name, user_prefs in USER_PROFILES.items():
        display_recommendations(profile_name, user_prefs, songs)



if __name__ == "__main__":
    main()
