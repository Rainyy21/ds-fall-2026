from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# --- Page Configuration ---
st.set_page_config(
    page_title="MovieLens Analytics Dashboard",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Data Loading with Caching ---
@st.cache_data
def load_data():
    """Loads and preprocesses the MovieLens ratings dataset."""
    data_path = Path(__file__).parent / "data" / "movie_ratings.csv"
    if not data_path.exists():
        # Fallback for relative path when run from project root
        data_path = Path("data/movie_ratings.csv")

    df = pd.read_csv(data_path)
    # Ensure year is numeric and drop nulls for release-year analytics
    df["year"] = pd.to_numeric(df["year"], errors="coerce")
    # Clean genres
    df["genres"] = df["genres"].fillna("unknown")
    return df

raw_df = load_data()

# --- Sidebar Filters ---
st.sidebar.title("🎬 MovieLens Controls")
st.sidebar.markdown(
    "Tune the filters below to explore how ratings and genre preferences shift across time and categories."
)

# Year Range Filter
min_year = int(raw_df["year"].dropna().min())
max_year = int(raw_df["year"].dropna().max())

selected_years = st.sidebar.slider(
    "📅 Movie Release Year Range",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year),
    step=1,
    help="Filter movies by their theatrical release year (not rating submission year)."
)

# Genre Multi-select Filter
all_genres = sorted({
    genre
    for sublist in raw_df["genres"].dropna().str.split("|")
    for genre in sublist
    if genre.strip()
})

selected_genres = st.sidebar.multiselect(
    "🎭 Filter by Genre(s)",
    options=all_genres,
    default=[],
    help="Leave empty to include all genres. Selecting genres filters the underlying dataset."
)

# Sidebar helper notes
st.sidebar.divider()
st.sidebar.markdown("### 📊 Dataset Overview")
st.sidebar.info(
    """
    **GroupLens MovieLens 100k**
    - **100,000** ratings
    - **1,682** unique movies
    - **943** users
    - Timeframe: 1922 – 1998
    """
)

# --- Apply Global Filters ---
filtered_df = raw_df.copy()

# Filter by release year
filtered_df = filtered_df[
    (filtered_df["year"].isna()) |
    ((filtered_df["year"] >= selected_years[0]) & (filtered_df["year"] <= selected_years[1]))
]

# Filter by selected genres if any are chosen
if selected_genres:
    pattern = "|".join([r"\b" + g + r"\b" for g in selected_genres])
    filtered_df = filtered_df[filtered_df["genres"].str.contains(pattern, regex=True, na=False)]

# --- Main App Header ---
st.title("🎬 MovieLens Data Science Dashboard")
st.caption(
    "Exploring 100k movie ratings: Genre distributions, viewer satisfaction, historical trends, and sample-size thresholds."
)

# --- Top Level Metrics Row ---
col_m1, col_m2, col_m3, col_m4 = st.columns(4)
total_ratings = len(filtered_df)
unique_movies = filtered_df["movie_id"].nunique()
avg_rating = filtered_df["rating"].mean() if total_ratings > 0 else 0.0
year_span = f"{selected_years[0]} – {selected_years[1]}"

col_m1.metric("Total Ratings", f"{total_ratings:,}")
col_m2.metric("Unique Movies", f"{unique_movies:,}")
col_m3.metric("Average Rating", f"{avg_rating:.2f} ⭐" if total_ratings > 0 else "N/A")
col_m4.metric("Release Window", year_span)

st.divider()

# --- Helper Function for Exploding Genres ---
@st.cache_data
def get_exploded_genre_data(df: pd.DataFrame):
    """Splits pipe-delimited genres and explodes rows."""
    exploded = df.assign(genre=df["genres"].str.split("|")).explode("genre")
    exploded = exploded[exploded["genre"].str.strip() != ""]
    return exploded

exploded_df = get_exploded_genre_data(filtered_df)

# ==============================================================================
# QUESTION 1: Genre Breakdown
# ==============================================================================
st.header("1. Genre Breakdown")
st.markdown(
    """
    > **Question 1:** *What's the distribution of genres among the movies that were rated?*
    """
)

