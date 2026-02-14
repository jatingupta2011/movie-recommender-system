import streamlit as st
import pickle
import requests

# ---------- Poster Fetch ----------
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=c7ec19ffdd3279641fb606d19ceb9bb1&language=en-US"
    data = requests.get(url).json()
    poster_path = data.get("poster_path")

    if poster_path:
        return "https://image.tmdb.org/t/p/w500/" + poster_path
    return "https://via.placeholder.com/300x450?text=No+Image"


# ---------- Load Data ----------
movies = pickle.load(open("movies_list.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))
movies_list = movies["title"].values


# ---------- UI ----------
st.title("🎬 Movie Recommender System")

st.subheader("Popular Movies")

cols = st.columns(5)
popular_ids = [1632, 299536, 17455, 2830, 429422]

for col, mid in zip(cols, popular_ids):
    with col:
        st.image(fetch_poster(mid))


# ---------- Dropdown ----------
selectvalue = st.selectbox("Select a movie", movies_list)


# ---------- Recommendation Logic ----------
def recommend(movie):
    index = movies[movies["title"] == movie].index[0]
    distances = sorted(
        list(enumerate(similarity[index])),
        reverse=True,
        key=lambda x: x[1],
    )

    recommended_movies = []
    recommended_posters = []

    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_posters


# ---------- Button ----------
if st.button("Show Recommendations"):
    movie_names, movie_posters = recommend(selectvalue)

    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.text(movie_names[i])
            st.image(movie_posters[i])
