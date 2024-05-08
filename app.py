from flask import Flask, request, jsonify,redirect,url_for,render_template
from sqlalchemy import create_engine, text
import pandas as pd
from preprocessing import preprocess_data
from sentiment_analysis import analyze_sentiment
app = Flask(__name__)

# Connect to MySQL database
engine = create_engine('mysql+mysqlconnector://root:Saravanan007@localhost/drug_reviews')

@app.route('/')
def index():
    return '''<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Drug Sentiment Analysis</title>
        <style>
            body {
            background-image: url('static/background_image.jpg');
            background-size: cover;
            background-repeat: no-repeat;
            background-position: center;
            font-family: Arial, sans-serif;
            margin: 0; /* Remove default margin */
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            overflow: hidden;
        }
            .container {
                max-width: 600px;
                background-color: rgba(255, 255, 255, 0.5);
                margin: 0 auto;
                padding: 20px;
                text-align:center;
            }

            .form-group {
                margin-bottom: 20px;
            }

            button {
                padding: 10px 20px;
                background-color: #007bff;
                color: #fff;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }

            button:hover {
                background-color: #0056b3;
            }
            h1{
                font-size: xx-large;
                font-family: 'Trebuchet MS', 'Lucida Sans Unicode';
                font-style:italic;
                font-weight: 400;
                color: blueviolet;
            }
            input{
                padding: 7px 10px;
                margin: 8px 0;
                box-sizing: border-box;
                border_radius: 25px;
            }
        </style>
    </head>
    <body>
        <div class="container" >
            <h1>Drug Sentiment Analysis</h1>
            <div class="form-group">
                <label for="drugName">Choose a Drug:</label>
                <input type="text" id="drugName" placeholder="Enter drug name...">
            </div>
            <button onclick="getSentiment()">Get Sentiment</button>
            <br>
            <br>
            <div id="result"></div>
            <br>
            <br>
            <button onclick="location.href='/enter_review'" style="background-color: green;">Enter Review</button>
        </div>

        <script>
            function getSentiment() {
                var drugName = document.getElementById('drugName').value;

                // Make an AJAX request to the backend to get the sentiment score
                var xhr = new XMLHttpRequest();
                xhr.open('GET', `/get_sentiment?drug_name=${drugName}`, true);

                xhr.onload = function() {
                    if (xhr.status >= 200 && xhr.status < 400) {
                        var data = JSON.parse(xhr.responseText);
                    if ('error' in data) {
            document.getElementById('result').innerHTML = data.error;
                    }
                    else{
                        document.getElementById('result').innerHTML = `Sentiment Score for ${drugName}: ${data.sentiment_score}`;}
                    }
                    else {
                        console.error('Error fetching sentiment score:', xhr.statusText);
                    }
                };

                xhr.onerror = function() {
                    console.error('Request failed');
                };

                xhr.send();
            }
        </script>
    </body>
    </html>'''
@app.route('/enter_review', methods=['GET', 'POST'])
def enter_review():
    if request.method == 'POST':
        # Retrieve drug name and review from the form submission
        drug_name = request.form['drug_name']
        review = request.form['review']
        rating = int(request.form.get('rating'))
        df = pd.DataFrame({'Review': [review],'rating':[rating]})
        df = preprocess_data(df)

        # Analyze sentiment
        df = analyze_sentiment(df)

        # Get the sentiment score
        sentiment_score = df['sentiment_score'][0]
        processed_review="11"
        print(drug_name,review,rating,processed_review,sentiment_score)
        conn = engine.connect()
        query = text("INSERT INTO processed_drug (drugName, Review, rating, Processed_Review, sentiment_score) VALUES (:drug_name, :review, :rating, :processed_review, :sentiment_score)")
        conn.execute(query,{
    'drug_name': drug_name,
    'review': review,
    'rating': rating,
    'processed_review': processed_review,
    'sentiment_score': sentiment_score
})
        conn.commit()
        print("Data inserted")
        # Redirect to the home page after adding the review
        return redirect(url_for('index'))
    else:
        return '''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Enter Review</title>
        </head>
        <body>
            <h1>Enter Review</h1>
            <form action="/enter_review" method="post">
                <div>
                    <label for="drugName">Drug Name:</label>
                    <input type="text" id="drugName" name="drug_name" placeholder="Enter drug name...">
                </div>
                <div>
                    <label for="review">Review:</label>
                    <textarea id="review" name="review" placeholder="Enter your review..."></textarea>
                </div>
                <div>
            <label for="rating">Rating (out of 10):</label><br>
            <input type="radio" id="rating1" name="rating" value="1">
            <label for="rating1">1</label><br>
            <input type="radio" id="rating2" name="rating" value="2">
            <label for="rating2">2</label><br>
            <input type="radio" id="rating3" name="rating" value="3">
            <label for="rating3">3</label><br>
            <input type="radio" id="rating4" name="rating" value="4">
            <label for="rating4">4</label><br>
            <input type="radio" id="rating5" name="rating" value="5">
            <label for="rating5">5</label><br>
            <input type="radio" id="rating6" name="rating" value="6">
            <label for="rating6">6</label><br>
            <input type="radio" id="rating7" name="rating" value="7">
            <label for="rating7">7</label><br>
            <input type="radio" id="rating8" name="rating" value="8">
            <label for="rating8">8</label><br>
            <input type="radio" id="rating9" name="rating" value="9">
            <label for="rating9">9</label><br>
            <input type="radio" id="rating10" name="rating" value="10">
            <label for="rating10">10</label><br>
        </div>
                <div>
                    <button type="submit">Submit Review</button>
                </div>
            </form>
        </body>
        </html>
        '''
@app.route('/get_sentiment')
def get_sentiment():
    drug_name = request.args.get('drug_name')
    conn = engine.connect()
    # Execute SQL query to get the average sentiment score for the specific drug
    query = f"SELECT AVG(sentiment_score) FROM processed_drug WHERE drugName='{drug_name}'"
    result = conn.execute(text(query)).fetchone()

    sentiment_score = result[0] if result else None
    if sentiment_score is not None:
        return jsonify(sentiment_score=sentiment_score)
    else:
        return jsonify(error="Drug Not Found")

if __name__ == '__main__':
    app.run(debug=True)
