# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**GrooveMatch 1.0** — A content-based music recommender that matches users to songs based on audio features and mood preferences.

---

## 2. Intended Use  

GrooveMatch is a classroom simulation designed to teach how music recommendation systems work. It takes a user's favorite genre, mood, and energy preference, then recommends songs with matching audio characteristics. The system assumes users have clear, consistent taste preferences (e.g., "I like chill lofi"). This is **not for real users**—it's a simplified model to explore how algorithms make recommendations and where they can go wrong.

---

## 3. How the Model Works  

The recommender compares each song to a user's taste profile using five features: genre, mood, energy level, acoustic preference, and brightness (valence). Each feature gets a score (0–1), then those scores are combined with weights to produce a final match score.

**The formula:** Genre (40%) + Mood (30%) + Energy (15%) + Acoustic (10%) + Valence (5%).

Genre and mood matter most because they define the core sound a user wants. Energy, acoustic preference, and valence refine the match. For example, a lofi chill listener will get lofi songs first (genre match = 0.40 points), then among those, it picks the most chill and low-energy ones. If no perfect matches exist, the system falls back to songs with matching mood or energy, even if the genre is different.

---

## 4. Data  

The dataset contains **18 songs** with seven attributes: genre, mood, energy (0–1), tempo (BPM), valence (0–1), danceability (0–1), and acousticness (0–1).

**Genres:** pop, lofi, rock, ambient, jazz, synthwave, indie pop, hip-hop, country, electronic, classical, metal (12 total).

**Moods:** happy, chill, intense, relaxed, focused, moody, melancholic, sad, aggressive, energetic, playful (11 total).

I added 8 new songs to expand the original 10-song catalog and represent underrepresented genres like metal, classical, country, and hip-hop. However, the catalog is still small—only 2 jazz songs and 1 country song, for example. This limits recommendations for users who like rare genres.

---

## 5. Strengths  

The system works well for users with clear, single-genre preferences. The lofi lover, pop fan, and metal head all got sensible top recommendations that matched their favorite genre perfectly. The system also correctly isolated users into genre bubbles—lofi lovers don't see pop, and pop fans don't see metal—which prevents jarring genre mismatches.

The energy matching works smoothly. When a user wants high-energy songs (0.85), the system scores songs by closeness to that value. A song at 0.82 energy scores better than 0.5, which is mathematically sound.

The acoustic preference and valence weights also add nuance. A user who likes acoustic music will see high-acousticness songs, and users who like happy moods will see brighter songs. These secondary features refine the recommendations without overwhelming the primary genre/mood signal.  

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

**Genre Dominance Creates Filter Bubbles**

During testing with the "Happy but Exhausted" user (who wants happy pop music but low energy ~0.2), the system recommended "Sunrise City" (pop, happy, energy 0.82) as the top match—a song that directly contradicts the user's low-energy preference. The issue: genre and mood weighting (40% + 30% = 70% combined) overwhelm the 15% energy weight, so the algorithm will nearly always pick a song matching the favorite genre, even if it clashes with other stated preferences. This reveals a fundamental bias: users are locked into their favorite genre and rarely discover cross-genre alternatives, even when those alternatives might be better matches for their actual mood or listening context. The weighting system sacrifices flexibility and personalization for simplicity.  

---

## 7. Evaluation  

I tested five distinct user profiles to verify the recommender's behavior across different taste preferences and edge cases:

1. **Chill Lofi Lover** (genre: lofi, mood: chill, energy: 0.4, acoustic: yes)
2. **High-Energy Pop Fan** (genre: pop, mood: happy, energy: 0.85, acoustic: no)
3. **Intense Metal Head** (genre: metal, mood: aggressive, energy: 0.95, acoustic: no)
4. **Happy but Exhausted** (genre: pop, mood: happy, energy: 0.2, acoustic: yes) — *conflicting preferences*
5. **Loud & Acoustic Metal** (genre: metal, mood: aggressive, energy: 0.9, acoustic: yes) — *impossible pairing*

**Profile Comparisons & Insights:**

