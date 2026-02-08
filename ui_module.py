# ui_module.py

from query_module import *

def display_menu():
    print("\n***********************Stroke Data Analytics Menu***********************")
    print("1. Average/Median/Modal age of smokers with hypertension and stroke")
    print("2. Average/Median/Modal age & glucose level of patients with heart disease and stroke")
    print("3. Age analysis based on gender and hypertension (stroke vs no stroke)")
    print("4. Smoking habit vs stroke age analysis")
    print("5. Urban vs Rural stroke age analysis")
    print("6. Dietary habits of stroke vs non-stroke patients")
    print("7. Patients with hypertension that led to stroke")
    print("8. Patients by hypertension-stroke status")
    print("9. Heart disease with stroke")
    print("10. Descriptive stats of any feature")
    print("11. Average sleep hours (stroke vs non-stroke)")
    print("0. Exit")
    print("----------------------------------")

def run_ui(data):
    valid_options = [str(i) for i in range(12)]
    
    while True:
        display_menu()
        option = input("Enter the option you wish to analyze: ").strip()
        
        if option not in valid_options:
            print(" Please select among the available options")
            continue
        if option == "0":
            print("Thanks for using the system")
            break

        if option == "1":
            smokers_hypertension_stroke(data)
        elif option == "2":
            heart_disease_stroke(data)
        elif option == "3":
            hypertension_stroke_by_gender(data)
        elif option == "4":
            smokers_stroke_results(data)
        elif option == "5":
            area_lived_stroke(data)
        elif option == "6":
            dietary_habits_stroke(data)
        elif option == "7":
            hypertension_stroke_patients(data)
        elif option == "8":
            hypertension_and_stroke_results(data)
        elif option == "9":
            heart_disease_with_stroke(data)
        elif option == "10":
            descriptive_analysis(data)
        elif option == "11":
            average_sleep_hours_stroke(data)

        while True:
            choice = input("\n Do you want to continue? (Yes or No): ").strip().lower()
            if choice == "yes":
                break  # Display the menu
            elif choice == "no":
                print("Thanks for using the system")
                return
            else:
                print("Please enter a valid choice")