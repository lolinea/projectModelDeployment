# Import library
import pandas as pd
import pickle
import joblib

def load_file(filename):
    with open(filename, 'rb') as file:
        files = joblib.load(file)
    return files

# Function untuk memperoleh rekomendasi
def get_recommendations(title, df, indices, cosine_sim, num_recommend = 5):
    title = title.lower()
    idx = indices.get(title)
    if idx is None:
        return f"Film '{title}' tidak ditemukan dalam database."

    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda df: df[1], reverse=True)
    top_similar = sim_scores[1:num_recommend+1]

    movie_indices = [i[0] for i in top_similar]
    ret_df = pd.DataFrame(df[['title', 'type', 'country', 'rating', 'listed_in']].iloc[movie_indices])
    ret_df['score'] = [i[1] for i in top_similar]
    return ret_df.reset_index(drop=True)

def main():
    cosine_sim = load_file('cosinesim.pkl')
    indices = load_file('indices.pkl')
    df = load_file('netflix_title.pkl')

    user_input = 'Once Upon a Time in London'
    recommendations = get_recommendations(user_input, df, indices, cosine_sim)

    pd.set_option('display.width', None)
    print(recommendations)

if __name__ == "__main__":
    main()

