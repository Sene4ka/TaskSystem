import asyncio
import socket
import json
from random import choice

async def reciver(con):
    try:
        #while True:
        data = con.recv(1024)
        data_d = data.decode()
        print(0, data)
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
    except ConnectionResetError:
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
        print(st)
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
        print(data)
        data_n = [":".join(j) for j in data[:2]]
        data_n.append(data[2])
        to_send.append(";".join(data_n))
    print(to_send)
    con.sendall("|".join(to_send).encode())
        
        
    
    
    

    

soc = socket.socket()
soc.bind(("192.168.0.104", 4444))
soc.listen()
while True:
    con, adress = soc.accept()
    asyncio.run(reciver(con))
