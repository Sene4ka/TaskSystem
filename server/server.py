import asyncio
import socket
import json
from random import choice

async def reciver(con):
    try:
        #while True:
        data = con.recv(1024)
        data_d = data.decode().split()
        print(0, data)
        if len(data_d) != 0:
            if "get_seed" in data_d:
                await get_seed(con, data_d)
            elif "get_name_by_number" in data_d:
                await get_name_by_number(con, data_d)
            elif "get_data" in data_d:
                await get_data(con, data_d)
                
    except Exception:
        print("Exception:", con)

async def get_seed(con, data):
    task_id, amount = data[1].split(":")
    seed_list = json.load(open(f"{task_id}.json"))
    if len(data) == 3:
        used_seeds = data[2].split(":")
        seeds = [i for i in list(seed_list.keys()) if i not in used_seeds]
    else:
        seeds = list(seed_list.keys())
    to_send = []
    for _ in range(int(amount)):
        seed = choice(seeds)
        st = seed_list[seed]
        st = f"{';'.join(st[0])}|{st[1]}"
        to_send.append(f"{seed}|{st}")
        del seeds[seeds.index(seed)]
    to_send = "$".join(to_send)
    con.sendall(to_send.encode())

async def  get_name_by_number(con, data):
    data_list = json.load(open("all_tasks.json"))
    to_send = []
    for i in data_list.keys():
        to_send.append(f"{i}|{data_list[i][0]}")
    to_send = "$".join(to_send)
    con.sendall(to_send.encode())
        
async def get_data(con, data):
    tasks = json.load(open("all_tasks.json"))
    data_s = tasks[data[1]]
    to_send = f"{'|'.join(data_s)}"
    con.sendall(to_send.encode())

soc = socket.socket()
soc.bind(("192.168.0.104", 4444))
soc.listen()
while True:
    con, adress = soc.accept()
    asyncio.run(reciver(con))
