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
Loading songs from data/songs.csv...
Loaded 18 songs.

======================================================================
🎵 Music Recommender for: Lofi + Chill
======================================================================
User preferences: lofi music, chill mood, energy ~0.4
Acoustic preference: Yes
======================================================================

Top 5 Recommendations:

1. Library Rain by Paper Lanterns
   Genre: lofi | Mood: chill | Energy: 0.35
   ⭐ Score: 0.948 / 1.000
   Why this song:
     • ✓ Genre match: lofi (+0.40)
     • ✓ Mood exact match: chill (+0.30)
     • Energy closeness: 0.35 vs target 0.40 (+0.14)
     • Acoustic: 0.86 (acoustic preference) (+0.09)
     • Valence: 0.60 (calm/sad for chill) (+0.02)

2. Midnight Coding by LoRoom
   Genre: lofi | Mood: chill | Energy: 0.42
   ⭐ Score: 0.940 / 1.000
   Why this song:
     • ✓ Genre match: lofi (+0.40)
     • ✓ Mood exact match: chill (+0.30)
     • Energy closeness: 0.42 vs target 0.40 (+0.15)
     • Acoustic: 0.71 (acoustic preference) (+0.07)
     • Valence: 0.56 (calm/sad for chill) (+0.02)

3. Focus Flow by LoRoom
   Genre: lofi | Mood: focused | Energy: 0.40
   ⭐ Score: 0.798 / 1.000
   Why this song:
     • ✓ Genre match: lofi (+0.40)
     • ✓ Mood similar: focused (+0.15)
     • Energy closeness: 0.40 vs target 0.40 (+0.15)
     • Acoustic: 0.78 (acoustic preference) (+0.08)
     • Valence: 0.59 (calm/sad for chill) (+0.02)

4. Spacewalk Thoughts by Orbit Bloom
   Genre: ambient | Mood: chill | Energy: 0.28
   ⭐ Score: 0.541 / 1.000
   Why this song:
     • ✗ Genre mismatch: ambient vs lofi (+0.00)
     • ✓ Mood exact match: chill (+0.30)
     • Energy closeness: 0.28 vs target 0.40 (+0.13)
     • Acoustic: 0.92 (acoustic preference) (+0.09)
     • Valence: 0.65 (calm/sad for chill) (+0.02)

5. Coffee Shop Stories by Slow Stereo
   Genre: jazz | Mood: relaxed | Energy: 0.37
   ⭐ Score: 0.399 / 1.000
   Why this song:
     • ✗ Genre mismatch: jazz vs lofi (+0.00)
     • ✓ Mood similar: relaxed (+0.15)
     • Energy closeness: 0.37 vs target 0.40 (+0.15)
     • Acoustic: 0.89 (acoustic preference) (+0.09)
     • Valence: 0.71 (calm/sad for chill) (+0.01)
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

