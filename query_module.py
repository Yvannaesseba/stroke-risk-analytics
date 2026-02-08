from dataset_module import load_stroke_clinical_dataset_record
data = load_stroke_clinical_dataset_record("data.csv")

# These are some helper functions to compute the different statistics throughout the query
def mean(ages):   
    if ages:
        return sum(ages) / len(ages)    
    return None   # Does not return anything if the list of ages is empty


def median(ages):    
    sorted_ages = sorted(ages)   
    n = len(sorted_ages)
    mid = n // 2
   
    if n % 2 == 0:        
        first_middle = sorted_ages[mid - 1] 
        second_middle = sorted_ages[mid]
        median = (first_middle + second_middle) / 2  
        return median
    else:           
        return sorted_ages[mid]


def mode(ages):  
    if not ages:
        return None
    counts = {}
    for age in ages:
        counts[age] = counts.get(age, 0) + 1
    max_count = max(counts.values())
    mode_ages = [age for age, count in counts.items() if count == max_count]  # this return the smallets age in case multiple values have the same number of appearances
    return min(mode_ages)  


def std_dev(values):   # Sample standard deviation
    average = mean(values)
    squared_diffs = [(x - average) ** 2 for x in values]
    variance = sum(squared_diffs) / len(values)
    standard_deviation = variance ** 0.5
    return standard_deviation
    
def percentiless(values):    
    values = sorted(values)
    n = len(values)
    percentiles = {
        "25%": values[int(n * 0.25)],
        "50%": values[int(n * 0.5)],
        "75%": values[int(n * 0.75)],
    }
    return percentiles


def save_and_export_to_csv(results, filename):
    """Simple function to save results into a CSV file (supports dict or list of dicts)."""    # TODO: try using numeric column list defined later
    try:
        with open(filename, "w") as f:
            if type(results) == dict:
                headers = list(results.keys())
                values = []
                for key in headers:
                    value = results[key]
                    values.append(str(value))
                f.write(",".join(headers) + "\n")
                f.write(",".join(values) + "\n")

            elif type(results) == list:
                if len(results) == 0:
                    print("The list is empty.")
                    return
                first_item = results[0]
                if type(first_item) == dict:
                    headers = list(first_item.keys())
                    f.write(",".join(headers) + "\n")
                    for item in results:
                        row = []
                        for header in headers:
                            value = item.get(header, "")
                            row.append(str(value))
                        f.write(",".join(row) + "\n")
                else:
                    print("The list does not contain dictionaries.")
                    return
            else:
                print("Unsupported result format.")
                return
        print(f"Results saved successfully to {filename}")
    except Exception as e:
        print(f"Error saving file {filename}: {e}")



def smokers_hypertension_stroke(clinical_dataset_record):
    """
    An age stats function for those who smoked/smokes, were hypertensive and had a stroke
    """
    ages = []  # store patients' matching with the conditions
    for patient_info in clinical_dataset_record.values():
        try:
            smoking_status = patient_info.get("smoking_status", "").strip().lower()   # cleans it to ease the comparison
            smoke = smoking_status in ["formerly smoked", "smokes"]
            hypertension = float(patient_info.get("hypertension")) == 1  # converts the values to float to avoid wrong calculations
            stroke_occurrence = float(patient_info.get("stroke_occurrence")) == 1

            if smoke and hypertension and stroke_occurrence:
                age = float(patient_info.get("age"))
                ages.append(age)
        except (TypeError, ValueError) as e:
            # Print an error message if the conversion was not successful
            print(f"Skipping record due to an error: {e} in patient_info: {patient_info}")
            continue  # continue with the next patient

    if not ages:
        return { "Mean Age": None, "Mode Age": None, "Median Age": None}

    results_i = {
        "Mean Age" : mean(ages),
        "Median Age" : median(ages),
        "Mode Age": mode(ages),
    }
    save_and_export_to_csv(results_i, "smokers_hypertension_stroke.csv")
    return results_i 



