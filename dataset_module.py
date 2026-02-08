numeric_columns = {"id","age","hypertension","heart_disease","ever_married","average_glucose_level", "bmi","alcohol_consumption","chronic_stress","sleep_hours","family_history_of_stroke","stroke_risk_score","stroke_occurrence"} # Defines the columns whose content should be treated as numeric values

def load_stroke_clinical_dataset_record(filename="data.csv") -> dict:
	""" Load patients record into a nested dictionary
	"""
	clinical_dataset_record = {}  # To store the patients' data
	
	
	try:
		with open(filename, "r") as f:
			# Converts each column name to lowercase and replace empty space with underscore
			header_line = f.readline()
			header = [col.strip().lower().replace(" ", "_").strip('"').strip("'") for col in header_line.strip().split(",")]
			
			for line_number, line in enumerate(f, start=2):  # Start counting after header
				if not line.strip():
					continue  # Skips empty lines
				
				values = line.strip().split(",")
				
				# Skip rows tnat do not match the number of columns
				if len(values) != len(header):
					print(f"Row {line_number} skipped due to mismatched column count")
					continue
				
				# Get the first value which is patient ID
				patient_id = values[0].strip()  
				
				
				patient_info = {}  
				for i in range(1, len(header)):
					col_name = header[i]
					value = values[i].strip()
					
					# Check if the column can should be stored as a number and proceeds by converting it into a float
					if col_name in numeric_columns:
						try:
							patient_info[col_name] = float(value)
						except ValueError:
							print(f"Warning: Non-numeric value '{value}' in numeric column '{col_name}' on line {line_number}")
							patient_info[col_name] = None
					else:
						patient_info[col_name] = value
				
				# Store the record
				clinical_dataset_record[patient_id] = patient_info
				
	except FileNotFoundError:
		# If the file is not found
		print("Error: File not found:", filename)
	except Exception as e:
		# Handles all other unexpected errors
		print("An unexpected error occurred:", e)
		
	return clinical_dataset_record
