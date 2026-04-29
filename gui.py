from flask import Flask, render_template, request, jsonify
from dataset_module import load_stroke_clinical_dataset_record
from query_module import (
    smokers_hypertension_stroke, heart_disease_stroke,
    hypertension_stroke_by_gender, smokers_stroke_results,
    area_lived_stroke, dietary_habits_stroke,
    hypertension_stroke_patients, hypertension_and_stroke_results,
    heart_disease_with_stroke, descriptive_analysis,
    average_sleep_hours_stroke
)

app = Flask(__name__)

try:
    data = load_stroke_clinical_dataset_record("data.csv")
    print(f"Successfully loaded {len(data)} records from dataset!")
except Exception as e:
    print(f"Failed to load dataset: {e}")
    data = {}

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
    '11': average_sleep_hours_stroke,
}

@app.route('/')
def home():
    return render_template('index.html', record_count=len(data))

@app.route('/analyze', methods=['POST'])
def analyze():
    user_input = request.get_json(force=True)
    query_id = user_input.get('query_id')
    feature = user_input.get('feature', 'age')

    if not data:
        return jsonify(success=False, message="Dataset not loaded."), 500

    selected_query_fn = QUERY_DISPATCHER.get(query_id)
    if not selected_query_fn:
        return jsonify(success=False, message="Invalid option."), 400

    try:
        if query_id == '10':
            output = selected_query_fn(data, feature=feature)
        else:
            output = selected_query_fn(data)
        return jsonify(success=True, data=output, query_id=query_id)
    except Exception as e:
        print(f"[ERROR] Query {query_id} failed: {e}")
        return jsonify(success=False, message="Analysis failed."), 500

if __name__ == '__main__':
    app.run(debug=True)