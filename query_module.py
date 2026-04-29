from dataset_module import load_stroke_clinical_dataset_record
data = load_stroke_clinical_dataset_record("data.csv")

# Helper functions
def mean(values):
    if values:
        return round(sum(values) / len(values), 2)
    return None

def median(values):
    sorted_vals = sorted(values)
    n = len(sorted_vals)
    mid = n // 2
    if n % 2 == 0:
        return round((sorted_vals[mid - 1] + sorted_vals[mid]) / 2, 2)
    return round(sorted_vals[mid], 2)

def mode(values):
    if not values:
        return None
    counts = {}
    for v in values:
        counts[v] = counts.get(v, 0) + 1
    max_count = max(counts.values())
    mode_vals = [v for v, count in counts.items() if count == max_count]
    return round(min(mode_vals), 2)

def std_dev(values):
    average = mean(values)
    squared_diffs = [(x - average) ** 2 for x in values]
    variance = sum(squared_diffs) / len(values)
    return round(variance ** 0.5, 2)

def percentiless(values):
    values = sorted(values)
    n = len(values)
    return {
        "25%": round(values[int(n * 0.25)], 2),
        "50%": round(values[int(n * 0.5)], 2),
        "75%": round(values[int(n * 0.75)], 2),
    }

def save_and_export_to_csv(results, filename):
    try:
        with open(filename, "w") as f:
            if type(results) == dict:
                headers = list(results.keys())
                values = [str(results[k]) for k in headers]
                f.write(",".join(headers) + "\n")
                f.write(",".join(values) + "\n")
            elif type(results) == list:
                if not results:
                    return
                first_item = results[0]
                if type(first_item) == dict:
                    headers = list(first_item.keys())
                    f.write(",".join(headers) + "\n")
                    for item in results:
                        row = [str(item.get(h, "")) for h in headers]
                        f.write(",".join(row) + "\n")
        print(f"Results saved to {filename}")
    except Exception as e:
        print(f"Error saving {filename}: {e}")


def smokers_hypertension_stroke(clinical_dataset_record):
    """Age stats for smokers with hypertension who had a stroke."""
    ages = []
    for patient_info in clinical_dataset_record.values():
        try:
            smoking_status = patient_info.get("smoking_status", "").strip().lower()
            smoke = smoking_status in ["formerly smoked", "smokes"]
            hypertension = float(patient_info.get("hypertension")) == 1
            stroke_occurrence = float(patient_info.get("stroke_occurrence")) == 1
            if smoke and hypertension and stroke_occurrence:
                ages.append(float(patient_info.get("age")))
        except (TypeError, ValueError):
            continue

    if not ages:
        return {"Mean Age": None, "Median Age": None, "Mode Age": None, "Patient Count": 0}

    results = {
        "Mean Age": mean(ages),
        "Median Age": median(ages),
        "Mode Age": mode(ages),
        "Patient Count": len(ages),
    }
    save_and_export_to_csv(results, "smokers_hypertension_stroke.csv")
    return results


def heart_disease_stroke(clinical_dataset_record):
    """Age and glucose stats for heart disease patients who had a stroke."""
    ages = []
    glucose_levels = []

    for patient_info in clinical_dataset_record.values():
        try:
            heart_disease = float(patient_info.get("heart_disease")) == 1
            stroke_occurrence = float(patient_info.get("stroke_occurrence")) == 1
            if heart_disease and stroke_occurrence:
                ages.append(float(patient_info.get("age")))
                glucose_levels.append(float(patient_info.get("average_glucose_level")))
        except (TypeError, ValueError):
            continue

    results = {
        "Mean Age": mean(ages),
        "Median Age": median(ages),
        "Mode Age": mode(ages),
        "Mean Glucose Level": mean(glucose_levels),
        "Patient Count": len(ages),
    }
    save_and_export_to_csv(results, "heart_disease_stroke.csv")
    return results