st.info(
    """
    ℹ️ **How Multi-Genre Movies are Handled:**  
    Most movies are tagged with multiple genres (e.g. *Kolya* is *Comedy*, while *Legends of the Fall* is *Drama|Romance|War|Western*).  
    Rather than forcing a single primary genre, we **explode** the pipe-separated (`|`) genre strings so each movie is counted in every genre it represents.  
    Use the toggle below to inspect distribution by **Unique Movie Titles** vs **Total Rating Volume**.
    """
)

q1_mode = st.radio(
    "Select metric for genre distribution:",
    options=["Unique Movies Rated", "Total Ratings Submitted"],
    horizontal=True,
    key="q1_metric_toggle"
)

if q1_mode == "Unique Movies Rated":
    genre_q1 = (
        exploded_df.groupby("genre")["movie_id"]
        .nunique()
        .reset_index(name="count")
        .sort_values(by="count", ascending=True)
    )
    metric_label = "Unique Movies"
else:
    genre_q1 = (
        exploded_df.groupby("genre")["rating"]
        .count()
        .reset_index(name="count")
        .sort_values(by="count", ascending=True)
    )
    metric_label = "Total Ratings"

fig_q1 = px.bar(
    genre_q1,
    x="count",
    y="genre",
    orientation="h",
    labels={"count": metric_label, "genre": "Genre"},
    title=f"Genre Distribution by {metric_label} (Sorted)",
    text="count",
    color="count",
    color_continuous_scale="Blues",
)
fig_q1.update_layout(
    xaxis_title=metric_label,
    yaxis_title="Genre",
    showlegend=False,
    height=540,
    margin=dict(l=20, r=40, t=50, b=40),
)
fig_q1.update_traces(texttemplate="%{text:,}", textposition="outside")
st.plotly_chart(fig_q1, use_container_width=True)

st.divider()

# ==============================================================================
# QUESTION 2: Genre Satisfaction
# ==============================================================================
st.header("2. Genre Satisfaction")
st.markdown(
    """
    > **Question 2:** *Which genres have the highest average rating? Which have the lowest?*
    """
)

genre_stats = (
    exploded_df.groupby("genre")
    .agg(
        avg_rating=("rating", "mean"),
        rating_count=("rating", "count"),
        movie_count=("movie_id", "nunique"),
    )
    .reset_index()
    .sort_values(by="avg_rating", ascending=True)
)

if not genre_stats.empty:
    highest_genre = genre_stats.iloc[-1]
    lowest_genre = genre_stats.iloc[0]

    col_q2_high, col_q2_low = st.columns(2)
    col_q2_high.success(
        f"🏆 **Highest Rated Genre:** **{highest_genre['genre']}** ({highest_genre['avg_rating']:.2f} ⭐ avg across {highest_genre['rating_count']:,} ratings)"
    )
    col_q2_low.warning(
        f"📉 **Lowest Rated Genre:** **{lowest_genre['genre']}** ({lowest_genre['avg_rating']:.2f} ⭐ avg across {lowest_genre['rating_count']:,} ratings)"
    )

    fig_q2 = px.bar(
        genre_stats,
        x="avg_rating",
        y="genre",
        orientation="h",
        labels={"avg_rating": "Average Rating (1–5)", "genre": "Genre"},
        title="Average Rating by Genre (Sorted Ascending to Descending)",
        color="avg_rating",
        color_continuous_scale="Tealgrn",
        hover_data={"avg_rating": ":.3f", "rating_count": ":,", "movie_count": ":,"},
        text="avg_rating",
    )
    fig_q2.update_layout(
        xaxis=dict(range=[2.5, 4.3], title="Average Rating"),
        yaxis_title="Genre",
        height=540,
        margin=dict(l=20, r=40, t=50, b=40),
    )
    fig_q2.update_traces(texttemplate="%{text:.2f}", textposition="outside")
    st.plotly_chart(fig_q2, use_container_width=True)
