from flask import Flask, render_template, request, jsonify
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from orchestrator.coordinator_agent import CoordinatorAgent

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_preferences = request.form.to_dict()
        # Add demographic fields with defaults if missing
        user_preferences['age'] = request.form.get('age', '')
        user_preferences['sex'] = request.form.get('sex', '')
        user_preferences['gender'] = request.form.get('gender', '')
        user_preferences['nationality'] = request.form.get('nationality', '')
        user_preferences['participants'] = request.form.get('participants', '')
        coordinator = CoordinatorAgent()
        import markdown
        itinerary_md = coordinator.build_itinerary(user_preferences)
        itinerary = markdown.markdown(itinerary_md)
        return render_template('index.html', itinerary=itinerary, user_preferences=user_preferences)
    return render_template('index.html', itinerary=None, user_preferences=None)

@app.route('/api/itinerary', methods=['POST'])
def api_itinerary():
    user_preferences = request.json
    coordinator = CoordinatorAgent()
    itinerary = coordinator.build_itinerary(user_preferences)
    return jsonify({'itinerary': itinerary})

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')