def heart_disease_stroke(clinical_dataset_record):
    """ Age and glucose level stats function of those who had heart disease that resulted in stroke"""

    ages = []
    glucose_levels = []

    for patient_info in clinical_dataset_record.values():
        try: # Skip patients with missing data or unconvertable data
            heart_disease = float(patient_info.get("heart_disease")) == 1
            stroke_occurrence = float(patient_info.get("stroke_occurrence")) == 1

            if heart_disease and stroke_occurrence:
                age = float(patient_info.get("age"))
                ages.append(age)
                average_glucose_level = float(patient_info.get("average_glucose_level"))
                glucose_levels.append(average_glucose_level)
        except (TypeError, ValueError) as e:
            print(f"Skipping record due to an error: {e} in patient_info: {patient_info}")
            continue

    results_ii = {
        "Mean Age": mean(ages),
        "Median Age": median(ages),
        "Mode Age": mode(ages),
        "Average Glucose level": mean(glucose_levels),
    }
    return results_ii




def hypertension_stroke_by_gender(clinical_dataset_record):
    """ Age stats function based on gender for patients whose hypertension resulted to stroke and for those who didn't.
    """
    # empty lists to store ages based on the category that fits
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
        except (TypeError, ValueError) as e:
            print(f"Skipping record due to an error: {e} in patient_info: {patient_info}")
            continue

        if hypertension:   # continue only if they had hypertension
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



    results_iii = [
         {"Group": "Female With Stroke",
          "Mean Age": mean(female_with_stroke),
          "Median Age": median(female_with_stroke),
          "Mode Age": mode(female_with_stroke)},

        {"Group": "Female Without Stroke",
         "Mean Age": mean(female_without_stroke),
         "Median Age": median(female_without_stroke),
         "Mode Age": mode(female_without_stroke)},

        {"Group": "Male With Stroke",
         "Mean Age": mean(male_with_stroke),
         "Median Age": median(male_with_stroke),
         "Mode Age": mode(male_with_stroke)},

        {"Group": "Male Without Stroke",
         "Mean Age": mean(male_without_stroke),
         "Median Age": median(male_without_stroke),
         "Mode Age": mode(male_without_stroke)},
    ]

    save_and_export_to_csv(results_iii, "hypertension_stroke_by_gender.csv")
    return results_iii





def smokers_stroke_results(clinical_dataset_record):
    """ Age stats function for people whose smoking habits resulted to stroke and for those who didn't """
    # Empty lists to store the data by category
    smokers_with_stroke  = []
    smokers_without_stroke = []

    for patient_info in clinical_dataset_record.values():
        smoking_status = patient_info.get("smoking_status", "").strip().lower()
        smoked = smoking_status in ["formerly smoked", "smokes"]

        try: # Attempt to convert their ages to float for condition
            stroke_occurrence = float(patient_info.get("stroke_occurrence")) == 1
            age = float(patient_info.get("age"))
        except (TypeError, ValueError) as e:  #  handles the conversion error
            print(f"Skipping record due to an error: {e} in patient_info: {patient_info}")
            continue

        if smoked:   # continue only if they used to smoke or still smokes
            if stroke_occurrence:
                smokers_with_stroke .append(age)
            else:
                smokers_without_stroke.append(age)

    results_iv = [
    {"Group": "Smokers With Stroke", 
     "Mean Age": mean(smokers_with_stroke),
     "Median Age": median(smokers_with_stroke),
     "Mode Age": mode(smokers_with_stroke)},
     
    {"Group": "Smokers Without Stroke",
     "Mean Age": mean(smokers_without_stroke),
     "Median Age": median(smokers_without_stroke),
     "Mode Age": mode(smokers_without_stroke)}
]
    
    save_and_export_to_csv(results_iv, "smokers_stroke_results.csv")
    return results_iv
	



def area_lived_stroke(clinical_dataset_record):
    """ Age stats function for patients who lived in urban and rural areas that had stroke"""
    # Create two list to contain the ages based on the habitation
    urban_ages = []
    rural_ages = []

    for patient_info in clinical_dataset_record.values():
        residence = patient_info.get("residence_type", "").strip().lower()

        try:
            stroke_occurrence = float(patient_info.get("stroke_occurrence")) == 1
            age = float(patient_info.get("age"))
        except (TypeError, ValueError) as e:  #  handles the conversion error
            print(f"Skipping record due to an error: {e} in patient_info: {patient_info}")
            continue # continue with the next patient

        if stroke_occurrence:  # continue only if they had a stroke
            if residence == "urban":  # check the residence type
                urban_ages.append(age)
            elif residence == "rural":
                rural_ages.append(age)


    results_v = [
        {
            "Residence Type": "urban",
            "Mean Age": mean(urban_ages),
            "Median Age": median(urban_ages),
            "Mode Age": mode(urban_ages)
        },
        {
            "Residence Type": "rural",
            "Mean Age": mean(rural_ages),
            "Median Age": median(rural_ages),
            "Mode Age": mode(rural_ages)
        }
    ]

    save_and_export_to_csv(results_v, "area_lived_stroke.csv")
    return results_v
	
