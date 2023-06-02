import pytest
from midddle import TaskManagementSystem

@pytest.fixture
def task_system(tmpdir):
    file_path = tmpdir.join("tasks.json")
    return TaskManagementSystem(str(file_path))

@pytest.mark.parametrize("task_data", [
    ("Finish project", "2023-06-01", 3),
    ("Submit report", "2023-06-02", 2),
    ("Prepare presentation", "2023-06-03", 1)
])
def test_add_task(task_system, task_data):
    description, created_date, priority = task_data
    task_system.add_task(description, created_date, priority)
    tasks = task_system.get_task_list()
    assert len(tasks) == 1
    assert tasks[0].description == description
    assert tasks[0].created_date == created_date
    assert tasks[0].priority == priority

def test_delete_task(task_system):
    task_system.add_task("Finish project", "2023-06-01", 3)
    task_system.add_task("Submit report", "2023-06-02", 2)
    tasks = task_system.get_task_list()
    task_id = id(tasks[0])
    task_system.delete_task(task_id)
    tasks = task_system.get_task_list()
    assert len(tasks) == 1
    assert tasks[0].description == "Submit report"

@pytest.mark.parametrize("completed_task_data", [
    ("Finish project", "2023-06-01", 3),
    ("Submit report", "2023-06-02", 2),
    ("Prepare presentation", "2023-06-03", 1)
])
def test_mark_task_completed(task_system, completed_task_data):
    description, created_date, priority = completed_task_data
    task_system.add_task(description, created_date, priority)
    tasks = task_system.get_task_list()
    task_id = id(tasks[0])
    task_system.mark_task_completed(task_id)
    tasks = task_system.get_task_list()
    assert tasks[0].completed

@pytest.mark.parametrize("sorting_option, expected_priority_order", [
    ('priority', [3, 2, 1]),
    ('created_date', [1, 2, 3])
])
def test_get_task_list(task_system, sorting_option, expected_priority_order):
    task_system.add_task("Finish project", "2023-06-01", 3)
    task_system.add_task("Submit report", "2023-06-02", 2)
    task_system.add_task("Prepare presentation", "2023-06-03", 1)
    tasks = task_system.get_task_list(sort_by=sorting_option)
    assert len(tasks) == 3
    assert [task.priority for task in tasks] == expected_priority_order
