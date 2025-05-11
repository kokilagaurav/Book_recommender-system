from flask import Flask,render_template,request
import pickle
import numpy as np
import os

# Define models directory path
models_dir = os.path.join('models')

# Fix file paths using os.path.join
popular_df = pickle.load(open(os.path.join(models_dir, 'popular.pkl'), 'rb'))
pt = pickle.load(open(os.path.join(models_dir, 'pt.pkl'), 'rb'))
books = pickle.load(open(os.path.join(models_dir, 'books.pkl'), 'rb'))
similarity_scores = pickle.load(open(os.path.join(models_dir, 'similarity_scores.pkl'), 'rb'))

app = Flask(__name__)

@app.route('/')
def index():
    # Debug: print columns to console
    print("popular_df columns:", popular_df.columns)
    # Try common alternatives for the rating column
    rating_col = None
    for col in ['avg_rating', 'average_rating', 'Average Rating', 'Avg Rating']:
        if col in popular_df.columns:
            rating_col = col
            break
    if rating_col is None:
        rating_col = popular_df.columns[-1]  # fallback to last column

    # Sort by rating column in descending order and slice the top 50 books
    top_50 = popular_df.sort_values(by=rating_col, ascending=False).head(50)

    return render_template('index.html',
                           book_name=list(top_50['Book-Title'].values),
                           author=list(top_50['Book-Author'].values),
                           image=list(top_50['Image-URL-M'].values),
                           votes=list(top_50['num_ratings'].values),
                           rating=list(top_50[rating_col].values)
                           )

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books', methods=['post'])
def recommend():
    user_input = request.form.get('user_input').strip().lower()  # Normalize user input to lowercase

    # Normalize the index of pt to lowercase for case-insensitive matching
    normalized_index = pt.index.str.lower()

    # Check if the user_input exists in the normalized index
    if user_input not in normalized_index:
        # Handle the case where the book is not found
        error_message = f"Sorry, the book '{user_input}' was not found in our database."
        return render_template('recommend.html', data=None, error=error_message)

    # Find the index of the book
    index = np.where(normalized_index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'].str.lower() == pt.index[i[0]].lower()]  # Match book titles case-insensitively
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(item)

    print(data)

    return render_template('recommend.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)