import json

import frappe
from frappe import _
from frappe.utils.caching import redis_cache as get_cache


@frappe.whitelist(allow_guest=False)
def create_task(title, description="", status="Open", priority="Medium", due_date=None, assigned_to=None):
    """
    Create a new Task record.
    """
    try:
        # Create a new document for the Task DocType
        task = frappe.get_doc(
            {
                "doctype": "Task",
                "title": title,
                "description": description,
                "status": status,
                "priority": priority,
                "due_date": due_date,
                "assigned_to": assigned_to,
            }
        )
        task.insert(ignore_permissions=True)
        frappe.db.commit()
        return {"status": "success", "message": _("Task created successfully."), "task": task.as_dict()}
    except Exception as e:
        frappe.db.rollback()
        return {"status": "error", "message": str(e)}


@frappe.whitelist(allow_guest=False)
def read_task(task_name):
    """
    Optimized read API that only returns select fields of the Task.
    """
    try:
        # Instead of getting the full doc, fetch only specific fields
        task = frappe.db.get_value(
            "Task",
            {"name": task_name},
            ["name", "title", "status", "priority", "due_date", "assigned_to"],
            as_dict=True,
        )
        if not task:
            return {"status": "error", "message": "Task not found"}
        return {"status": "success", "task": task}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@frappe.whitelist(allow_guest=False)
def update_task(
    task_name, title=None, description=None, status=None, priority=None, due_date=None, assigned_to=None
):
    """
    Update an existing Task record.
    """
    try:
        task = frappe.get_doc("Task", task_name)
        # Update fields only if new values are provided
        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        if status is not None:
            task.status = status
        if priority is not None:
            task.priority = priority
        if due_date is not None:
            task.due_date = due_date
        if assigned_to is not None:
            task.assigned_to = assigned_to

        task.save(ignore_permissions=True)
        frappe.db.commit()
        return {"status": "success", "message": _("Task updated successfully."), "task": task.as_dict()}
    except Exception as e:
        frappe.db.rollback()
        return {"status": "error", "message": str(e)}


@frappe.whitelist(allow_guest=False)
def delete_task(task_name):
    """
    Delete a Task record.
    """
    try:
        frappe.delete_doc("Task", task_name, force=1)
        frappe.db.commit()
        return {"status": "success", "message": _("Task deleted successfully.")}
    except Exception as e:
        frappe.db.rollback()
        return {"status": "error", "message": str(e)}


@frappe.whitelist(allow_guest=False)
def list_tasks(page=1, page_size=10):
    """
    List tasks with pagination.
    """
    try:
        limit_start = (int(page) - 1) * int(page_size)
        tasks = frappe.get_all(
            "Task",
            fields=["name", "title", "status", "priority", "due_date"],
            limit_page_length=page_size,
            limit_start=limit_start,  # changed from 'offset' to 'limit_start'
            order_by="creation desc",
        )
        return {"status": "success", "tasks": tasks}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@frappe.whitelist(allow_guest=False)
def get_frequent_tasks():
    """
    Retrieve frequently accessed tasks with caching.
    """
    # Obtain a cache object with a specific cache key namespace
    cache = get_cache("frequent_tasks")
    # Try to fetch the cached task list
    cached_tasks = cache.get("task_list")

    if cached_tasks:
        # Return the cached result directly
        return {"status": "success", "tasks": json.loads(cached_tasks)}

    try:
        # Query the database if the cache is empty
        tasks = frappe.get_all(
            "Task",
            fields=["name", "title", "status", "priority", "due_date"],
            filters={"status": "Open"},
            limit=10,
            order_by="modified desc",
        )
        # Cache the result for 60 seconds (or any appropriate timeout)
        cache.set("task_list", json.dumps(tasks), timeout=60)
        return {"status": "success", "tasks": tasks}
    except Exception as e:
        return {"status": "error", "message": str(e)}
