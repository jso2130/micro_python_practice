<<<<<<< Updated upstream
number = 7      # 나눠지는 값
size = 2        # 나눌 값
groups = 0      # 몫

print('시작: ', number)
while number >= size:
    number -= size
    groups += 1             # 나눌 값으로 한 번씩 빼면서 '몫'을 센다.
    print(number + size, '-', size, '=', number, '(', groups, '번째 )' )

print('더 못 뺀다:', number,'<', size)
print('몫(뺀 횟수) =', groups)
=======
number = 7      # 나눠지는 값
size = 2        # 나눌 값
groups = 0      # 몫

print('시작: ', number)
while number >= size:
    number -= size
    groups += 1             # 나눌 값으로 한 번씩 빼면서 '몫'을 센다.
    print(number + size, '-', size, '=', number, '(', groups, '번째 )' )

print('더 못 뺀다:', number,'<', size)
print('몫(뺀 횟수) =', groups)
>>>>>>> Stashed changes
print('나머지(남은 수) =', number)  # number에는 '나머지값'만 남는다.