else:
    st.info("No data available for the selected filters.")

st.divider()

# ==============================================================================
# QUESTION 3: Ratings Over Time
# ==============================================================================
st.header("3. Ratings Over Time")
st.markdown(
    """
    > **Question 3:** *How has the mean rating changed across movie release years?*
    """
)

# Ensure we use movie release year, dropping null release years
valid_year_df = filtered_df.dropna(subset=["year"]).copy()
valid_year_df["year"] = valid_year_df["year"].astype(int)

yearly_stats = (
    valid_year_df.groupby("year")
    .agg(
        mean_rating=("rating", "mean"),
        count=("rating", "count"),
        unique_movies=("movie_id", "nunique"),
    )
    .reset_index()
    .sort_values(by="year")
)

st.caption(
    "⚠️ **Analytical Note:** Movie ratings are aggregated by **theatrical release year** (`year`), *not* the timestamp when users submitted ratings (`rating_year`). Notice the high variance in early decades (1920s–1940s) due to very small sample sizes (e.g. 1926 has only 2 ratings), before stabilizing around ~3.3–3.5 in the 1980s and 1990s."
)

if not yearly_stats.empty:
    fig_q3 = go.Figure()

    # Add trend line for Mean Rating
    fig_q3.add_trace(
        go.Scatter(
            x=yearly_stats["year"],
            y=yearly_stats["mean_rating"],
            mode="lines+markers",
            name="Mean Rating",
            line=dict(color="#1f77b4", width=2.5),
            marker=dict(size=6),
            hovertemplate="<b>Year %{x}</b><br>Mean Rating: %{y:.2f} ⭐<extra></extra>",
        )
    )

    # Optional volume bar on secondary axis to explain variance
    fig_q3.add_trace(
        go.Bar(
            x=yearly_stats["year"],
            y=yearly_stats["count"],
            name="Total Ratings (Volume)",
            yaxis="y2",
            opacity=0.25,
            marker_color="#7f7f7f",
            hovertemplate="Ratings Count: %{y:,}<br>Unique Movies: "
            + yearly_stats["unique_movies"].astype(str)
            + "<extra></extra>",
        )
    )

    fig_q3.update_layout(
        title="Mean Rating Across Movie Release Years (With Review Volume Overlay)",
        xaxis=dict(title="Release Year", tickmode="linear", dtick=10),
        yaxis=dict(title="Mean Rating (1–5)", range=[2.0, 5.0]),
        yaxis2=dict(
            title="Rating Count (Volume)",
            overlaying="y",
            side="right",
            showgrid=False,
        ),
        legend=dict(x=0.02, y=0.98, bgcolor="rgba(255,255,255,0.7)"),
        height=480,
        margin=dict(l=20, r=40, t=50, b=40),
        hovermode="x unified",
    )
    st.plotly_chart(fig_q3, use_container_width=True)
else:
    st.info("No movie ratings found for the selected year range.")

st.divider()

# ==============================================================================
# QUESTION 4: Best Movies, With a Floor
# ==============================================================================
st.header("4. Best Movies, With a Floor")
st.markdown(
    """
    > **Question 4:** *What are the top 5 best-rated movies, once you only count movies with at least 50 ratings? What changes if you raise that floor to 150?*
    """
)

# Group by movie to compute counts and averages
movie_aggregates = (
    filtered_df.groupby(["movie_id", "title"])
    .agg(
        rating_count=("rating", "count"),
        mean_rating=("rating", "mean"),
    )
    .reset_index()
)

def get_top_n(df: pd.DataFrame, floor: int, n: int = 5):
    """Filters by floor threshold and returns top n movies."""
    qualifying = df[df["rating_count"] >= floor]
    return qualifying.sort_values(by=["mean_rating", "rating_count"], ascending=[False, False]).head(n)

top_50 = get_top_n(movie_aggregates, floor=50, n=5)
top_150 = get_top_n(movie_aggregates, floor=150, n=5)

