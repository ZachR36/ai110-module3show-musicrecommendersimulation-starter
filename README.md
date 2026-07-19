# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Real-world recommendation engines like Spotify and YouTube use a hybrid approach: they analyze what similar users liked (collaborative filtering), examine the actual audio/content features of songs (content-based filtering), and factor in context like time of day or device. This simulation focuses on **content-based filtering**—a technique that matches a user's stated taste preferences directly to the audio characteristics of songs.

**How it works:**
- **Input data:** Song features (genre, mood, energy, tempo, valence, danceability, acousticness)
- **User preferences:** The user's stated preferred genre, mood, and energy level, plus weights indicating how much each feature matters
- **Scoring:** The recommender compares each song's features to the user's preferences and outputs a similarity score
- **Ranking/selection:** Songs are ranked by score (highest first) and the top matches are recommended

This content-based approach has a key advantage: new songs can be recommended immediately based on their audio attributes alone, without waiting for user interaction history (avoiding the "cold start" problem in collaborative filtering).

### Song Features
Each `Song` object contains:
- **Categorical attributes:** `genre` (pop, lofi, rock, etc.), `mood` (happy, chill, intense, etc.)
- **Audio metrics:** `energy` (0-1 intensity scale), `tempo` (BPM), `valence` (0-1 brightness/happiness), `danceability` (0-1), `acousticness` (0-1)

### UserProfile Features
Each `UserProfile` stores:
- **Preferred genre** and **mood** (what the user gravitates toward)
- **Preferred energy level** (do they like high-energy or calm songs?)
- **Preference weights** (how much to emphasize genre vs. mood vs. energy when scoring)

### How the Recommender Computes a Score
For each song, the recommender calculates a weighted similarity score using this algorithm recipe:

```
Total Score = (genre_score × 0.40) + (mood_score × 0.30) + (energy_score × 0.15) 
            + (acoustic_score × 0.10) + (valence_score × 0.05)
```

**Scoring rules for each feature:**
- **Genre (40%):** Exact match = 1.0; similar genre family = 0.6; different = 0.0
- **Mood (30%):** Exact match = 1.0; similar mood = 0.5; opposite mood = 0.1
- **Energy (15%):** Continuous distance score = `1 - |user_target - song_energy|` (rewards closeness)
- **Acoustic (10%):** Rewards songs that match user's acoustic preference (high if user likes acoustic and song is acoustic, etc.)
- **Valence (5%):** Adjusts for song brightness/happiness based on mood category

### Ranking Rule
Songs are ranked by their total score (highest first). The top K songs are recommended.

### Known Biases in This Design
- **Genre dominance:** The algorithm heavily favors genre matching (40%), which may cause filter bubbles—users who like pop will mostly get pop recommendations, even if there are excellent chill songs in other genres.
- **Acoustic preference:** Users with `likes_acoustic=True` will rarely get synth-heavy or electronic recommendations, even if they match mood and energy perfectly.
- **Narrow taste profiles:** A user who likes "chill lofi" will rarely discover "intense metal," even if they might enjoy it—the multi-feature weighting prevents cross-genre discovery.
- **Valence underweighting:** At 5% weight, valence has minimal impact, so a happy pop song and a sad pop song score almost identically for a pop fan.
- **No temporal context:** The system ignores time of day, session context, or recency—it treats every recommendation as context-free.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
# e.g.:
# User profile: genre=indie, mood=chill, energy=low
# Recommendations:
#   1. ...
#   2. ...
#   3. ...
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



