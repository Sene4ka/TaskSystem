import json
name = "Информатика. Количество цветов в изображении n*m пикселей размером k КБайт"
txt = "Изображение размером {} на {} пикселей занимает в памяти {} {}байт (без учёта сжатия). Найдите максимально возможное количество цветов в палитре изображения."
sol = "Найдем количество пикселей в изображении: {} * {} = {} пикселей\nНайдем вес изображения: {} = {} бит\nНайдем количество бит информации на пиксель: {} / {} = {} бит на пиксель\nНайдем количесво цветов: 2 ** {} = {} цветов"
data = {}
c = 1
lt = "K"
for i in range(2, 12):
    for j in range(2, 11):
        for k in range(2, 257):
            p = (2 ** i) * (2 ** j)
            vk = k * 1024 * 8
            if 2 ** int(vk / p) <= 65536 and len(str(vk / p).split(".")[1]) <= 3:
                lt = "K"
                data[str(c).rjust(8, "0")] = (str(2 ** i), str(2 ** j), str(k), lt), (str(2 ** i), str(2 ** j), str(p), f"{k} * 1024 * 8", str(vk), str(vk), str(p), str(vk / p), str(int(vk / p)), str(2 ** int(vk / p))), str(2 ** int(vk / p))
                c += 1
                print(sol.format(str(2 ** i), str(2 ** j), str(p), f"{k} * 1024 * 8", str(vk), str(vk), str(p), str(vk / p), str(int(vk / p)), str(2 ** int(vk / p))))
with open("00000004.json", "w+") as f:
    json.dump(data, f)
print(c)
