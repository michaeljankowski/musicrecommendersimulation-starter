# Model Card: VibeFinder 1.0

## 1. Model Name

VibeFinder 1.0

## 2. Goal / Task

VibeFinder suggests songs from a small catalog. It compares each song with a
user's favorite genre, mood, target energy, and acoustic preference. Its goal is
to return five songs that fit those preferences.

## 3. Algorithm Summary

The system judges every song separately. A genre match adds 1 point, a mood
match adds 1 point, and closeness to the target energy adds up to 2 points. A
matching acoustic preference adds another 0.5 points. The songs are then sorted
by total score, and the five highest-scoring songs are returned with an
explanation of where their points came from.

I originally gave genre 2 points and energy at most 1 point. During the
experiment, I halved the genre weight and doubled the energy weight. This kept
the arithmetic valid because energy similarity still stays between 0 and 2, but
it made intensity more important in close rankings.

## 4. Data Used

The catalog contains 18 fictional songs. It includes pop, lofi, rock, ambient,
jazz, synthwave, indie pop, classical, hip-hop, metal, folk, electronic, blues,
reggae, and Latin music. Each song also has mood, energy, tempo, valence,
danceability, and acousticness data. The catalog is still very small, and most
genres have only one example.

## 5. Observed Behavior / Biases

The strongest results occur when genre, mood, energy, and acoustic preference
agree. “Sunrise City” feels like the right first choice for High-Energy Pop
because it matches pop and happy, is close to the 0.90 energy target, and is
non-acoustic. The Chill Lofi and Deep Intense Rock profiles also put the most
intuitive song first. This shows that the scoring rule responds to different
tastes.

The system treats genre and mood as exact labels, so related labels such as pop
and indie pop receive no genre-match credit. The conflicted blues workout test
also showed that an exact genre and mood match can still beat a much better
energy match, even when the requested energy is very different. Because most
genres have only one song, the catalog cannot provide much variety within a
style and can create a narrow filter bubble. It also ignores listening history,
artists the user dislikes, and potentially useful features such as tempo,
valence, and danceability.

## 6. Evaluation Process

I tested three normal profiles and one adversarial profile. The adversarial
“Conflicted Blues Workout” profile asks for melancholy blues at 0.95 energy,
even though the only matching blues song has 0.33 energy. The output below is
from the final weight-shift experiment.

### High-Energy Pop

```text
1. Sunrise City — 4.34
   genre match (+1.0), mood match (+1.0), energy similarity (+1.84), acoustic preference match (+0.5)
2. Gym Hero — 3.44
   genre match (+1.0), energy similarity (+1.94), acoustic preference match (+0.5)
3. Rooftop Lights — 3.22
   mood match (+1.0), energy similarity (+1.72), acoustic preference match (+0.5)
4. Storm Runner — 2.48
   energy similarity (+1.98), acoustic preference match (+0.5)
5. Electric Sky — 2.48
   energy similarity (+1.98), acoustic preference match (+0.5)
```

### Chill Lofi

```text
1. Library Rain — 4.40
   genre match (+1.0), mood match (+1.0), energy similarity (+1.90), acoustic preference match (+0.5)
2. Midnight Coding — 4.26
   genre match (+1.0), mood match (+1.0), energy similarity (+1.76), acoustic preference match (+0.5)
3. Spacewalk Thoughts — 3.46
   mood match (+1.0), energy similarity (+1.96), acoustic preference match (+0.5)
4. Focus Flow — 3.30
   genre match (+1.0), energy similarity (+1.80), acoustic preference match (+0.5)
5. Empty Station Blues — 2.44
   energy similarity (+1.94), acoustic preference match (+0.5)
```

### Deep Intense Rock

```text
1. Storm Runner — 4.48
   genre match (+1.0), mood match (+1.0), energy similarity (+1.98), acoustic preference match (+0.5)
2. Gym Hero — 3.44
   mood match (+1.0), energy similarity (+1.94), acoustic preference match (+0.5)
3. Electric Sky — 2.48
   energy similarity (+1.98), acoustic preference match (+0.5)
4. Iron Horizon — 2.36
   energy similarity (+1.86), acoustic preference match (+0.5)
5. Sunrise City — 2.34
   energy similarity (+1.84), acoustic preference match (+0.5)
```

### Conflicted Blues Workout

```text
1. Empty Station Blues — 2.76
   genre match (+1.0), mood match (+1.0), energy similarity (+0.76)
2. Gym Hero — 2.46
   energy similarity (+1.96), acoustic preference match (+0.5)
3. Iron Horizon — 2.46
   energy similarity (+1.96), acoustic preference match (+0.5)
4. Storm Runner — 2.42
   energy similarity (+1.92), acoustic preference match (+0.5)
5. Electric Sky — 2.38
   energy similarity (+1.88), acoustic preference match (+0.5)
```

“Sunrise City” ranks first for High-Energy Pop because it receives both label
matches, 1.84 of the 2 available energy points, and the acoustic bonus. “Gym
Hero” is slightly closer in energy but lacks the happy mood point, so it finishes
second. This matches my intuition: both are energetic pop songs, but the happy
track is a better complete match.

The profile comparisons also showed clear differences:

- High-Energy Pop versus Chill Lofi: the pop list favors bright, non-acoustic
  songs, while the lofi list favors low-energy acoustic songs.
- High-Energy Pop versus Deep Intense Rock: both favor energetic tracks, but
  their genre and mood points give different winners.
- High-Energy Pop versus Conflicted Blues Workout: “Sunrise City” wins the
  coherent pop profile, while the exact blues and melancholy labels narrowly
  keep “Empty Station Blues” first in the conflicted profile.
- Chill Lofi versus Deep Intense Rock: their opposite energy and acoustic
  preferences produce almost completely different top results.
- Chill Lofi versus Conflicted Blues Workout: both can reward “Empty Station
  Blues” for acousticness or labels, but it ranks much higher for the blues
  profile because its genre and mood match.
- Deep Intense Rock versus Conflicted Blues Workout: both request high energy,
  so several energetic songs overlap, but the different labels change the first
  result.

Before the weight shift, “Empty Station Blues” beat the next adversarial result
by 1.90 points. After the shift, its lead fell to 0.30 points. The experiment
made the system more responsive to energy and improved the conflicted case. It
did not fully solve it because two exact label matches still add up.

## 7. Intended Use and Non-Intended Use

This project is intended for learning about scoring, ranking, experiments, and
recommendation bias. It can be used to compare simple fictional user profiles.
It should not be used by a real music service or treated as a reliable measure
of a person's taste. It should not make high-stakes decisions about users or
artists.

## 8. Ideas for Improvement

- Add more songs from every genre and mood.
- Let users choose their own feature weights.
- Use valence, danceability, and tempo, then add a rule that improves variety.

## 9. Personal Reflection

My biggest learning moment was seeing a mathematically correct result still
feel wrong. “Empty Station Blues” won a high-energy profile because its genre
and mood points hid a large energy mismatch. Changing the weights improved the
result, but it did not completely fix it.

AI tools helped me draft the CSV loader, scoring structure, test profiles, and
clear explanations. I still needed to run the program and check the arithmetic
against my own musical intuition. That check caught the conflicting blues case
and showed why generated code cannot be accepted without testing.

I was surprised that a few weighted rules could produce lists that often felt
personal. The effect came from ranking several weak signals together, not from
the program actually understanding music. If I continued, I would expand the
catalog, test more conflicting profiles, and let each user control the weights.
