s1 = int(input("Enter marks of subject 1:"))
s2 = int(input("Enter marks of subject 2:"))
s3 = int(input("Enter marks of subject 3:"))

total = s1 + s2 + s3
percentage = (total/300)*100

print("total marks:",total)
print("percentage:",percentage)
if percentage >=90:
    print("grade:A")
elif percentage >=80:
    print("grade:B")
elif percentage >=70:
    print("grade:C")
elif percentage >=60:
    print("grade:D")
else:
    print("grade:F")
    