from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Function to query the database for attractions
def query_attractions(destination, duration, budget):
    conn = sqlite3.connect('your_database.db')
    c = conn.cursor()

    c.execute("SELECT * FROM Attractions \
               WHERE tagged_place LIKE ? \
               AND time_spent <= ? \
               AND predicted_cost <= ?",
              ('%' + destination + '%', duration, budget))

    results = c.fetchall()

    conn.close()

    return results

# API endpoint to handle search requests for attractions
@app.route('/search', methods=['GET'])
def search_attractions():
    # Get parameters from the request
    destination = request.args.get('destination')
    duration = request.args.get('duration')
    budget = request.args.get('budget')

    # Validate parameters
    if not duration or not budget:
        return jsonify({'error': 'Duration and budget parameters are required'}), 400

    try:
        duration = int(duration)
        budget = float(budget)
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid input for duration or budget. Please provide numeric values'}), 400

    # Query the database for attractions
    attractions = query_attractions(destination, duration, budget)

    # Return results as JSON
    return jsonify(attractions)

if __name__ == '__main__':
    app.run(debug=True)
