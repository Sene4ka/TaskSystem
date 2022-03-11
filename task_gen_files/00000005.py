import json
txt = "Найдем количество бит информации на пиксель у первого и второго файлов:\n1){} = 2 ** {} -> {} бит на пиксель\n2){} = 2 ** {} -> {} бит на пиксель\nТогда их объемы будут равны:\nV1 = k * {};V2 = k * {}, где k - количество пикселей в изображении\nПо условию V2 = V1 {} {} -> {} * k - {} * k = {} * 1024 * 8;\n{} * k = {} * 1024 * 8;\nk = {}\nТогда V1 = {} * {} = {}"
data = {}
lt1 = "уменьшился"
lt2 = "-"
c = 1
for i in range(1, 13):
    for j in range(1, 13):
        for k in range(2, 256):
            if i > j:
                lt1 = "уменьшился"
                lt2 = "-"
                ans = (7 * 1024 * 8) / abs(i - j) * i / (1024 * 8)
                if int(ans) == ans:
                    data[str(c).rjust(8, "0")] = (str(2 ** i), str(2 ** j), lt1, str(k)), (str(2 ** i), str(i), str(i), str(2 ** j), str(j), str(j), str(i), str(j), lt2, str(k), str(i), str(j), str(k), str(abs(i - j)), str(k), str(k * 1024 * 8 / abs(i - j)), str(i), str(k * 1024 * 8 / abs(i - j)), str(int(ans))), str(int(ans))
                    c += 1
            elif j > i:
                lt1 = "увеличился"
                lt2 = "+"
                ans = (7 * 1024 * 8) / abs(i - j) * i / (1024 * 8)
                if int(ans) == ans:
                    data[str(c).rjust(8, "0")] = (str(2 ** i), str(2 ** j), lt1, str(k)), (str(2 ** i), str(i), str(i), str(2 ** j), str(j), str(j), str(i), str(j), lt2, str(k), str(j), str(i), str(k), str(abs(i - j)), str(k), str(k * 1024 * 8 / abs(i - j)), str(i), str(k * 1024 * 8 / abs(i - j)), str(int(ans))), str(int(ans))
                    c += 1
print(c)
with open("00000005.json", "w+") as f:
    json.dump(data, f)