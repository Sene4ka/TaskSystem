import asyncio
import socket
import json
import datetime
from random import choice

async def reciver(con):
    try:
        #while True:
        data = con.recv(1024)
        data_d = data.decode()
        print(data)
        if len(data_d) != 0:
            if "get_seed" == data_d.split()[0]:
                await get_seed(con, data_d.split())
            elif "get_name_by_number" == data_d.split()[0]:
                await get_name_by_number(con, data_d.split())
            elif "get_data" == data_d.split()[0]:
                await get_data(con, data_d.split())
            elif "save_data" == data_d.split("||")[0]:
                await save_data(con, data_d.split("||"))
            elif "get_saved_tl_names" == data_d.split()[0]:
                await get_saved_tl_names(con, data_d.split()[1])
            elif "get_saved_tl_data" == data_d.split("|")[0]:
                await get_saved_tl_data(con, data_d.split("|")[1])
            elif "get_task_data_from_seeds" == data_d.split()[0]:
                await get_task_data_from_seeds(con, data_d.split()[1])
            elif "give_task" == data_d.split()[0]:
                await give_task(con, data_d.split())
            elif "get_user_tasks_names" == data_d.split()[0]:
                await get_user_tasks_names(con, data_d.split()[1])
            elif "get_teacher_task_by_name" == data_d.split()[0]:
                await get_teacher_task_by_name(con, data_d.split()[1])
            elif "system_login" == data_d.split(" ")[0]:
                await system_login(con, data_d.split(" ")[1])
            elif "delete_task" == data_d.split(" ")[0]:
                await delete_task(con, data_d.split(" ")[1])
    except Exception:
        print("Exception:", con)

async def get_seed(con, data):
    task_id, amount = data[1].split(":")
    seed_list = json.load(open(f"json_data/{task_id}.json"))
    if len(data) == 3:
        used_seeds = data[2].split(":")
        seeds = [i for i in list(seed_list.keys()) if i not in used_seeds]
    else:
        seeds = list(seed_list.keys())
    to_send = []
    for _ in range(int(amount)):
        seed = choice(seeds)
        st = seed_list[seed]
        st = f"{';'.join(st[0])}|{';'.join(st[1])}|{st[2]}"
        to_send.append(f"{seed}|{st}")
        del seeds[seeds.index(seed)]
    to_send = "$".join(to_send)
    con.sendall(to_send.encode())

async def get_name_by_number(con, data):
    data_list = json.load(open("json_data/all_tasks.json"))
    to_send = []
    for i in data_list.keys():
        to_send.append(f"{i}|{data_list[i][0]}")
    to_send = "$".join(to_send)
    con.sendall(to_send.encode())
        
async def get_data(con, data):
    tasks = json.load(open("json_data/all_tasks.json"))
    data_s = tasks[data[1]]
    to_send = f"{'|'.join(data_s)}"
    con.sendall(to_send.encode())

async def give_task(con, data):
    date = datetime.datetime.now()
    date = date.strftime("%m/%d/%Y_%H:%M")
    name = f"Задание_от_{date}"
    tasks = json.load(open("json_data/gived_tasks.json"))
    if data[1] not in tasks:
        tasks[data[1]] = []
    tasks[data[1]].append([name, data[2]])
    json.dump(tasks, open("json_data/gived_tasks.json", "w"))

async def delete_task(con, data):
    uid, name = data.split("|")
    tasks = json.load(open("json_data/gived_tasks.json"))
    for i in range(len(tasks[uid])):
        if tasks[uid][i][0] == name:
            del tasks[uid][i]
            break
    json.dump(tasks, open("json_data/gived_tasks.json", "w"))

async def save_data(con, data):
    data_l = json.load(open("json_data/saved_tasks.json"))
    dt = data[2].split("&")
    #dt = dt[1].split("|")
    #sl = {}
    #for i in dt:
        #dti = i.split(";")
        #tid = dti[0]
        #dti = dti[1:]
        #sp = []
        #for j in dti:
            #sp.append([*j.split(":")])
        #sl[tid] = sp
    if data[1] in data_l:
        data_l[data[1]].append(dt)
    else:
        data_l[data[1]] = [dt]
    if len(data_l[data[1]]) == 21:
        del data_l[data[1]][-1]
    with open("json_data/saved_tasks.json", "w+") as f:
        json.dump(data_l, f)

async def get_saved_tl_names(con, data):
    data_l = json.load(open("json_data/saved_tasks.json"))
    if data in data_l.keys():
        dt = data_l[data]
        to_send = []
        for i in dt:
            to_send.append(f"{i[0]}|{i[2]}|{i[3]}")
        to_send = "&".join(to_send)
        con.sendall(to_send.encode())
    else:
        con.sendall("NothingFound".encode())

async def get_saved_tl_data(con, data):
    uid, index = data.split("&")
    index = int(index)
    s = False
    data_l = json.load(open("json_data/saved_tasks.json"))
    if index < len(data_l[uid]):
        con.sendall(data_l[uid][index][1].encode())
    else:
        con.sendall("NothingFound".encode())

async def get_task_data_from_seeds(con, data):
    tid, seeds = data.split("|")
    seed_list = json.load(open(f"json_data/{tid}.json"))
    seeds = seeds.split(";")
    to_send = []
    for i in seeds:
        data = seed_list[i]
        #print(data)
        data_n = [":".join(j) for j in data[:2]]
        data_n.append(data[2])
        to_send.append(";".join(data_n))
    #print(to_send)
    con.sendall("|".join(to_send).encode())

async def get_teacher_task_by_name(con, data):
    uid, name = data.split("|")
    tasks = json.load(open("json_data/gived_tasks.json"))
    to_send = ""
    for i in tasks[uid]:
        if i[0] == name:
            to_send = i[1]
            break
    con.sendall(to_send.encode())

async def get_user_tasks_names(con, uid):
    tasks = json.load(open("json_data/gived_tasks.json"))
    if uid in tasks.keys():
        to_send = []
        print(tasks[uid])
        tasks_k = tasks[uid]
        for i in tasks_k:
            to_send.append(i[0])
        if len(to_send) != 0:
            con.sendall("|".join(to_send).encode())
        else:
            con.sendall("nothing_found".encode())
    else:
        con.sendall("nothing_found".encode())
           
async def system_login(con, encoded_data):
    #print(encoded_data)
    encoded_login, encoded_password = encoded_data.split("|")
    soc = socket.socket()
    soc.connect(("alexavr.ru", 25555))
    soc.sendall(f"com://connect {encoded_login}&&{encoded_password}".encode())
    result = soc.recv(1024).decode()
    name = soc.recv(1024).decode().split()
    soc.close()
    con.sendall(f"{result}|{name[2]}|{name[1]}".encode())
    #print(f"{result}|{name[2]}|{name[1]}")

uid = "sene4ka.abrosimov@yandex.ru"
data = "00000001:1|00000002:1|00000003:1|00000004:1|00000005:1"
date = datetime.datetime.now()
date = date.strftime("%m/%d/%Y_%H:%M")
name = f"Задание_от_{date}"
tasks = json.load(open("json_data/gived_tasks.json"))
if data[1] not in tasks:
    tasks[uid] = []
if len(tasks[uid]) == 0:
    tasks[uid].append([name, data])
json.dump(tasks, open("json_data/gived_tasks.json", "w"))
sp = []
soc = socket.socket()
soc.bind(("192.168.0.104", 4444))
soc.listen()
while True:
    con, adress = soc.accept()
    asyncio.run(reciver(con))
