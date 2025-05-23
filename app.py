import streamlit as st
import pickle
import requests

# Load data
movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Set your TMDB API key here
API_KEY = 'c592172537b957fe9a13742d14a6188d'  # Replace with your actual API key

# Function to fetch poster and link
def fetch_poster(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US'
    response = requests.get(url)
    if response.status_code != 200:
        return None, f"https://www.themoviedb.org/movie/{movie_id}"
    data = response.json()
    poster_path = data.get('poster_path')
    poster_url = f"https://image.tmdb.org/t/p/w500/{poster_path}" if poster_path else None
    link = data.get('homepage') or f"https://www.themoviedb.org/movie/{movie_id}"
    return poster_url, link

# Recommend movies
def recommend(movie):
    movie = movie.lower()
    if movie not in movies['title'].str.lower().values:
        return ["Movie not found."], [None], [None]

    index = movies[movies['title'].str.lower() == movie].index[0]
    distances = list(enumerate(similarity[index]))
    movies_list = sorted(distances, reverse=True, key=lambda x: x[1])[1:9]

    recommended_titles = []
    recommended_posters = []
    recommended_links = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        title = movies.iloc[i[0]].title
        poster, link = fetch_poster(movie_id)
        recommended_titles.append(title)
        recommended_posters.append(poster)
        recommended_links.append(link)

    return recommended_titles, recommended_posters, recommended_links

# Streamlit UI
st.set_page_config(page_title="Movie Recommender", layout="wide")
st.title("🎬 Movie Recommender System with Posters")
st.write("Type a movie name to get 5 similar movie recommendations with posters and links.")

selected_movie = st.text_input("Enter Movie Name")

if st.button('Recommend'):
    if selected_movie:
        names, posters, links = recommend(selected_movie)
        if names[0] == "Movie not found.":
            st.error("❌ Movie not found in database.")
        else:
            cols = st.columns(5)
            for i in range(5):
                with cols[i]:
                    if posters[i]:
                        st.markdown(f"[![{names[i]}]({posters[i]})]({links[i]})", unsafe_allow_html=True)
                    st.caption(names[i])
    else:
        st.warning("⚠️ Please enter a movie name.")