def dietary_habits_stroke(clinical_dataset_record):
    """ Stats function to retrieve the dietary habit(s) of those who had stroke and those who did not have stroke."""
    # Initialise two dictionaries to store information for patients who had stroke and those who didn't
    dietary_habits_stroke = {}
    dietary_habits_no_stroke = {}

    for patient_info in clinical_dataset_record.values():
        try:  # get stroke status and dietary habit 
            stroke_occurrence = float(patient_info.get("stroke_occurrence")) == 1
            dietary_habit = patient_info.get("dietary_habits", "").lower().strip()

            if not dietary_habit: # if no dietary info, move to the next patient
                continue 

            if stroke_occurrence:  # Continue only if the patient had a stroke 
                if dietary_habit in dietary_habits_stroke:  #  update and increment the count in the dictionary if true
                    dietary_habits_stroke[dietary_habit] += 1
                else: # 
                    dietary_habits_stroke[dietary_habit] = 1  
            else: # if patient didn't have a stroke
                if dietary_habit in dietary_habits_no_stroke:  #  update and increment the count in the dictionary if true
                    dietary_habits_no_stroke[dietary_habit] += 1
                else:
                    dietary_habits_no_stroke[dietary_habit] = 1
        except (TypeError, ValueError) as e:  #  handles the conversion error
            print(f"Skipping record due to an error: {e} in patient_info: {patient_info}")
            continue

    results_vi = []
    all_dietary_habits = set(list(dietary_habits_stroke.keys()) + list(dietary_habits_no_stroke.keys()))

    for habit in all_dietary_habits:
        stroke_count = dietary_habits_stroke.get(habit, 0)
        no_stroke_count = dietary_habits_no_stroke.get(habit, 0)
        results_vi.append({
            "dietary_habit": habit,
            "stroke_count": stroke_count,
            "no_stroke_count": no_stroke_count
        })

    save_and_export_to_csv(results_vi, "dietary_habits_stroke.csv")
    return results_vi

def hypertension_stroke_patients(clinical_dataset_record):
    """
    Stats function to return a list of any patient whose hypertension resulted in stroke.
    """
    hypertension_stroke = []  # initializes and empty list to store records of patients meeting these conditions

    for patient_id, patient_info in clinical_dataset_record.items():
        try:
            hypertension = float(patient_info.get("hypertension", 0)) == 1
            stroke_occurrence = float(patient_info.get("stroke_occurrence", 0)) == 1
        except (TypeError, ValueError) as e:  #  handles the conversion error
            print(f"Skipping record due to an error: {e} in patient_info: {patient_info}")
            continue

        if hypertension and stroke_occurrence:
            record = {"patient_id": patient_id}
            # Copy all patient info into the record
            for key, value in patient_info.items():
                record[key] = value
            hypertension_stroke.append(record)

    results_vii = hypertension_stroke
    save_and_export_to_csv(results_vii, "hypertension_stroke_patients.csv")
    return results_vii






def hypertension_and_stroke_results(clinical_dataset_record):
    """
    Stats fxn for those whose hypertension did not result in stroke
    and those whose hypertension resulted in stroke.
    """
    hypertension_with_stroke = []
    hypertension_without_stroke = []

    for patient_id, patient_info in clinical_dataset_record.items():
        try: 
            # Check if the patient has hypertension and stroke occurred
            hypertension = float(patient_info.get("hypertension", 0)) == 1
            stroke_occurrence = float(patient_info.get("stroke_occurrence", 0)) == 1
            # Process only if the patient has hypertension
            if hypertension:
                record = {"ID": patient_id}
                record.update(patient_info)
                if stroke_occurrence:  # group stroke status based on whether or not they had hypertension
                    record["Group"] = "Hypertension With Stroke"
                    hypertension_with_stroke.append(record)
                else:
                    record["Group"] = "Hypertension Without Stroke"
                    hypertension_without_stroke.append(record)

        except (TypeError, ValueError) as e:  #  handles the conversion error
            print(f"Skipping record due to conversion error: {e} in patient_info: {patient_info}")
            continue


    results_viii = hypertension_with_stroke + hypertension_without_stroke  # merge the results into a list to  display them easilu
    save_and_export_to_csv(results_viii, "hypertension_and_stroke_results.csv")

    return results_viii




