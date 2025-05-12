from flask import Flask, render_template, request
import pickle
import numpy as np
import os
from fuzzywuzzy import process  # Import fuzzy matching library

# Define the directory where the model files are stored
model_dir = os.path.join(os.path.dirname(__file__), 'models')

# Load the pickle files using absolute paths
popular_df = pickle.load(open(os.path.join(model_dir, 'popular.pkl'), 'rb'))
pt = pickle.load(open(os.path.join(model_dir, 'pt.pkl'), 'rb'))
books = pickle.load(open(os.path.join(model_dir, 'books.pkl'), 'rb'))
similarity_scores = pickle.load(open(os.path.join(model_dir, 'similarity_scores.pkl'), 'rb'))

app = Flask(__name__)

@app.route('/')
def index():
    # Debugging: Print the columns of popular_df
    print("Columns in popular_df:", popular_df.columns)

    # Handle missing 'avg_rating' column
    rating_col = None
    for col in ['avg_rating', 'average_rating', 'Average Rating', 'Avg Rating']:
        if col in popular_df.columns:
            rating_col = col
            break
    if rating_col is None:
        # Fallback to the last column if no match is found
        rating_col = popular_df.columns[-1]
        print(f"'avg_rating' column not found. Using fallback column: {rating_col}")

    # Sort the books by rating in descending order and slice the top 50
    top_50_books = popular_df.sort_values(by=rating_col, ascending=False).head(50)

    return render_template('index.html',
                           book_name=list(top_50_books['Book-Title'].values),
                           author=list(top_50_books['Book-Author'].values),
                           image=list(top_50_books['Image-URL-M'].values),
                           votes=list(top_50_books['num_ratings'].values),
                           rating=list(top_50_books[rating_col].values)
                           )

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books', methods=['post'])
def recommend():
    user_input = request.form.get('user_input').strip().lower()  # Normalize user input to lowercase

    # Debugging: Print the user input
    print("User input:", user_input)

    # Ensure the 'Book-Title' column in books is normalized
    books['Book-Title'] = books['Book-Title'].str.strip().str.lower()

    # Ensure the index of pt is normalized
    pt.index = pt.index.str.strip().str.lower()

    # Check if the user_input exists in the books DataFrame
    if user_input not in books['Book-Title'].values:
        print(f"Book '{user_input}' not found in books['Book-Title'].")
        error_message = f"Sorry, the book '{user_input}' was not found in our database."
        return render_template('recommend.html', data=None, error=error_message)

    # Use fuzzy matching to find the closest match in pt.index
    closest_match, score = process.extractOne(user_input, pt.index)
    print(f"Closest match for '{user_input}' is '{closest_match}' with a score of {score}.")

    # Check if the match is good enough (e.g., score > 80)
    if score < 80:
        print(f"No close match found for '{user_input}' in pt.index.")
        # Provide fallback recommendations based on popularity
        fallback_books = popular_df.head(5)[['Book-Title', 'Book-Author', 'Image-URL-M']].values.tolist()
        error_message = f"Sorry, we couldn't generate collaborative recommendations for '{user_input}'. Here are some popular books instead."
        return render_template('recommend.html', data=fallback_books, error=error_message)

    # Find the index of the closest match
    index = np.where(pt.index == closest_match)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]  # Match book titles directly (already normalized)
        # Debugging: Print the matched book details
        print(f"Matched book for similarity index {i[0]}:", temp_df)
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(item)

    print("Recommended books data:", data)

    return render_template('recommend.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)