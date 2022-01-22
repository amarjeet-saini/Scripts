import sys
file_name = sys.argv[1]
engine_no = sys.argv[2]
model = sys.argv[3]

if not(int(engine_no)>=1 and int(engine_no) <=5):
    print("invalid eng no")
    sys.exit(2)

out_name = "accuracy_result-" + str(engine_no) + "_" + model + ".txt"


count = 0
TOTAL = int(sys.argv[4])

try:
    with open(file_name,"r") as input_file, open(out_name,"w") as opf:
        for line in input_file:
            actual = line[:9]
            predict = line[10:-1]
            result = str(actual==predict)+"\n"
            opf.write(result)
            if actual == predict:
                count += 1
except:
    print("file error")

print(count)
print(count/TOTAL)
