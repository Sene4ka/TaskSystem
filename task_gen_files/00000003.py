import json
data = {}
c = 1
strf = "Найдем количество пикселей: {} * {} = {} пикселей\nНайдем количество бит информации на пиксель: {} цветов =  2 ^ {} цветов -> {} бит на пиксель\nНайдем вес изображения в битах: {} * {} = {} бит\nПереведем размер изображения в {}Байты: {} = {} {}Байт -> Зарезервировать нужно {} {}Байт"
lt = "K"
ans = 0
for i in range(2, 13):
    for j in range(2, 12):
        for k in range(1, 10):
            v = 2 ** i * 2 ** j * k
            if v <= 1024 * 8:
                pass
            elif v / (1024 * 8) < 1024:
                lt = "K"
                ans = v / (1024 * 8)
                if int(ans) != ans:
                    tans = int(ans) + 1
                else:
                    tans = int(ans)
                data[str(c).rjust(8, "0")] = (lt, str(2 ** i), str(2 ** j), str(2 ** k)), (str(2 ** i), str(2 ** j), str(2 ** (i + j)), str(2 ** k), str(k), str(k), str(v / k), str(k), str(v), lt, f"{v} / (1024 * 8)", str(ans), lt, str(tans), lt), str(tans)
                c += 1
            elif v / (1024 * 8) > 1024:
                lt = "M"
                ans = v / (1024 * 1024 * 8)
                if int(ans) != ans:
                    tans = int(ans) + 1
                else:
                    tans = int(ans)
                data[str(c).rjust(8, "0")] = (lt, str(2 ** i), str(2 ** j), str(2 ** k)), (str(2 ** i), str(2 ** j), str(2 ** (i + j)), str(2 ** k), str(k), str(k), str(v / k), str(k), str(v), lt, f"{v} / (1024 * 1024 * 8)", str(ans), lt, str(tans), lt), str(tans)
with open("00000003.json", "w+") as f:
    json.dump(data, f)
print(c)