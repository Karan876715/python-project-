# 1 Student - 5 variables 
student1_name = "karan"
student1_marks = 85
student_roll_number = 101
student_subject = "java"
student_city = "Hingoli"


#List
students = ("kartik","karan","kunal","krushna")
marks = [85,92,78,65]
roll_numbers = [101, 102, 103, 104]
subjects = ["java","python","c++","javascript"]
cities =["Hingoli", "Pune", "Mumbai", "Nagpur"]

#get roll number of kartik
#rolls[0] 

student = {
    "name": "karan",
    "marks": 92,
    "roll_number": 102,
    "subject": "python",
    "city": "pune"

}

#Accessing values from  dictionary
print(student["name"])
print(student["marks"])
print(student["roll_number"])
print(student["subject"])
print(student["city"])

#Update values in dictionary
student["marks"] = 90
print(student["marks"]) 

#new field
student ["grade"] = "A"
print(student["grade"])

#check 
print("name" in student)
print ("age" in student )

# keys and values
print(student.keys())
print(student.values())