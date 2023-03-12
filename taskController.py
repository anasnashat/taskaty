from datetime import datetime
from argparse import Namespace
from .Task import Task
from datetime import  date
from tabulate import tabulate


class TaskController:
    def __init__(self, file_name):
        self.file_name = file_name

    def add_task(self, args):

        if not args.start_date:
            now = date.today().isoformat()
            args.start_date = now
        task = Task(args.title, args.description, args.start_date, args.end_date, args.done)
        with open(self.file_name, 'a') as f:
            f.write(f"{task}\n")

    def list_tasks(self):
        unfinished_tasks = []
        with open(self.file_name, 'r') as f:
            for lin in f:
                if lin != '\n':
                    title, description, start_date, end_date, done = lin.split(', ')
                    end_date = None if end_date == 'None' else end_date
                    done = False if done.strip('\n') == 'False' else done
                    if done:
                        continue
                    unfinished_tasks.append(
                        {'title': title, "description": description, "start_date": start_date, "end_date": end_date})
        return unfinished_tasks

    def list_all_task(self):
        all_tasks = []
        with open(self.file_name, 'r') as f:
            for lin in f:
                if lin != '\n':
                    title, description, start_date, end_date, done = lin.split(', ')
                    end_date = None if end_date == 'None' else end_date
                    done = False if done.strip('\n') == "False" else done
                    all_tasks.append(
                        {'title': title, "description": description, "start_date": start_date, "end_date": end_date,
                         "done": done})
        return all_tasks

    def due_date(self, start, end):
        start_date = datetime.strptime(start, "%Y-%m-%d")
        end_date = datetime.strptime(end, "%Y-%m-%d")
        date_delta = end_date - start_date
        return f'{date_delta} days left.'

    def print_table(self, tasks):
        formatted_tasks = []
        try:
            for number, task in enumerate(tasks, 1):
                if task['start_date'] and task['end_date']:
                    due_date = self.due_date(task['start_date'], task['end_date'])
                else:
                    due_date = 'Open'
                formatted_tasks.append({'id': number, **task, 'due_date': due_date})
            print(tabulate(formatted_tasks, headers="keys", tablefmt="grid"))
        except Exception as e:
            with open(self.file_name, 'w') as f:
                f.write('')
                for lin in formatted_tasks:
                    if lin == '\n':
                        formatted_tasks.remove(lin)
                f.write(f"{formatted_tasks}\n")

    def display(self, args):
        all_tasks = self.list_all_task()
        unshacked_tasks = self.list_tasks()
        if not all_tasks:
            print("There is no tasks to add .")
            return
        if args.all:
            self.print_table(all_tasks)

        else:
            if unshacked_tasks:
                self.print_table(unshacked_tasks)
            else:
                print('All tasks are checked')

    def remove(self, args):
        tasks = self.list_all_task()
        if args.remove:
            index = args.remove
        else:
            index = len(tasks) - 1
        if index <= 0 or index > len(tasks):
            print(f"no task withe this number {index}")
            return
        tasks.pop(index - 1)
        with open(self.file_name, 'w') as f:
            for task in tasks:
                self.add_task(Namespace(**task))

    def check_task(self, args):
        index = args.task
        print(index)
        tasks = self.list_all_task()
        if index <= 0 or index > len(tasks):
            print(f"no task withe this number {index}")
            return
        tasks[index - 1]['done'] = True
        with open(self.file_name, 'w') as f:
            for task in tasks:
                self.add_task(Namespace(**task))





    def reset_all_tasks(self, *args):
        with open(self.file_name, 'w') as f:
            f.write('')
        print('All tasks are reset')
