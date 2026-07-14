import os
import json
import errno
import datetime
import argparse

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tasks.json")
work_statuses = {"todo","doing","done"}
with open(out_path, "r", encoding="utf-8") as f:
    tasks = json.loads(f.read().strip())

for task in tasks:
    print(f"任务ID：{task["id"]} , 任务状态：{task["status"]} , "
          f"任务内容：{task["description"]}")