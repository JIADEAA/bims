def count_numbers(T, test_cases):
    for i in range(T):
        L, R, X, Y = test_cases[i]
        count = 0
        Y_bits = [b == '1' for b in bin(Y)[2:].zfill(30)]
        for N in range(2**30):
            if bin(N).count('1') >= L and bin(N).count('1') <= R and N & X == X:
                if all((N | (1 << i)) & (1 << i) == (1 << i) for i, b in enumerate(Y_bits) if b):
                    count += 1
        print(count)

# 读取输入的测试数据
T = int(input())
test_cases = []
for _ in range(T):
    L, R, X, Y = map(int, input().split())
    test_cases.append((L, R, X, Y))

# 调用函数计算并输出答案
count_numbers(T, test_cases)
