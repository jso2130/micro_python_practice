def make_speedup(count, start, step):
    result = []
    for i in range(count):
        result.append(start - i * step)
    return result

fast = make_speedup(6,600,100)
print(fast)