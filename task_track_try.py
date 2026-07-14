import os
import json
import errno
import datetime
import argparse



out_path = os.path.join(os.getcwd(), 'tasks_try.json')
work_statuses = {"todo", "doing", "done"}


def load_file():
    if not os.path.exists(out_path):
        return []
    try:
        with open(out_path, "r", encoding="utf-8") as f:
            tasks = json.loads(f.read().strip())
            if not tasks:
                return []
            return tasks
    except json.JSONDecodeError as j:
        print(f"错误：json文件格式有误{j}")
        return []
    except OSError as e:
        if e.errno == errno.ENOSPC:
            print("磁盘空间不足，无法完成写入操作")
        elif e.errno == errno.ENOSPC:
            print("磁盘空间不足")
        else:
            print(f"文件操作失败：{e.strerror}")
        return []


def save_file(tasks):
    try:
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(tasks,f, ensure_ascii=False, indent=4)
    except OSError as e:
        print(f"错误：文件保存失败{e}")


def next_file(tasks):
    if not tasks:
        return 1
    return max(t["id"] for t in tasks) + 1


"""def remove_task(tasks):
    if not tasks:
        return []
    try:
        with open(out_path , "w", encoding="utf-8") as f:"
"""


def find_file(task_id, tasks):
    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            return i, task
    return None, None


#功能实现层


def add_task(description):
    tasks = load_file()
    now_time = datetime.datetime.now().isoformat(timespec="seconds")
    task = {
        "id": next_file(tasks),
        "description": description,
        "status": "todo",
        "created_on": now_time,
        "updated_on": now_time,
    }
    tasks.append(task)
    save_file(tasks)
    print(f"任务创建成功 +=+ ：id:{task['id']}, description:{task['description']}")


def delete_task(task_id = None , del_all = False):
    tasks = load_file()
    index, task = find_file(task_id, tasks)
    if del_all:
        count = len(tasks)
        if count == 0:
            print("任务列表已为空")
            return
        tasks.clear()
        save_file(tasks)
        print(f"任务列表清空完毕，共删除{count}个任务!")
        return
    if task is None:
        print(f"错误：未找到该ID为{task_id}文件")
        return
    tasks.pop(index)
    save_file(tasks)
    print(f"删除成功：，已删除id为{task_id},description为：{task}的文件")
    return


def update_task(task_id, description):
    tasks = load_file()
    index, task = find_file(task_id, tasks)
    if task is None:
        print(f"错误：未找到该ID为{task_id}文件")
        return
    task["description"] = description
    task["updated_on"] = datetime.datetime.now().isoformat(timespec="seconds")
    save_file(tasks)


def mark_task(task_id, status):
    tasks = load_file()
    index, task = find_file(task_id, tasks)
    if task is None:
        print(f"错误：未找到该ID为{task_id}文件")
        return
    task["status"] = status
    task["updated_on"] = datetime.datetime.now().isoformat(timespec="seconds")
    save_file(tasks)
    print(f"任务{task_id} ， 已标记:{task["status"]} ，更新时间：{task["updated_on"]}")


def list_tasks(status=None):
    tasks = load_file()
    if status:
        tasks = [t for t in tasks if t["status"] == status]
    if not tasks:
        print("暂无任务")
        return
    print(f"{'ID':<5} {'状态':<10} {'描述':<40} {'创建时间':<22} {'更新时间':<22}")
    print("─" * 105)

    status_label = {"todo": "🔵 待办", "doing": "🟡 进行中", "done": "✅ 已完成"}
    for t in tasks:
        status = status_label.get(t["status"], t["status"])
        description = t["description"]
        if len(description) > 40:
            description = description[:37] + "..."
        if status == "🔵 待办":
            print(f"{t['id']:<5} {status:<10}  {description:<40} {t['created_on']:<22} {t['updated_on']:<22}")
        else:
            print(f"{t['id']:<5} {status:<10} {description:<40} {t['created_on']:<22} {t['updated_on']:<22}")

    print(f"\n共 {len(tasks)} 个任务")


#——————————————cli层————————————
def build_parser():
    parser = argparse.ArgumentParser(
        description="任务追踪器————cli",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""示例:
  python task_tracker.py add "学习 Python"
  python task_tracker.py update 1 "深入学习 Python"
  python task_tracker.py todo 1
  python task_tracker.py done 1
  python task_tracker.py list
  python task_tracker.py list todo
  python task_tracker.py delete 1
        """,
    )

    sub = parser.add_subparsers(dest="command", help="可用命令")

    add_p = sub.add_parser("add", help="添加任务")
    add_p.add_argument("description")

    update_parser = sub.add_parser("update", help="更新任务描述")
    update_parser.add_argument("id", type=int,help="任务ID")
    update_parser.add_argument("description", help="新的任务描述")

    delete_parser = sub.add_parser("delete", help="删除任务")
    delete_parser.add_argument("id", type=int,nargs="?",help="ID")
    delete_parser.add_argument("--all", action="store_true" ,help = "all删除所有任务")

    todo_p = sub.add_parser("todo", help="标记任务为待办")
    todo_p.add_argument("id", type=int,help="任务 ID")

    doing_p  = sub.add_parser("doing", help="标记任务为进行中")
    doing_p.add_argument("id", type=int,help="任务 ID")

    done_p = sub.add_parser("done", help="标记任务为已完成")
    done_p.add_argument("id",type=int,  help="任务 ID")

    list_parser = sub.add_parser("list", help="列出任务")
    list_parser.add_argument(
        "status",
        nargs="?",
        choices=["todo", "doing", "done"],
        default=None,
        help="按状态过滤",
    )

    return parser

def main():
    p = build_parser()
    arg = p.parse_args()

    if arg.command == "add":
        add_task(arg.description)
    elif arg.command == "update":
        update_task(arg.id, arg.description)
    elif arg.command == "delete":
        if arg.all:
            delete_task(None, del_all =True)
        else:
            delete_task(arg.id)
    elif arg.command == "todo":
        mark_task(arg.id, "todo")
    elif arg.command == "doing":
        mark_task(arg.id, "doing")
    elif arg.command == "done":
        mark_task(arg.id, "done")
    elif arg.command == "list":
        list_tasks(arg.status)

if __name__ == "__main__":
    main()