def hypertension_stroke_by_gender(clinical_dataset_record):
    """Age stats by gender for hypertensive patients — stroke vs no stroke."""
    male_with_stroke = []
    male_without_stroke = []
    female_with_stroke = []
    female_without_stroke = []

    for patient_info in clinical_dataset_record.values():
        gender = patient_info.get("gender", "").strip().lower()
        try:
            hypertension = float(patient_info.get("hypertension")) == 1
            stroke_occurrence = float(patient_info.get("stroke_occurrence")) == 1
            age = float(patient_info.get("age"))
        except (TypeError, ValueError):
            continue

        if hypertension:
            if gender == "male":
                if stroke_occurrence:
                    male_with_stroke.append(age)
                else:
                    male_without_stroke.append(age)
            elif gender == "female":
                if stroke_occurrence:
                    female_with_stroke.append(age)
                else:
                    female_without_stroke.append(age)

    results = [
        {"Group": "Female With Stroke", "Mean Age": mean(female_with_stroke), "Median Age": median(female_with_stroke), "Mode Age": mode(female_with_stroke), "Count": len(female_with_stroke)},
        {"Group": "Female Without Stroke", "Mean Age": mean(female_without_stroke), "Median Age": median(female_without_stroke), "Mode Age": mode(female_without_stroke), "Count": len(female_without_stroke)},
        {"Group": "Male With Stroke", "Mean Age": mean(male_with_stroke), "Median Age": median(male_with_stroke), "Mode Age": mode(male_with_stroke), "Count": len(male_with_stroke)},
        {"Group": "Male Without Stroke", "Mean Age": mean(male_without_stroke), "Median Age": median(male_without_stroke), "Mode Age": mode(male_without_stroke), "Count": len(male_without_stroke)},
    ]
    save_and_export_to_csv(results, "hypertension_stroke_by_gender.csv")
    return results


def smokers_stroke_results(clinical_dataset_record):
    """Age stats by smoking status — stroke vs no stroke."""
    groups = {}

    for patient_info in clinical_dataset_record.values():
        try:
            smoking_status = patient_info.get("smoking_status", "Unknown").strip()
            stroke_occurrence = float(patient_info.get("stroke_occurrence")) == 1
            age = float(patient_info.get("age"))
        except (TypeError, ValueError):
            continue

        key = f"{smoking_status} - {'Stroke' if stroke_occurrence else 'No Stroke'}"
        if key not in groups:
            groups[key] = []
        groups[key].append(age)

    results = []
    for group, ages in groups.items():
        results.append({
            "Group": group,
            "Mean Age": mean(ages),
            "Median Age": median(ages),
            "Count": len(ages),
        })
    save_and_export_to_csv(results, "smokers_stroke_results.csv")
    return results


def area_lived_stroke(clinical_dataset_record):
    """Urban vs rural stroke age analysis."""
    urban_stroke = []
    urban_no_stroke = []
    rural_stroke = []
    rural_no_stroke = []

    for patient_info in clinical_dataset_record.values():
        try:
            area = patient_info.get("residence_type", "").strip().lower()
            stroke_occurrence = float(patient_info.get("stroke_occurrence")) == 1
            age = float(patient_info.get("age"))
        except (TypeError, ValueError):
            continue

        if area == "urban":
            if stroke_occurrence:
                urban_stroke.append(age)
            else:
                urban_no_stroke.append(age)
        elif area == "rural":
            if stroke_occurrence:
                rural_stroke.append(age)
            else:
                rural_no_stroke.append(age)

    results = [
        {"Area": "Urban", "Status": "Stroke", "Mean Age": mean(urban_stroke), "Median Age": median(urban_stroke), "Count": len(urban_stroke)},
        {"Area": "Urban", "Status": "No Stroke", "Mean Age": mean(urban_no_stroke), "Median Age": median(urban_no_stroke), "Count": len(urban_no_stroke)},
        {"Area": "Rural", "Status": "Stroke", "Mean Age": mean(rural_stroke), "Median Age": median(rural_stroke), "Count": len(rural_stroke)},
        {"Area": "Rural", "Status": "No Stroke", "Mean Age": mean(rural_no_stroke), "Median Age": median(rural_no_stroke), "Count": len(rural_no_stroke)},
    ]
    save_and_export_to_csv(results, "area_lived_stroke.csv")
    return results


def dietary_habits_stroke(clinical_dataset_record):
    """Dietary habits distribution — stroke vs no stroke patients."""
    dietary_habits_stroke_dict = {}
    dietary_habits_no_stroke = {}

    for patient_info in clinical_dataset_record.values():
        try:
            dietary_habit = patient_info.get("dietary_habits", "Unknown").strip()
            stroke_occurrence = float(patient_info.get("stroke_occurrence")) == 1
        except (TypeError, ValueError):
            continue

        if stroke_occurrence:
            dietary_habits_stroke_dict[dietary_habit] = dietary_habits_stroke_dict.get(dietary_habit, 0) + 1
        else:
            dietary_habits_no_stroke[dietary_habit] = dietary_habits_no_stroke.get(dietary_habit, 0) + 1

    all_habits = set(list(dietary_habits_stroke_dict.keys()) + list(dietary_habits_no_stroke.keys()))
    results = []
    for habit in sorted(all_habits):
        stroke_count = dietary_habits_stroke_dict.get(habit, 0)
        no_stroke_count = dietary_habits_no_stroke.get(habit, 0)
        total = stroke_count + no_stroke_count
        stroke_pct = round((stroke_count / total * 100), 1) if total > 0 else 0
        results.append({
            "dietary_habit": habit,
            "stroke_count": stroke_count,
            "no_stroke_count": no_stroke_count,
            "stroke_percentage": stroke_pct,
        })

    save_and_export_to_csv(results, "dietary_habits_stroke.csv")
    return results