def heart_disease_with_stroke(clinical_dataset_record):
    """ This is a function that returns anyone whose heart disease resulted in stroke."""
    patient = []

    for patient_id, patient_info in clinical_dataset_record.items():
        try: 
            # Check if the patient has heart disease and stroke occurred
            heart_disease = float(patient_info.get("heart_disease", 0)) == 1
            stroke_occurrence = float(patient_info.get("stroke_occurrence", 0)) == 1

            if heart_disease and stroke_occurrence: # if both conditions are true, add to the list
                record = {"ID": patient_id}
                # Add all other patient information to the record
                record.update(patient_info)
                patient.append(record)
        except (TypeError, ValueError) as e: # Failure to convert or missing data
             print(f"Skipping record {patient_id} due to data conversion error: {e}")
             continue

    results_ix = patient
    save_and_export_to_csv(results_ix, "heart_disease_with_stroke.csv")
    return results_ix



descriptive_columns = {"age", "average_glucose_level", "bmi", "sleep_hours"}

def descriptive_analysis(clinical_dataset_record, feature=None):
    """ Stats function that returns the descriptive statistics of any of the features of the dataset. """
    if feature is None:
        print(f"List of available features: {descriptive_columns}")
        feature = input("Which feature do you want to analyze? ").strip().lower()
        
    # Checks if the feature selected is among the available features
    if feature not in descriptive_columns:
        return {f"Please select a feature among the ones given {sorted(descriptive_columns)}"}

    values = []

    for patient_id, patient_info in clinical_dataset_record.items():
        value = patient_info.get(feature)
        try:
            value = float(value)
            values.append(value)
        except (TypeError, ValueError) as e:
            print(f"Skipping record due to an error: {e} in patient_info: {patient_info}")
            continue

    if not values:
        return {"error": f"No numeric values were found for the {feature} feature"}

    # Calculate the descriptive statistics
    mean_value = mean(values)
    std_dev_value = std_dev(values)
    minimum = min(values)
    maximum = max(values)
    percentiles = percentiless(values)
    count = len(values)

    statistics = {
        "Feature": feature,
        "Count": count,
        "Mean": mean_value,
        "Standard Dev": std_dev_value,
        "Min": minimum,
        "Max": maximum,
        **percentiles
    }
    results_x = statistics
    save_feature = feature.replace(" ", "_")
    filename = f"{save_feature}_descriptive_analysis.csv"
    save_and_export_to_csv(results_x, filename)
    return results_x



def average_sleep_hours_stroke(clinical_dataset_record):
    """
    Stats function to get the average sleep hours of those who had stroke and those who didn't
    """
    stroke_sleep_hours = []  # patients who had stroke
    no_stroke_sleep_hours = []  # patients who did not have stroke

    for patient_id, patient_info in clinical_dataset_record.items():
        try:
            stroke_occurence = float(patient_info.get('stroke_occurrence')) == 1
            sleep_hours = float(patient_info.get('sleep_hours'))

            if stroke_occurence: # if patient had a stroke, add their age to the first list
                stroke_sleep_hours.append(sleep_hours)
            else:  # if they didn't , add their age to the second list
                no_stroke_sleep_hours.append(sleep_hours)

        except (TypeError, ValueError) as e:  #  handles the conversion error
            print(f"Skipping record due to an error: {e} in patient_info: {patient_info}")
            continue

    if stroke_sleep_hours:
        avg_sleep_stroke = mean(stroke_sleep_hours)
    else:
        avg_sleep_stroke = 0

    if no_stroke_sleep_hours:
        avg_sleep_no_stroke = mean(no_stroke_sleep_hours)
    else:
        avg_sleep_no_stroke = 0

    results_xi = {
        "Average hours with stroke": avg_sleep_stroke,
        "Average hours without stroke": avg_sleep_no_stroke,
        "Stroke Count": len(stroke_sleep_hours),
        "No stroke count": len(no_stroke_sleep_hours)
    }

    save_and_export_to_csv(results_xi, "average_sleep_hours_stroke.csv")

    return results_xi
