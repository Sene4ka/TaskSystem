# "Значение арифметического выражения: {}^{} {} {}^{} записали в системе счисления с основанием {}. Сколько цифр «{}» в этой записи?"
import json

def to_Xn(x, n):
    c = x
    s = ""
    smb = "0123456789ABCDEF"
    while c >= n:
        s = smb[c % n] + s
        c //= n
    s = smb[c % n] + s
    return s

data = {}
c = 1
smb = "0123456789ABCDEF"
f = False
ss = [2, 4, 6, 8, 10, 16]
for s in ss:
    for n1 in range(20, 31):
        for s1 in range(10, 16):
            for n2 in range(5, 10):
                for s2 in range(20,26):
                    for i in range(s):
                        v1 = (n1 ** s1) + (n2 ** s2)
                        v2 = (n1 ** s1) - (n2 ** s2)
                        #print(c, v1, v2)
                        if 10 <= len(str(v1)) <= 50:
                            if to_Xn(v1, s).count(smb[i]) < 100:
                                data[str(c).rjust(8, "0")] = (n1, s1, "+", n2, s2, s, i), to_Xn(v1, s).count(smb[i])
                                c += 1
                                print(c)
                        if v2 >= 0 and 10 <= len(str(v2)) <= 50:
                            if to_Xn(v2, s).count(smb[i]) < 100:
                                data[str(c).rjust(8, "0")] = (n1, s1, "-", n2, s2, s, i), to_Xn(v2, s).count(smb[i])
                                c += 1
                                print(c)
with open("00000002.json", "w+") as f:
    json.dump(data, f)