We tested five different "edge case" user profiles to push the capabilities of the program. Here's the output from those 5 test cases:
```
Loading songs from data/songs.csv...
Loaded 18 songs.

======================================================================
🎵 Music Recommender for: Chill Lofi Lover
======================================================================
User preferences: lofi music, chill mood, energy ~0.4
Acoustic preference: Yes
======================================================================

Top 5 Recommendations:

1. Library Rain by Paper Lanterns
   Genre: lofi | Mood: chill | Energy: 0.35
   ⭐ Score: 0.948 / 1.000
   Why this song:
     • ✓ Genre match: lofi (+0.40)
     • ✓ Mood exact match: chill (+0.30)
     • Energy closeness: 0.35 vs target 0.40 (+0.14)
     • Acoustic: 0.86 (acoustic preference) (+0.09)
     • Valence: 0.60 (calm/sad for chill) (+0.02)

2. Midnight Coding by LoRoom
   Genre: lofi | Mood: chill | Energy: 0.42
   ⭐ Score: 0.940 / 1.000
   Why this song:
     • ✓ Genre match: lofi (+0.40)
     • ✓ Mood exact match: chill (+0.30)
     • Energy closeness: 0.42 vs target 0.40 (+0.15)
     • Acoustic: 0.71 (acoustic preference) (+0.07)
     • Valence: 0.56 (calm/sad for chill) (+0.02)

3. Focus Flow by LoRoom
   Genre: lofi | Mood: focused | Energy: 0.40
   ⭐ Score: 0.798 / 1.000
   Why this song:
     • ✓ Genre match: lofi (+0.40)
     • ✓ Mood similar: focused (+0.15)
     • Energy closeness: 0.40 vs target 0.40 (+0.15)
     • Acoustic: 0.78 (acoustic preference) (+0.08)
     • Valence: 0.59 (calm/sad for chill) (+0.02)

4. Spacewalk Thoughts by Orbit Bloom
   Genre: ambient | Mood: chill | Energy: 0.28
   ⭐ Score: 0.541 / 1.000
   Why this song:
     • ✗ Genre mismatch: ambient vs lofi (+0.00)
     • ✓ Mood exact match: chill (+0.30)
     • Energy closeness: 0.28 vs target 0.40 (+0.13)
     • Acoustic: 0.92 (acoustic preference) (+0.09)
     • Valence: 0.65 (calm/sad for chill) (+0.02)

5. Coffee Shop Stories by Slow Stereo
   Genre: jazz | Mood: relaxed | Energy: 0.37
   ⭐ Score: 0.399 / 1.000
   Why this song:
     • ✗ Genre mismatch: jazz vs lofi (+0.00)
     • ✓ Mood similar: relaxed (+0.15)
     • Energy closeness: 0.37 vs target 0.40 (+0.15)
     • Acoustic: 0.89 (acoustic preference) (+0.09)
     • Valence: 0.71 (calm/sad for chill) (+0.01)


======================================================================
🎵 Music Recommender for: High-Energy Pop Fan
======================================================================
User preferences: pop music, happy mood, energy ~0.8
Acoustic preference: No
======================================================================

Top 5 Recommendations:

1. Sunrise City by Neon Echo
   Genre: pop | Mood: happy | Energy: 0.82
   ⭐ Score: 0.970 / 1.000
   Why this song:
     • ✓ Genre match: pop (+0.40)
     • ✓ Mood exact match: happy (+0.30)
     • Energy closeness: 0.82 vs target 0.85 (+0.15)
     • Acoustic: 0.18 (non-acoustic preference) (+0.08)
     • Valence: 0.84 (bright/happy for happy) (+0.04)

2. Gym Hero by Max Pulse
   Genre: pop | Mood: intense | Energy: 0.93
   ⭐ Score: 0.702 / 1.000
   Why this song:
     • ✓ Genre match: pop (+0.40)
     • ✗ Mood different: intense (+0.03)
     • Energy closeness: 0.93 vs target 0.85 (+0.14)
     • Acoustic: 0.05 (non-acoustic preference) (+0.10)
     • Valence: 0.77 (bright/happy for happy) (+0.04)

3. Rooftop Lights by Indigo Parade
   Genre: indie pop | Mood: happy | Energy: 0.76
   ⭐ Score: 0.542 / 1.000
   Why this song:
     • ✗ Genre mismatch: indie pop vs pop (+0.00)
     • ✓ Mood exact match: happy (+0.30)
     • Energy closeness: 0.76 vs target 0.85 (+0.14)
     • Acoustic: 0.35 (non-acoustic preference) (+0.07)
     • Valence: 0.81 (bright/happy for happy) (+0.04)

4. Bass Drop by DJ Wavelength
   Genre: electronic | Mood: playful | Energy: 0.87
   ⭐ Score: 0.421 / 1.000
   Why this song:
     • ✗ Genre mismatch: electronic vs pop (+0.00)
     • ✓ Mood similar: playful (+0.15)
     • Energy closeness: 0.87 vs target 0.85 (+0.15)
     • Acoustic: 0.12 (non-acoustic preference) (+0.09)
     • Valence: 0.72 (bright/happy for happy) (+0.04)

5. Electric Pulse by Neon Synth
   Genre: electronic | Mood: energetic | Energy: 0.92
   ⭐ Score: 0.420 / 1.000
   Why this song:
     • ✗ Genre mismatch: electronic vs pop (+0.00)
     • ✓ Mood similar: energetic (+0.15)
     • Energy closeness: 0.92 vs target 0.85 (+0.14)
     • Acoustic: 0.08 (non-acoustic preference) (+0.09)
     • Valence: 0.78 (bright/happy for happy) (+0.04)


======================================================================
🎵 Music Recommender for: Intense Metal Head
======================================================================
User preferences: metal music, aggressive mood, energy ~0.9
Acoustic preference: No
======================================================================

Top 5 Recommendations:

1. Heavy Metal Thunder by Iron Fist
   Genre: metal | Mood: aggressive | Energy: 0.96
   ⭐ Score: 0.968 / 1.000
   Why this song:
     • ✓ Genre match: metal (+0.40)
     • ✓ Mood exact match: aggressive (+0.30)
     • Energy closeness: 0.96 vs target 0.95 (+0.15)
     • Acoustic: 0.05 (non-acoustic preference) (+0.10)
     • Valence: 0.32 (neutral for aggressive) (+0.03)

2. Midnight Flow by Urban Beats
   Genre: hip-hop | Mood: aggressive | Energy: 0.85
   ⭐ Score: 0.545 / 1.000
   Why this song:
     • ✗ Genre mismatch: hip-hop vs metal (+0.00)
     • ✓ Mood exact match: aggressive (+0.30)
     • Energy closeness: 0.85 vs target 0.95 (+0.14)
     • Acoustic: 0.15 (non-acoustic preference) (+0.09)
     • Valence: 0.42 (neutral for aggressive) (+0.03)

3. Gym Hero by Max Pulse
   Genre: pop | Mood: intense | Energy: 0.93
   ⭐ Score: 0.417 / 1.000
   Why this song:
     • ✗ Genre mismatch: pop vs metal (+0.00)
     • ✓ Mood similar: intense (+0.15)
     • Energy closeness: 0.93 vs target 0.95 (+0.15)
     • Acoustic: 0.05 (non-acoustic preference) (+0.10)
     • Valence: 0.77 (neutral for aggressive) (+0.03)

4. Storm Runner by Voltline
   Genre: rock | Mood: intense | Energy: 0.91
   ⭐ Score: 0.409 / 1.000
   Why this song:
     • ✗ Genre mismatch: rock vs metal (+0.00)
     • ✓ Mood similar: intense (+0.15)
     • Energy closeness: 0.91 vs target 0.95 (+0.14)
     • Acoustic: 0.10 (non-acoustic preference) (+0.09)
     • Valence: 0.48 (neutral for aggressive) (+0.03)

5. Electric Pulse by Neon Synth
   Genre: electronic | Mood: energetic | Energy: 0.92
   ⭐ Score: 0.293 / 1.000
   Why this song:
     • ✗ Genre mismatch: electronic vs metal (+0.00)
     • ✗ Mood different: energetic (+0.03)
     • Energy closeness: 0.92 vs target 0.95 (+0.15)
     • Acoustic: 0.08 (non-acoustic preference) (+0.09)
     • Valence: 0.78 (neutral for aggressive) (+0.03)


======================================================================
🎵 Music Recommender for: Happy but Exhausted
======================================================================
User preferences: pop music, happy mood, energy ~0.2
Acoustic preference: Yes
======================================================================

Top 5 Recommendations:

1. Sunrise City by Neon Echo
   Genre: pop | Mood: happy | Energy: 0.82
   ⭐ Score: 0.817 / 1.000
   Why this song:
     • ✓ Genre match: pop (+0.40)
     • ✓ Mood exact match: happy (+0.30)
     • Energy closeness: 0.82 vs target 0.20 (+0.06)
     • Acoustic: 0.18 (acoustic preference) (+0.02)
     • Valence: 0.84 (bright/happy for happy) (+0.04)

2. Gym Hero by Max Pulse
   Genre: pop | Mood: intense | Energy: 0.93
   ⭐ Score: 0.514 / 1.000
   Why this song:
     • ✓ Genre match: pop (+0.40)
     • ✗ Mood different: intense (+0.03)
     • Energy closeness: 0.93 vs target 0.20 (+0.04)
     • Acoustic: 0.05 (acoustic preference) (+0.01)
     • Valence: 0.77 (bright/happy for happy) (+0.04)

3. Rooftop Lights by Indigo Parade
   Genre: indie pop | Mood: happy | Energy: 0.76
   ⭐ Score: 0.442 / 1.000
   Why this song:
     • ✗ Genre mismatch: indie pop vs pop (+0.00)
     • ✓ Mood exact match: happy (+0.30)
     • Energy closeness: 0.76 vs target 0.20 (+0.07)
     • Acoustic: 0.35 (acoustic preference) (+0.03)
     • Valence: 0.81 (bright/happy for happy) (+0.04)

4. Spacewalk Thoughts by Orbit Bloom
   Genre: ambient | Mood: chill | Energy: 0.28
   ⭐ Score: 0.292 / 1.000
   Why this song:
     • ✗ Genre mismatch: ambient vs pop (+0.00)
     • ✗ Mood different: chill (+0.03)
     • Energy closeness: 0.28 vs target 0.20 (+0.14)
     • Acoustic: 0.92 (acoustic preference) (+0.09)
     • Valence: 0.65 (bright/happy for happy) (+0.03)

5. Whisper Soft by Piano Dreams
   Genre: classical | Mood: relaxed | Energy: 0.28
   ⭐ Score: 0.292 / 1.000
   Why this song:
     • ✗ Genre mismatch: classical vs pop (+0.00)
     • ✗ Mood different: relaxed (+0.03)
     • Energy closeness: 0.28 vs target 0.20 (+0.14)
     • Acoustic: 0.92 (acoustic preference) (+0.09)
     • Valence: 0.64 (bright/happy for happy) (+0.03)


======================================================================
🎵 Music Recommender for: Loud & Acoustic Metal
======================================================================
User preferences: metal music, aggressive mood, energy ~0.9
Acoustic preference: Yes
======================================================================

Top 5 Recommendations:

1. Heavy Metal Thunder by Iron Fist
   Genre: metal | Mood: aggressive | Energy: 0.96
   ⭐ Score: 0.871 / 1.000
   Why this song:
     • ✓ Genre match: metal (+0.40)
     • ✓ Mood exact match: aggressive (+0.30)
     • Energy closeness: 0.96 vs target 0.90 (+0.14)
     • Acoustic: 0.05 (acoustic preference) (+0.01)
     • Valence: 0.32 (neutral for aggressive) (+0.03)

2. Midnight Flow by Urban Beats
   Genre: hip-hop | Mood: aggressive | Energy: 0.85
   ⭐ Score: 0.483 / 1.000
   Why this song:
     • ✗ Genre mismatch: hip-hop vs metal (+0.00)
     • ✓ Mood exact match: aggressive (+0.30)
     • Energy closeness: 0.85 vs target 0.90 (+0.14)
     • Acoustic: 0.15 (acoustic preference) (+0.01)
     • Valence: 0.42 (neutral for aggressive) (+0.03)

3. Storm Runner by Voltline
   Genre: rock | Mood: intense | Energy: 0.91
   ⭐ Score: 0.334 / 1.000
   Why this song:
     • ✗ Genre mismatch: rock vs metal (+0.00)
     • ✓ Mood similar: intense (+0.15)
     • Energy closeness: 0.91 vs target 0.90 (+0.15)
     • Acoustic: 0.10 (acoustic preference) (+0.01)
     • Valence: 0.48 (neutral for aggressive) (+0.03)

4. Gym Hero by Max Pulse
   Genre: pop | Mood: intense | Energy: 0.93
   ⭐ Score: 0.326 / 1.000
   Why this song:
     • ✗ Genre mismatch: pop vs metal (+0.00)
     • ✓ Mood similar: intense (+0.15)
     • Energy closeness: 0.93 vs target 0.90 (+0.15)
     • Acoustic: 0.05 (acoustic preference) (+0.01)
     • Valence: 0.77 (neutral for aggressive) (+0.03)

5. Sunset Dreams by Country Roads
   Genre: country | Mood: melancholic | Energy: 0.58
   ⭐ Score: 0.235 / 1.000
   Why this song:
     • ✗ Genre mismatch: country vs metal (+0.00)
     • ✗ Mood different: melancholic (+0.03)
     • Energy closeness: 0.58 vs target 0.90 (+0.10)
     • Acoustic: 0.78 (acoustic preference) (+0.08)
     • Valence: 0.38 (neutral for aggressive) (+0.03)


======================================================================
🎵 Music Recommender for: Genre Agnostic Mediator
======================================================================
User preferences: jazz music, focused mood, energy ~0.5
Acoustic preference: Yes
======================================================================

Top 5 Recommendations:

1. Rainy Day Blues by Slow Jazz Trio
   Genre: jazz | Mood: melancholic | Energy: 0.42
   ⭐ Score: 0.678 / 1.000
   Why this song:
     • ✓ Genre match: jazz (+0.40)
     • ✗ Mood different: melancholic (+0.03)
     • Energy closeness: 0.42 vs target 0.50 (+0.14)
     • Acoustic: 0.85 (acoustic preference) (+0.09)
     • Valence: 0.48 (neutral for focused) (+0.03)

2. Coffee Shop Stories by Slow Stereo
   Genre: jazz | Mood: relaxed | Energy: 0.37
   ⭐ Score: 0.674 / 1.000
   Why this song:
     • ✓ Genre match: jazz (+0.40)
     • ✗ Mood different: relaxed (+0.03)
     • Energy closeness: 0.37 vs target 0.50 (+0.13)
     • Acoustic: 0.89 (acoustic preference) (+0.09)
     • Valence: 0.71 (neutral for focused) (+0.03)

3. Focus Flow by LoRoom
   Genre: lofi | Mood: focused | Energy: 0.40
   ⭐ Score: 0.538 / 1.000
   Why this song:
     • ✗ Genre mismatch: lofi vs jazz (+0.00)
     • ✓ Mood exact match: focused (+0.30)
     • Energy closeness: 0.40 vs target 0.50 (+0.14)
     • Acoustic: 0.78 (acoustic preference) (+0.08)
     • Valence: 0.59 (neutral for focused) (+0.03)

4. Library Rain by Paper Lanterns
   Genre: lofi | Mood: chill | Energy: 0.35
   ⭐ Score: 0.389 / 1.000
   Why this song:
     • ✗ Genre mismatch: lofi vs jazz (+0.00)
     • ✓ Mood similar: chill (+0.15)
     • Energy closeness: 0.35 vs target 0.50 (+0.13)
     • Acoustic: 0.86 (acoustic preference) (+0.09)
     • Valence: 0.60 (neutral for focused) (+0.03)

5. Spacewalk Thoughts by Orbit Bloom
   Genre: ambient | Mood: chill | Energy: 0.28
   ⭐ Score: 0.384 / 1.000
   Why this song:
     • ✗ Genre mismatch: ambient vs jazz (+0.00)
     • ✓ Mood similar: chill (+0.15)
     • Energy closeness: 0.28 vs target 0.50 (+0.12)
     • Acoustic: 0.92 (acoustic preference) (+0.09)
     • Valence: 0.65 (neutral for focused) (+0.03)
```

