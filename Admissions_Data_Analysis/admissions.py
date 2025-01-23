# Function given to check the row length of each entry
def check_row_types(row):
    if len(row) != 8:
        print("Length incorrect! (should be 8): " + str(row))
        return False
    ind = 0
    while ind < len(row):
        if type(row[ind]) != float:
            print("Type of element incorrect: " + str(row[ind]) + " which is " + str(type(row[ind])))
            return False
        ind += 1
    return True
	
# Start of my program:
def convert_row_type(row):
    converted_data = [float(entry) for entry in row]
    return converted_data

def calculate_score(student_qualifiers):
    return (((student_qualifiers[0] / 160) * 0.3) + ((student_qualifiers[1] * 2) * 0.4) + (student_qualifiers[2] * 0.1) + (student_qualifiers[3] * 0.2))

def is_outlier(student_qualifiers):
    if student_qualifiers[2] == 0 or ((student_qualifiers[1] * 2) - (student_qualifiers[0] /160)) > 2:
        return True
    else:
        return False

def calculate_score_improved(student_qualifiers):
    if calculate_score(student_qualifiers) > 6 or is_outlier(student_qualifiers):
        return True
    else:
        return False
    
def grade_outlier(student_grades):
    student_grades = student_grades.copy()
    student_grades.sort()
    difference = student_grades[1]-student_grades[0]
    if difference >= 20:
        return True
    else:
        return False
    
def grade_improvement(student_scores):
    sorted_scores = student_scores.copy()
    sorted_scores.sort()
    return student_scores == sorted_scores

# Another way I achieved the same result as the function above:
def grade_improvement_2(student_scores):
    for i in range(1, len(student_scores)):
        if student_scores[i] <= student_scores[i - 1]:
            return False
    return True
        
def main():
    filename = "admission_algorithms_dataset.csv"
    with open(filename, "r") as input_file: 

        print("Processing " + filename + "...")

        headers = input_file.readline()
        
        students = []
        student_qualifiers = []
        student_scores = []
        
        for line in input_file:

            rows = line.strip().split(",")
            students.append(rows.pop(0))
            converted_data = convert_row_type(rows)

            if not check_row_types(converted_data):
                print("Invalid row: " + str(rows))
            
            student_qualifiers.append(converted_data[0:4])
            student_scores.append(converted_data[4:8])


    with open("student_scores.csv", "w") as scores_output, open("chosen_students.csv", "w") as chosen_output:
        for i, qualifiers in enumerate(student_qualifiers):
            scores_output.write(f"{students[i].strip()}, {calculate_score(qualifiers):.2f}\n")
            if calculate_score(qualifiers) > 6:
                chosen_output.write(f"{students[i]}\n")
    
    with open("outliers.csv", "w") as outlier_output:
        for i, qualifiers in enumerate(student_qualifiers):
            if is_outlier(student_qualifiers[i]):
                outlier_output.write(f"{students[i]}\n")
    
    with open("chosen_improved.csv", "w") as improved_output:
        for i, qualifiers in enumerate(student_qualifiers):
            if is_outlier(qualifiers) and calculate_score(qualifiers) > 5 or calculate_score(qualifiers) > 6:
                improved_output.write(f"{students[i].strip()}\n")

    with open('better_improved.csv', "w") as better_output:
        for i, qualifiers in enumerate(student_qualifiers):
            if calculate_score_improved(qualifiers):
                better_output.write(f"{students[i].strip()}, {qualifiers[0]}, {qualifiers[1]}, {qualifiers[2]}, {qualifiers[3]}\n")

    with open('composite_chosen.csv', "w") as composite_chosen:
        for i, qualifiers in enumerate(student_qualifiers):
            if calculate_score(qualifiers) > 6 or calculate_score(qualifiers) > 5 and True in [is_outlier(qualifiers),grade_outlier(student_scores[i]), grade_improvement(student_scores[i])]:
                composite_chosen.write(f"{students[i]}\n")

    # Manually Testing Code Here
    # for i in range(len(student_qualifiers)):
    #     if grade_improvement(student_scores[i]):
    #         print(f"{students[i]} {student_scores[i]} index {i} score: {calculate_score(student_qualifiers[i])}, is_outlier: {is_outlier(student_qualifiers[i])}, grade_improvement: {grade_improvement(student_scores[i])}, grade_outlier:{grade_outlier(student_scores[i])}")
    print("done!")

# this bit allows us to both run the file as a program or load it as a
# module to just access the functions
if __name__ == "__main__":
    main()
