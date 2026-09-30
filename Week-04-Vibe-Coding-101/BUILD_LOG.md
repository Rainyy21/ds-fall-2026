# 📝 Vibe Coding Build Log: MovieLens Dashboard

> *"You have to be the driver. AI is sitting shotgun. They can give you directions, but you're ultimately the person behind the wheel."*

This build log captures three authentic moments during the development of the MovieLens Dashboard where engineer intervention corrected AI assumptions, resolved statistical ambiguities, and avoided charting anti-patterns.

---

## Moment 1: Multi-Genre Handling & Chart Trap Avoidance (Question 1)

### 1. The Prompt Given:
> *"Create a visualization showing the genre breakdown across all rated movies in the MovieLens dataset. Make sure to handle movies with multiple genres."*

### 2. What the AI Produced on the First Try:
* **Chart Selection:** The AI generated a circular **Pie Chart** with 19 slices. Slices with small proportions (e.g. Film-Noir, Western, Fantasy) were crushed into unreadable overlapping labels.
* **Data Processing:** The AI grouped directly by the raw `genres` string (e.g., treating `"Action|Adventure"` as a single distinct genre separate from `"Action"` and `"Adventure"`), resulting in over 200 noisy genre combinations instead of the 19 standard MovieLens genres.

### 3. What Was Changed & Why:
* **Data Transformation Intervention:** We rejected grouping by raw strings. We instructed the data pipeline to **explode** the pipe-delimited (`|`) genre column so each movie is counted in every genre it legitimately belongs to.
* **Chart-Craft Intervention:** Replaced the 19-slice pie chart with a **sorted Horizontal Bar Chart** (`px.bar(orientation="h")`). Horizontal bars ensure genre names remain readable without label tilt, and sorting immediately communicates frequency rankings (Drama #1 at 725 movies, Comedy #2 at 505 movies).
* **Added Analytical Depth:** Added an interactive toggle allowing the user to view counts either by *Unique Movies* (1,682 items) or *Total Ratings Volume* (100,000 ratings).

---

## Moment 2: Release Year vs. Rating Timestamp Ambiguity (Question 3)

### 1. The Prompt Given:
> *"Plot how average ratings have changed over time across the MovieLens dataset."*

### 2. What the AI Produced on the First Try:
* **Column Misunderstanding:** The AI defaulted to grouping by `rating_year` (derived from the rating submission `timestamp` in 1997–1998) or grouped by date increments across months.
* **Visual Output:** A short 7-month trend line from 1997 to 1998 that showed minor user rating activity fluctuations, completely missing the historical movie era context.

### 3. What Was Changed & Why:
* **Feature Selection Intervention:** We redirected the model to group by theatrical release year (`year`, extracted from the movie title metadata spanning 1922 to 1998), as specified in the assignment prompt.
* **Statistical Context & Data Quality Handling:**
  - 30 records contained missing `year` values; we filtered these out explicitly rather than coercing them into a dummy year like 0 or 1970.
  - Early decades (1920s–1940s) have very small sample counts (e.g., 1926 had only 2 ratings with a mean of 3.0). To prevent users from misinterpreting early volatile swings as genuine historical decline, we added a secondary volume overlay/tooltip displaying sample size `n` per year, along with an explicit callout.

---

## Moment 3: The Rating Floor & Selection Bias (Question 4)

### 1. The Prompt Given:
> *"Find the top 5 highest-rated movies in the dataset. Then filter for movies with at least 50 ratings and at least 150 ratings."*

### 2. What the AI Produced on the First Try:
* **Threshold Oversight:** The AI initially calculated pure `mean(rating)` grouped by movie title without any minimum review floor.
* **Output:** Obscure movies with a single 5-star rating (e.g., *Santa with Muscles (1996)*, *Great Day in Harlem, A (1994)*) dominated the top 5 leaderboard with a perfect 5.0 score.

### 3. What Was Changed & Why:
* **Threshold Implementation:** We enforced minimum review counts ($n \ge 50$ and $n \ge 150$) using grouped aggregates.
* **Architectural & UI Design:**
  - Rather than just printing two static lists, we built a side-by-side comparative UI to visually illustrate the statistical shift:
    - **At Floor $\ge 50$:** Three of the top 5 are British stop-motion animations (*A Close Shave*, *The Wrong Trousers*, *Wallace & Gromit* with 67–118 reviews).
    - **At Floor $\ge 150$:** The niche animations drop off due to lack of mass volume, and universally recognized cinematic classics (*Schindler's List*, *Casablanca*, *Shawshank Redemption*, *Rear Window*, *The Usual Suspects*) take over.
  - We added an interactive slider allowing the user to freely vary the floor threshold between 5 and 300 to observe real-time leaderboard reshuffling.