---

## Limitations and Risks

- **Tiny catalog:** Only 18 songs means recommendations get repetitive. Real systems have millions of songs.
- **Genre dominance:** The 40% genre weight creates filter bubbles. Lofi lovers will almost never see rock or metal, even if a specific rock song matches their mood perfectly.
- **Conflicting preferences:** The system can't handle users with contradictory tastes (e.g., "happy but low-energy"). It just picks the highest-scoring match, even if it violates one preference.
- **No cold-start handling:** New users with no preference data get no recommendations. New songs have no interaction history to boost them.
- **Limited attributes:** The system only uses audio features (genre, mood, energy, acoustic, valence). It ignores artist popularity, lyrics, trends, and cultural context. A world-famous song and an obscure song score the same if their audio features match.
- **No serendipity:** The algorithm never surprises users with cross-genre discoveries because genre matching is too strict.

You will go deeper on this in the model card.

---

## Reflection

This project revealed that recommendation systems are not neutral—they're shaped by design choices. I started thinking genre was 40% because it felt right, but that weight has real consequences. It locked users into genre bubbles and prevented cross-genre discovery. In a real system like Spotify, the weights would be tuned based on millions of user interactions, A/B tests, and feedback. Here, my weight was arbitrary, and it biased the entire recommender.

I also learned that bias shows up in subtle ways. The "Happy but Exhausted" user exposed how fixed weights can create contradictions—the system happily ignored the low-energy preference because it was outweighed by genre and mood. Real recommenders handle this by asking follow-up questions, using context (time of day, playlist type), or learning from user behavior (skips, pauses). But a simple content-based system like mine has no way to recover from these mistakes. This made me realize that whenever I use a recommendation app, the suggestions I get aren't magic—they're the result of weighted features and design decisions that might not match my actual needs.

See the full analysis in the [**Model Card**](model_card.md).



