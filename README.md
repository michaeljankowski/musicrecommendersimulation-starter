# Music Recommender Simulation

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

My recommender compares a user's stated taste with the information stored for
each song. The catalog includes genre and mood labels, along with energy,
tempo, valence, danceability, and acousticness. Those numerical features add
some detail that genre alone cannot capture. For example, energy and
acousticness make it easy to tell an intense rock track from a chill lofi track.
Real services do something similar at a much larger scale, although they also
learn from listening history, skips, likes, and patterns shared by many users.

The profile I will use for the first test is:

```python
user_profile = {
    "favorite_genre": "pop",
    "favorite_mood": "happy",
    "target_energy": 0.80,
    "likes_acoustic": False,
}
```

This profile is specific enough to separate upbeat pop from low-energy,
acoustic lofi without requiring every song to be an exact match. A `Song` stores
`id`, `title`, `artist`, `genre`, `mood`, `energy`, `tempo_bpm`, `valence`,
`danceability`, and `acousticness`. A `UserProfile` stores `favorite_genre`,
`favorite_mood`, `target_energy`, and `likes_acoustic`.

### Algorithm Recipe

For every song, the recommender will:

1. Add 1.0 point when the genre matches the user's favorite genre.
2. Add 1.0 point when the mood matches the user's favorite mood.
3. Add up to 2.0 energy-similarity points using
   `2 * (1 - abs(song.energy - user.target_energy))`.
4. Add 0.5 points when the song's acousticness agrees with the user's acoustic
   preference. An acousticness value of 0.60 or higher counts as acoustic.
5. Sort all songs from highest score to lowest score and return the top `k`.
   If two songs tie, the song whose energy is closer to the target comes first.

The planned data flow is:

`User preferences + songs.csv -> score each song -> sort by score -> top k songs`

Energy has the largest weight after a sensitivity experiment showed that exact
genre and mood matches could overwhelm a major energy mismatch. This can create
a different bias: songs with the right intensity may outrank songs that better
match the user's requested style. The small, hand-written catalog also cannot
represent every style evenly, so genres with more songs have more chances to
appear in the results.

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
python -m pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

```text
Loaded songs: 18

Profile: High-Energy Pop
------------------------

1. Sunrise City by Neon Echo
   Score: 4.34
   Reasons: genre match (+1.0), mood match (+1.0), energy similarity (+1.84), acoustic preference match (+0.5)

2. Gym Hero by Max Pulse
   Score: 3.44
   Reasons: genre match (+1.0), energy similarity (+1.94), acoustic preference match (+0.5)

3. Rooftop Lights by Indigo Parade
   Score: 3.22
   Reasons: mood match (+1.0), energy similarity (+1.72), acoustic preference match (+0.5)

4. Storm Runner by Voltline
   Score: 2.48
   Reasons: energy similarity (+1.98), acoustic preference match (+0.5)

5. Electric Sky by Phase Garden
   Score: 2.48
   Reasons: energy similarity (+1.98), acoustic preference match (+0.5)
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