**Chill Lofi vs. High-Energy Pop:** The lofi lover scored songs in the 0.94–0.40 range, with all top-3 picks being lofi/chill tracks. The pop fan scored similarly high (0.97–0.70), but their top-5 had zero overlap—they rejected lofi entirely. This makes sense: both profiles weight genre at 40%, so a genre mismatch is a ~0.40-point penalty that energy/mood bonuses cannot overcome. The recommender correctly isolated these into separate genre bubbles.

**High-Energy Pop vs. Intense Metal:** Despite opposite moods (happy vs. aggressive) and genres (pop vs. metal), both profiles scored their perfect-match songs in the 0.96–0.97 range. However, when their preferred genres were unavailable, the pop fan rated electronic/playful songs (0.42), while the metal fan dropped to hip-hop/rock (0.55). This shows the algorithm respects genre hierarchy: pop fans won't accept rock, but a metal fan will accept rock as a closer alternative than pop. The mood weight (30%) was insufficient to bridge the genre gap in either direction.

**Happy but Exhausted (conflicting preferences):** This profile revealed a critical flaw. The top recommendation was "Sunrise City" (pop, happy, energy 0.82)—the *opposite* of the user's energy preference (0.2). The system picked it anyway because genre + mood (70%) dominated energy (15%). A user asking for "happy but low-energy" should get acoustic, mellow pop songs, not club-ready dance tracks. Instead, the algorithm chose genre/mood consistency over energy match. This is a real limitation of the weighting system.

**Loud & Acoustic Metal (impossible pairing):** Metal is rarely acoustic, and the data confirms this. The top recommendation was "Heavy Metal Thunder" (acoustic: 0.05), which barely satisfies the acoustic preference. The system correctly picked it anyway because metal + aggressive + high-energy are too strong (0.871 score). The acoustic preference was penalized heavily (0.01 contribution vs. typical 0.09), showing the algorithm gracefully degrades when preferences conflict—it doesn't break, but it won't force a recommendation that violates genre/mood priorities.

**What Surprised Me:** I expected the "Happy but Exhausted" case to produce low scores across the board, but the algorithm happily recommended high-energy pop songs because genre + mood satisfied 70% of the scoring criteria. This taught me that content-based filtering with fixed weights can create surprising mismatches when user preferences are internally conflicted. Real recommenders use user feedback or context (time of day, session type) to resolve these tensions—this system cannot.

---

## 8. Future Work  

**Add dynamic weighting:** Instead of fixed 40-30-15-10-5 weights, ask users how much they care about each feature. A user might say "mood is more important than genre to me," and the system would adjust weights accordingly.

**Use context:** Add time-of-day or session-type hints. A user's preferences at 7am (workout) differ from 11pm (wind-down). The system could adjust energy preferences based on context.

**Improve diversity:** After finding the top match, deprioritize songs by the same artist or genre in subsequent recommendations. This prevents five lofi songs in a row.

**Handle conflicting preferences:** Detect when a user's stated preferences conflict (e.g., "happy but low-energy") and either ask for clarification or suggest compromise recommendations (e.g., acoustic happy songs instead of dance pop).

**Expand the dataset:** Add more songs per genre, especially for underrepresented genres like jazz, country, and classical. Larger catalogs improve recommendation quality.

---

## 9. Personal Reflection  

Building this recommender taught me that weighting features is a design decision, not just math. A 40% genre weight seemed reasonable, but it created filter bubbles where users can't discover cross-genre matches. Real recommendation systems use feedback loops and context to avoid this—Spotify learns from skips and playlists, not just static preferences.

I was surprised by how the "Happy but Exhausted" case exposed the system's brittleness. Two conflicting preferences shouldn't just ignore one of them; they should trigger a conversation with the user or produce compromise recommendations. This showed me that content-based filtering is simple but inflexible compared to real systems.

Most importantly, I realized that recommender systems aren't neutral tools—they embody choices about what matters (genre over energy, popular over niche). Building this system made me think critically about the music apps I use daily. When Spotify recommends pop when I wanted chill, it's not magic—it's weighted features. And those weights reflect design decisions that might not match my actual preferences.  
