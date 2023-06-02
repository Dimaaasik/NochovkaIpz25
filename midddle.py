import os
import json

class Task:
    def __init__(self, description, created_date, priority):
        self.description = description
        self.created_date = created_date
        self.priority = priority
        self.completed = False

    def complete(self):
        self.completed = True

    def to_dict(self):
        return {
            'description': self.description,
            'created_date': self.created_date,
            'priority': self.priority,
            'completed': self.completed
        }

    @classmethod
    def from_dict(cls, task_dict):
        task = cls(task_dict['description'], task_dict['created_date'], task_dict['priority'])
        task.completed = task_dict['completed']
        return task

class TaskManagementSystem:
    def __init__(self, file_path):
        self.file_path = file_path
        self.tasks = []
        self.load_tasks()


    def load_tasks(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as file:
                data = json.load(file)
                self.tasks = [Task.from_dict(task_dict) for task_dict in data]
    #save task
    def save_tasks(self):
        with open(self.file_path, 'w') as file:
            data = [task.to_dict() for task in self.tasks]
            json.dump(data, file)
    #add task
    def add_task(self, description, created_date, priority):
        task = Task(description, created_date, priority)
        self.tasks.append(task)
        self.save_tasks()
    #delete task
    def delete_task(self, task_id):
        for task in self.tasks:
            if id(task) == task_id:
                self.tasks.remove(task)
                self.save_tasks()
                return True
        return False
    # mark task as completed
    def mark_task_completed(self, task_id):
        for task in self.tasks:
            if id(task) == task_id:
                task.complete()
                self.save_tasks()
                return True
        return False
    #return task list in sorted way
    def get_task_list(self, sort_by='priority'):
        if sort_by == 'priority':
            sorted_tasks = sorted(self.tasks, key=lambda x: x.priority, reverse=True)
        elif sort_by == 'created_date':
            sorted_tasks = sorted(self.tasks, key=lambda x: x.created_date, reverse=True)
        else:
            sorted_tasks = self.tasks

        return sorted_tasks

# file path
file_path = os.path.expanduser("~/tasks.json")

task_system = TaskManagementSystem(file_path)

# Adding tasks
task_system.add_task("Finish project", "2023-06-01", 3)
task_system.add_task("Buy groceries", "2023-06-02", 2)
task_system.add_task("Call John", "2023-06-02", 1)

# Displaying a list of tasks
tasks = task_system.get_task_list(sort_by='priority')
print("Task List (Sorted by Priority):")
for task in tasks:
    print(task.__dict__)

#Marking the task as completed
task_id = id(tasks[0])  #
task_system.mark_task_completed(task_id)