# Side-by-side comparison columns
col_f50, col_f150 = st.columns(2)

with col_f50:
    st.subheader("Floor = 50 Ratings")
    st.caption("Includes acclaimed niche films and cult favorites.")
    if not top_50.empty:
        fig_f50 = px.bar(
            top_50.sort_values(by="mean_rating", ascending=True),
            x="mean_rating",
            y="title",
            orientation="h",
            labels={"mean_rating": "Mean Rating", "title": "Movie Title"},
            title="Top 5 (Minimum 50 Ratings)",
            color="mean_rating",
            color_continuous_scale="Purples",
            hover_data={"mean_rating": ":.3f", "rating_count": ":,"},
            text="mean_rating",
        )
        fig_f50.update_layout(xaxis=dict(range=[4.0, 4.6]), showlegend=False, height=340)
        fig_f50.update_traces(texttemplate="%{text:.2f} ⭐", textposition="outside")
        st.plotly_chart(fig_f50, use_container_width=True)

        for i, row in enumerate(top_50.itertuples(), 1):
            st.markdown(f"**{i}. {row.title}** — `{row.mean_rating:.3f}` ⭐ ({row.rating_count:,} reviews)")
    else:
        st.warning("No movies qualify at floor 50 with current filters.")

with col_f150:
    st.subheader("Floor = 150 Ratings")
    st.caption("Only widely-seen consensus cinematic masterpieces.")
    if not top_150.empty:
        fig_f150 = px.bar(
            top_150.sort_values(by="mean_rating", ascending=True),
            x="mean_rating",
            y="title",
            orientation="h",
            labels={"mean_rating": "Mean Rating", "title": "Movie Title"},
            title="Top 5 (Minimum 150 Ratings)",
            color="mean_rating",
            color_continuous_scale="Purples",
            hover_data={"mean_rating": ":.3f", "rating_count": ":,"},
            text="mean_rating",
        )
        fig_f150.update_layout(xaxis=dict(range=[4.0, 4.6]), showlegend=False, height=340)
        fig_f150.update_traces(texttemplate="%{text:.2f} ⭐", textposition="outside")
        st.plotly_chart(fig_f150, use_container_width=True)

        for i, row in enumerate(top_150.itertuples(), 1):
            st.markdown(f"**{i}. {row.title}** — `{row.mean_rating:.3f}` ⭐ ({row.rating_count:,} reviews)")
    else:
        st.warning("No movies qualify at floor 150 with current filters.")

# Insight Callout explaining the statistical divergence
st.markdown("### 💡 What Changes and Why?")
st.info(
    """
    - **At Floor = 50:** Three of the top 5 are British stop-motion animations (*A Close Shave*, *The Wrong Trousers*, *Wallace & Gromit*), which enjoy intense affection from a devoted, smaller audience (67–118 reviews).
    - **At Floor = 150:** Those niche films drop off because they lack mass viewership volume. They are replaced by broad, universally acclaimed cinematic heavyweights (*The Shawshank Redemption*, *Rear Window*, *The Usual Suspects*).
    - **Statistical Takeaway:** Low thresholds reward passionate niche appeal; higher thresholds require widespread consensus across general audiences.
    """
)

# Dynamic Floor Exploration Slider (Interactive Widget)
st.markdown("#### 🎛️ Interactive Custom Floor Explorer")
custom_floor = st.slider(
    "Choose a custom minimum rating floor:",
    min_value=5,
    max_value=300,
    value=100,
    step=5,
    help="Dynamically see how raising or lowering the threshold reshuffles the leaderboard."
)

custom_top = get_top_n(movie_aggregates, floor=custom_floor, n=5)
if not custom_top.empty:
    st.write(f"**Top 5 Movies with at least {custom_floor} ratings:**")
    st.dataframe(
        custom_top[["title", "mean_rating", "rating_count"]].rename(
            columns={"title": "Movie Title", "mean_rating": "Mean Rating", "rating_count": "Rating Count"}
        ),
        use_container_width=True,
        hide_index=True,
    )
