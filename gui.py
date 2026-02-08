# app.py


from flask import Flask, render_template, request, jsonify

from dataset_module import load_stroke_clinical_dataset_record
from query_module import (
    smokers_hypertension_stroke,
    heart_disease_stroke,
    hypertension_stroke_by_gender,
    smokers_stroke_results,
    area_lived_stroke,
    dietary_habits_stroke,
    hypertension_stroke_patients,
    hypertension_and_stroke_results,
    heart_disease_with_stroke,
    descriptive_analysis,
    average_sleep_hours_stroke
)

# create flask app instance
app = Flask(__name__)  

# attempts to load the dataset
try:
    data = load_stroke_clinical_dataset_record("data.csv")  # Note: Might switch to a config file later
    print(f"Successfully loaded {len(data)} records from dataset!")
except Exception as e:
    print(f"Failed to load dataset: {e}")
    data = {}  #sets the data to an empty dictionary if failed to load

# Map query options to their corresponding functions for easy access
QUERY_DISPATCHER = {
    '1': smokers_hypertension_stroke,
    '2': heart_disease_stroke,
    '3': hypertension_stroke_by_gender,
    '4': smokers_stroke_results,
    '5': area_lived_stroke,
    '6': dietary_habits_stroke,
    '7': hypertension_stroke_patients,
    '8': hypertension_and_stroke_results,
    '9': heart_disease_with_stroke,
    '10': descriptive_analysis,
    '11': average_sleep_hours_stroke
}

@app.route('/')  # loads the index.html home page 
def home():
    """Landing page - just renders index.html"""
    return render_template('index.html')

 
@app.route('/analyze', methods=['POST']) # Define an endpoint for analysis requests
def analyze():   # f
    """
    A function to handle the input the user wants to analyze
    
    Expected input: { "query_id": 1 to 11 }
    """
    user_input = request.get_json(force=True)
    query_id = user_input.get('query_id')  # extract the query id from the user imput

    if not data:
        return jsonify(success=False, message="Oops, dataset not loaded."), 500

    # get the function based on the user selection
    selected_query_fn = QUERY_DISPATCHER.get(query_id)
    
    if not selected_query_fn:
        return jsonify(success=False, message="Invalid option. Try again"), 400

    try:
        output = selected_query_fn(data)  # run the selected query function
        return jsonify(success=True, data=output)  # Returns the analysis results
    except Exception as e:
        print(f"[SERVER ERROR] Query {query_id} analysis crashed: {e}") 
        return jsonify(success=False, message="Something went wrong during query analysis."), 500

# start the flask server
if __name__ == '__main__':

    app.run(debug=True)  # auto reload changes in the code
