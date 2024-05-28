import streamlit as st
import pickle
import pandas as pd
import requests


def fetch_poster(movie_id):
    api_key = "YOUR_TMDB_API_KEY"  # Replace with your TMDb API key
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}"
    headers = {
        "Content-Type": "application/json",
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        poster_path = data.get('poster_path')
        return "http://image.tmdb.org/t/p/w500/" + poster_path



movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    # Fetch poster from API
    movie_id = movies.iloc[movie_index].id
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(similarity[movie_index])), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []  # making a new list of recommended movies
    recommended_movies_posters = []
    for i in movie_list:
        recommended_movies.append(movies.iloc[i[0]].title)  # to convert index to title of the movie
        # Fetch poster from API using movie ID
        recommended_movies_posters.append(fetch_poster(movies.iloc[i[0]].id))
    return recommended_movies, recommended_movies_posters


st.title('Movie Recommender')


# Define the special_internal_function
def special_internal_function(option):
    # Your formatting logic goes here
    return option


# Rest of your Streamlit code
label = "Select a movie:"
options = movies['title'].values
index = 0

format_func = special_internal_function

selected_option = st.selectbox(label=label, options=options, index=index, format_func=format_func)

# Assuming you want to create a button with the same label as the selectbox
button_label = "Recommend"
clicked_button = st.button(button_label, key=None, help=None, on_click=None, args=None, kwargs=None, type="secondary",
                           disabled=False, use_container_width=False)

# You can use 'clicked_button' to check if the button was clicked
if clicked_button:
    # Assuming 'recommend' returns a tuple with two lists: recommendations and posters
    recommendations, posters = recommend(selected_option)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommendations[0])
        st.image(posters[0])

    with col2:
        st.text(recommendations[1])
        st.image(posters[1])

    with col3:
        st.text(recommendations[2])
        st.image(posters[2])

    with col4:
        st.text(recommendations[3])
        st.image(posters[3])

    with col5:
        st.text(recommendations[4])
        st.image(posters[4])
