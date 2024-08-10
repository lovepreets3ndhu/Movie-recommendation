import streamlit as st
import pickle
import requests
import pandas as pd


def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(
        movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


# Function to recommend movies
def recommend(movie):
    movie = movie.strip().lower()
    movies_lists['normalized_title'] = movies_lists['title'].str.strip().str.lower()
    if movie in movies_lists['normalized_title'].values:
        movie_index = movies_lists[movies_lists['normalized_title'] == movie].index[0]
        distance = similarity[movie_index]
        movie_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:6]
        recommended_movies = []
        recommended_movies_poster=[]
        for i in movie_list:
            movie_id = movies_lists.iloc[i[0]].movie_id
            recommended_movies_poster.append(fetch_poster(movie_id))
            #fetch poster from api
            recommended_movies.append(movies_lists.iloc[i[0]].title)
        return recommended_movies,recommended_movies_poster
    else:
        return ["Movie not found in the list."]


similarity = pickle.load(open('similarity.pkl', 'rb'))
movies_lists = pickle.load(open('movies.pkl', 'rb'))

if isinstance(movies_lists, pd.DataFrame) and 'title' in movies_lists.columns:
    movie_titles = movies_lists['title'].values
else:
    st.error("Invalid movies list structure.")

# Streamlit app
st.title('Movie Recommender System')

selected = st.selectbox(
    "Select a movie:",
    (movie_titles))

if st.button("Recommend"):
    names,posters = recommend(selected)
    col1, col2, col3,col4,col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0])

    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])

    with col4:
        st.text(names[3])
        st.image(posters[3])

    with col5:
        st.text(names[4])
        st.image(posters[4])
