first_num = int(input('Введите первое число: '))
second_num = int(input('Введите второе число: '))
fibonachi_to_second = []
fibonachi_to_second.append(0)
fibonachi_to_second.append(1)
last_nums_sum = 0
while last_nums_sum<=second_num:
    last_nums_sum = fibonachi_to_second[(len(fibonachi_to_second)-1)] + fibonachi_to_second[(len(fibonachi_to_second)-2)]
    if last_nums_sum <= second_num:
        fibonachi_to_second.append(last_nums_sum)
fibonachi = []
for i in fibonachi_to_second:
    if (i>=first_num) and (i<=second_num):
        fibonachi.append(i)
if len(fibonachi)==0:
    print('В заданном диапазоне нет чисел Фибоначчи')
else:
    print(*fibonachi)