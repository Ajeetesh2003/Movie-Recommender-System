import streamlit as st
import pickle
import pandas as pd
import requests # for api calling

def fetch_poster(movie_id):
    response = requests.get("https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id))

    data = response.json()
    poster_path = data['poster_path']
    return ("https://image.tmdb.org/t/p/w500/" + poster_path)

# ----------------------( Adding and testing new feature )-----------------------------------
def fetch_movie_details(movie_id):
    response = requests.get("https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id))
    return response.json()
#  --------------------------------------------------------

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    # ---------------------
    recommended_movies_id = []
    # -------------------
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id

        # ---------------------------------
        recommended_movies_id.append(movie_id)
        # -----------------------

        recommended_movies.append(movies.iloc[i[0]].title)
        # fetch poster from API
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters, recommended_movies_id

movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

#  ----------------------------(Adding and testing new feature)------------------
# Main function to display the main page or the movie detail page
def main():
    st.title("CineBuddy")
    st.markdown(f"""
        <h2>Movie Recommendor System</h2>""", unsafe_allow_html=True)

    selected_movie_name = st.selectbox(
        'Select a Movie Title',
        movies['title'].values)

    if st.button('Recommend'):
        names, posters, ids = recommend(selected_movie_name)
        st.markdown(f"<h3>Recommendations for {selected_movie_name}</h3>", unsafe_allow_html=True)

        cols = st.columns(5)
        # Wrap the movie cards in a flex container
        st.markdown("""
                <div style="display: flex; flex-wrap: wrap; width=100%; justify-content: center;">
            """, unsafe_allow_html=True)

        for i, (name, poster, movie_id) in enumerate(zip(names, posters, ids)):
            with cols[i]:
                movie_url = f"/?movie_id={movie_id}"
                card_html = f"""
                        <div style="flex:1; text-align: center; margin: 5px; padding: 5px 0 3px; width:100%; height:420px;">
                            <a href="{movie_url}">
                                <img src="{poster}" style="width: 95%; height: 210px; display: block; margin: 5px auto; border-radius: 10px;">
                                <h4 style="color: white; margin: 5px 0">{name}</h4>
                            </a>
                        </div>
                    """
                st.markdown(card_html, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)  # Close the flex container
# -----------------------------------------------------------------------------


# --------------------------- (Adding and testing new feture) ---------------
# Function to display detailed information about the selected movie
def show_movie_details(movie_id):
    movie_details = fetch_movie_details(movie_id)
    poster = f"https://image.tmdb.org/t/p/w500/{movie_details['poster_path']}"
    movie_name = movie_details['title']
    rating = movie_details['vote_average']
    vote_cnt = movie_details['vote_count']
    description = movie_details['overview']

    # prod_comps = movie_details['production_companies']
    # production_companies = []
    #
    # for prod_comp in prod_comps:
    #     production_companies.append(prod_comp["name"])

    ####### Movie Box
    st.markdown(f"""
        <div style="display: flex; flex-wrap: wrap; width: 100%; border: 2px solid white;">
            <div style="flex: 0 0 25%; padding: 10px">
                <div style="width: 90%; height: 50%; margin: 5% 2% 50% ; ">
                    <img src="{poster}" style="width: 100%; height: 100%;">
                </div>
            </div>
            <div style="flex: 0 0 75%;">
                <div style="margin: 2% 0">
                    <h2 style="padding: 2px 3px 2px">{movie_name}</h2>
                </div>
                <div style="margin: 2% 0">
                    <p style="padding: 2px 3px 2px">{movie_details['tagline']}</p>
                </div>
                <div style="display: flex; flex-wrap: wrap; margin: 2% 0">
                    <div style="flex: 0 0 50%;">
                        <h4 style="padding: 2px 3px 2px">Rating: ⭐{rating}/10</h4>
                    </div>
                    <div style="flex: 0 0 50%;">
                        <h4 style="padding: 2px 3px 2px">Vote Count: {vote_cnt}</h4>
                    </div>
                </div>
                <div style="margin: 4px 0">
                    <button style="border-radius: 10%; background-color: black">{movie_details['genres'][0]['name']}</button>
                    <button style="border-radius: 10%; background-color: black">{movie_details['genres'][1]['name']}</button>
                    <br>
                    <br>
                    <p>{description}</p>
                    <h4>Release date: <p>{movie_details['release_date']}</p></h4>
                    <h4>Languages Available:</h4>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


    ######## Production Companies Box

    prod_comps = movie_details['production_companies']
    ht = 27
    width = 75
    pd = 2

    st.markdown(f"""
            <div style="display: block; flex-wrap: wrap; width: 100%; height: 350px; border: 2px solid white;">
                <div style="flex: 1; width: 100%; height: 20%; margin: 0 0 3px 11px; text-align: center">
                    <h2>Production Companies</h2>
                </div>
                <div style="flex: 1; display: flex; flex-wrap: wrap; width: 100%; height: 80%;">
                    <div style="flex: 0 0 15%; height: {ht}%;">
                        <div style="width: {width}%; height: 100%; margin: 0 auto ; background-color: white">
                            <img src="{f"https://image.tmdb.org/t/p/w500/{prod_comps[len(prod_comps)-1]['logo_path']}"}" style="width: 100%; height: 100%;">
                        </div>
                    </div>
                    <div style="flex: 0 0 85%; height: {ht}%;">
                        <h3 style="">{prod_comps[len(prod_comps)-1]['name']}</h3>
                    </div>
                    <div style="flex: 0 0 15%; height: {ht}%;">
                        <div style="width: {width}%; height: 100%; margin: 0 auto; background-color: white">
                            <img src="{f"https://image.tmdb.org/t/p/w500/{prod_comps[0]['logo_path']}"}" style="width: 100%; height: 100%;">
                        </div>
                    </div>
                    <div style="flex: 0 0 85%; height: {ht}%;">
                        <h3>{prod_comps[0]['name']}</h3>
                    </div>
                    <div style="flex: 0 0 15%; height: {ht}%;">
                        <div style="width: {width}%; height: 100%; margin: 0 auto; background-color: white">
                            <img src="{f"https://image.tmdb.org/t/p/w500/{prod_comps[1]['logo_path']}"}" style="width: 100%; height: 100%;">
                        </div>
                    </div>
                    <div style="flex: 0 0 85%; height: {ht}%;">
                        <h3>{prod_comps[1]['name']}</h3>
                    </div>
                </div>
            </div>
    """, unsafe_allow_html=True)

    # st.image(f"https://image.tmdb.org/t/p/w500/{movie_details['poster_path']}")
    # st.title(movie_details['title'])
    # st.markdown(f"**Overview:** {movie_details['overview']}")
    # st.markdown(f"**Release Date:** {movie_details['release_date']}")
    # st.markdown(f"**Rating:** {movie_details['vote_average']}")

    # Printing the JSON
    st.json(movie_details)

# -----------------------------------------------------------------

# ---------------------------(Adding and testing new feature) --------------
# Route pages based on URL
query_params = st.query_params
if "movie_id" in query_params:
    movie_id = query_params["movie_id"]
    show_movie_details(movie_id)
else:
    main()
# ----------------------------------------------------------------------------

# -------Commented Part (old version) -------------------------

# st.title("Movie Recommendor System")
#
# selected_movie_name = st.selectbox(
#     'Select a Movie Title',
#     movies['title'].values)
#
# if st.button('Recommend'):
#     names, posters = recommend(selected_movie_name)
#     # for i in recommendations:
#     #     st.write(i)
#
#     st.markdown(f"<h3>Recommendations for {selected_movie_name}</h3>", unsafe_allow_html=True)
#
#     cols = st.columns(5)
#
#     for i, (name, poster) in enumerate(zip(names, posters)):
#         with cols[i]:
#             st.image(poster, use_column_width='auto')
#             st.markdown(f"<h5 style='text-align: center;'>{name}</h5>", unsafe_allow_html=True)



# Currently most of the things like button and production companies are hard
# coded do them dynamically with the help of loop. Tried but not getting output
# properly so understand and implement it accordingly