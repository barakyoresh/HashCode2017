f = open("kittens.in")
data = f.readlines()

numbers = data[0].split(" ")

v = int(numbers[0])
e = int(numbers[1])
r = int(numbers[2])
c = int(numbers[3])
x = int(numbers[4])

print numbers

# for line in data:
#     print line