from argparse import ArgumentParser
from .taskController import TaskController


def main():
    controller = TaskController('tasks.txt')
    parser = ArgumentParser(description='Simple CLI to mange tasks')
    subparser = parser.add_subparsers()
    add_task = subparser.add_parser('add', help='Add a task')
    add_task.add_argument('title', help='Title of the task', type=str)
    add_task.add_argument('-d', '--description', help='Description of the task', type=str, default=None)
    add_task.add_argument('-s', '--start_date', help='Start time of task', type=str, default=None)
    add_task.add_argument('-e', "--end_date", help="end date of task ", type=str, default=None)
    add_task.add_argument('--done', help="task Done", type=str, default=False)
    add_task.set_defaults(func=controller.add_task)

    list_task = subparser.add_parser('list', help="List all unfinished tasks")
    list_task.add_argument('-a', "--all", help="show all tasks ", action="store_true")
    list_task.set_defaults(func=controller.display)

    check_task = subparser.add_parser('check', help="Cheek the given task")
    check_task.add_argument('-t', '--task', help="Number of tasks To be done .", type=int)
    check_task.set_defaults(func=controller.check_task)

    remove_task = subparser.add_parser("remove", help="Remove Task ")
    remove_task.add_argument('-t', "--remove", help="Remove a Task " , type=int)
    remove_task.set_defaults(func=controller.remove)

    reset = subparser.add_parser('reset', help="reset all tasks")
    reset.set_defaults(func=controller.reset_all_tasks)
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
