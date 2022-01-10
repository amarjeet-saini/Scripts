import sys


file1 = sys.argv[1]
file2 = sys.argv[2]

posndot1 = file1.find(".")
posndot2 = file2.find(".")

outfile = "miss_engine" + file1[posndot1-1:posndot1] + file2[posndot2-1:posndot2] + ".txt"

count = 0
total = 0

with open(file1, 'r') as a, open(file1, 'r') as b, open(outfile, 'a+') as c:
    for line1,line2 in zip(a,b):
        line1 = line1[line1.find(" "):-1]
        line2 = line2[line2.find(" "):-1]
        if line1 != line2:
            print(line1)
            print(line2)
            count = count + 1
        total = total + 1

print(f"No of mis prediction : {count} out of {total}")