def hypertension_stroke_patients(clinical_dataset_record):
    """List of patients whose hypertension resulted in stroke."""
    hypertension_stroke = []

    for patient_id, patient_info in clinical_dataset_record.items():
        try:
            hypertension = float(patient_info.get("hypertension", 0)) == 1
            stroke_occurrence = float(patient_info.get("stroke_occurrence", 0)) == 1
        except (TypeError, ValueError):
            continue

        if hypertension and stroke_occurrence:
            record = {"patient_id": patient_id}
            record.update(patient_info)
            hypertension_stroke.append(record)

    save_and_export_to_csv(hypertension_stroke, "hypertension_stroke_patients.csv")
    return {"count": len(hypertension_stroke), "records": hypertension_stroke[:50]}  # cap at 50 for display


def hypertension_and_stroke_results(clinical_dataset_record):
    """Summary of hypertensive patients — with and without stroke."""
    with_stroke = 0
    without_stroke = 0

    for patient_info in clinical_dataset_record.values():
        try:
            hypertension = float(patient_info.get("hypertension", 0)) == 1
            stroke_occurrence = float(patient_info.get("stroke_occurrence", 0)) == 1
            if hypertension:
                if stroke_occurrence:
                    with_stroke += 1
                else:
                    without_stroke += 1
        except (TypeError, ValueError):
            continue

    total = with_stroke + without_stroke
    results = {
        "Hypertension With Stroke": with_stroke,
        "Hypertension Without Stroke": without_stroke,
        "Total Hypertensive Patients": total,
        "Stroke Rate (%)": round((with_stroke / total * 100), 1) if total > 0 else 0,
    }
    save_and_export_to_csv(results, "hypertension_and_stroke_results.csv")
    return results


def heart_disease_with_stroke(clinical_dataset_record):
    """Summary of heart disease patients who had a stroke."""
    with_stroke = 0
    without_stroke = 0

    for patient_info in clinical_dataset_record.values():
        try:
            heart_disease = float(patient_info.get("heart_disease", 0)) == 1
            stroke_occurrence = float(patient_info.get("stroke_occurrence", 0)) == 1
            if heart_disease:
                if stroke_occurrence:
                    with_stroke += 1
                else:
                    without_stroke += 1
        except (TypeError, ValueError):
            continue

    total = with_stroke + without_stroke
    results = {
        "Heart Disease With Stroke": with_stroke,
        "Heart Disease Without Stroke": without_stroke,
        "Total Heart Disease Patients": total,
        "Stroke Rate (%)": round((with_stroke / total * 100), 1) if total > 0 else 0,
    }
    save_and_export_to_csv(results, "heart_disease_with_stroke.csv")
    return results


descriptive_columns = {"age", "average_glucose_level", "bmi", "sleep_hours"}

def descriptive_analysis(clinical_dataset_record, feature="age"):
    """Descriptive statistics for a selected numeric feature."""
    if feature not in descriptive_columns:
        return {"error": f"Feature must be one of: {sorted(descriptive_columns)}"}

    values = []
    for patient_info in clinical_dataset_record.values():
        try:
            values.append(float(patient_info.get(feature)))
        except (TypeError, ValueError):
            continue

    if not values:
        return {"error": f"No numeric values found for {feature}"}

    results = {
        "Feature": feature,
        "Count": len(values),
        "Mean": mean(values),
        "Standard Dev": std_dev(values),
        "Min": round(min(values), 2),
        "Max": round(max(values), 2),
        **percentiless(values),
    }
    save_and_export_to_csv(results, f"{feature}_descriptive_analysis.csv")
    return results


def average_sleep_hours_stroke(clinical_dataset_record):
    """Average sleep hours — stroke vs non-stroke patients."""
    stroke_sleep = []
    no_stroke_sleep = []

    for patient_info in clinical_dataset_record.values():
        try:
            stroke_occurrence = float(patient_info.get("stroke_occurrence")) == 1
            sleep_hours = float(patient_info.get("sleep_hours"))
            if stroke_occurrence:
                stroke_sleep.append(sleep_hours)
            else:
                no_stroke_sleep.append(sleep_hours)
        except (TypeError, ValueError):
            continue

    results = {
        "Average Sleep Hours (Stroke)": mean(stroke_sleep),
        "Average Sleep Hours (No Stroke)": mean(no_stroke_sleep),
        "Stroke Patient Count": len(stroke_sleep),
        "Non-Stroke Patient Count": len(no_stroke_sleep),
    }
    save_and_export_to_csv(results, "average_sleep_hours_stroke.csv")
    return results