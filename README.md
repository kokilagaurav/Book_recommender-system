# Book Recommender System

This is a Flask-based web application that recommends books to users based on their input. It uses pre-trained models and datasets to provide personalized book recommendations.

## Features

- Displays the top 50 popular books on the homepage.
- Allows users to search for a book and get recommendations for similar books.
- Case-insensitive search for book titles.
- Handles errors gracefully when a book is not found in the database.

## Project Structure

```
Book_recommender_system/
│
├── app.py                # Main Flask application
├── models/               # Directory containing pre-trained models
│   ├── popular.pkl
│   ├── pt.pkl
│   ├── books.pkl
│   └── similarity_scores.pkl
├── templates/            # HTML templates for the web application
│   ├── index.html
│   └── recommend.html
├── requirements.txt      # Python libraries required for the project
└── README.md             # Project documentation
```

## Prerequisites

- Python 3.x
- Flask
- Required Python libraries (listed in `requirements.txt` if available)

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd Book_recommender_system
   ```

2. Install the required Python libraries:
   ```bash
   pip install -r requirements.txt
   ```

3. Ensure the `models` directory contains the following files:
   - `popular.pkl`
   - `pt.pkl`
   - `books.pkl`
   - `similarity_scores.pkl`

4. Run the Flask application:
   ```bash
   python app.py
   ```

5. Open your browser and navigate to `http://127.0.0.1:5000/`.

## Usage

- Visit the homepage to view the top 50 popular books.
- Use the recommendation page to search for a book and get similar book recommendations.

## Notes

- The application assumes that the datasets and models are pre-trained and stored in the `models` directory.
- Ensure that the column names in the datasets match the expected names in the code.

## License

This project is licensed under the MIT License. See the LICENSE file for details.