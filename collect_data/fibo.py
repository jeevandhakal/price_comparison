n = int(input("Enter nth term for the series: "))
n1, n2 = 0, 1
count = 1

if n <= 0:
    print("Enter positive integer")
elif n == 1:
    print(n1)
else:
    while count <= n:
        print(n1)
        nth = n1 + n2 
        n1 = n2
        n2 = nth
        count += 1
