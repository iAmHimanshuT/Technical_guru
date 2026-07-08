"""
To-Do List Application with Local Storage Functionality
Manages tasks with priority levels, due dates, and persistent storage
"""
import json
import os
from datetime import datetime, timedelta
from enum import Enum
from typing import List, Dict, Optional

class Priority(Enum):
    """Priority levels for tasks"""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    URGENT = 4

class Task:
    """Represents a single task in the to-do list"""
    
    def __init__(self, task_id: int, title: str, description: str = "", 
                 priority: Priority = Priority.MEDIUM, due_date: Optional[str] = None):
        """
        Initialize a task
        
        Args:
            task_id (int): Unique identifier for the task
            title (str): Task title
            description (str): Task description
            priority (Priority): Task priority level
            due_date (str): Due date in YYYY-MM-DD format
        """
        self.task_id = task_id
        self.title = title
        self.description = description
        self.priority = priority
        self.due_date = due_date
        self.completed = False
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.completed_at = None
    
    def mark_completed(self):
        """Mark task as completed"""
        self.completed = True
        self.completed_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def mark_incomplete(self):
        """Mark task as incomplete"""
        self.completed = False
        self.completed_at = None
    
    def is_overdue(self) -> bool:
        """Check if task is overdue"""
        if not self.due_date or self.completed:
            return False
        
        try:
            due_date_obj = datetime.strptime(self.due_date, "%Y-%m-%d").date()
            today = datetime.now().date()
            return due_date_obj < today
        except ValueError:
            return False
    
    def to_dict(self) -> Dict:
        """Convert task to dictionary"""
        return {
            'task_id': self.task_id,
            'title': self.title,
            'description': self.description,
            'priority': self.priority.name,
            'due_date': self.due_date,
            'completed': self.completed,
            'created_at': self.created_at,
            'completed_at': self.completed_at
        }
    
    @staticmethod
    def from_dict(data: Dict) -> 'Task':
        """Create task from dictionary"""
        task = Task(
            task_id=data['task_id'],
            title=data['title'],
            description=data.get('description', ''),
            priority=Priority[data.get('priority', 'MEDIUM')],
            due_date=data.get('due_date')
        )
        task.completed = data.get('completed', False)
        task.created_at = data.get('created_at', task.created_at)
        task.completed_at = data.get('completed_at')
        return task
    
    def __str__(self) -> str:
        """String representation of task"""
        status = "✓" if self.completed else "○"
        priority_symbol = {
            Priority.LOW: "▁",
            Priority.MEDIUM: "▂",
            Priority.HIGH: "▃",
            Priority.URGENT: "▄"
        }[self.priority]
        
        overdue_indicator = " ⚠ OVERDUE" if self.is_overdue() else ""
        
        return (f"{status} [{self.task_id}] {priority_symbol} {self.title} "
                f"(Due: {self.due_date or 'N/A'}){overdue_indicator}")


class ToDoList:
    """Main To-Do List application with local storage"""
    
    def __init__(self, storage_file: str = "tasks.json"):
        """
        Initialize the to-do list
        
        Args:
            storage_file (str): Path to the JSON storage file
        """
        self.storage_file = storage_file
        self.tasks: List[Task] = []
        self.next_task_id = 1
        self.load_tasks()
    
    def save_tasks(self) -> bool:
        """
        Save tasks to local storage
        
        Returns:
            bool: True if save successful
        """
        try:
            data = {
                'tasks': [task.to_dict() for task in self.tasks],
                'next_task_id': self.next_task_id,
                'last_saved': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            with open(self.storage_file, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"✓ Tasks saved to {self.storage_file}")
            return True
        except Exception as e:
            print(f"✗ Error saving tasks: {str(e)}")
            return False
    
    def load_tasks(self) -> bool:
        """
        Load tasks from local storage
        
        Returns:
            bool: True if load successful
        """
        try:
            if os.path.exists(self.storage_file):
                with open(self.storage_file, 'r') as f:
                    data = json.load(f)
                    self.tasks = [Task.from_dict(task_data) for task_data in data.get('tasks', [])]
                    self.next_task_id = data.get('next_task_id', len(self.tasks) + 1)
                print(f"✓ Loaded {len(self.tasks)} task(s) from storage")
                return True
            else:
                print(f"ℹ No existing tasks file found - creating new list")
                return True
        except Exception as e:
            print(f"✗ Error loading tasks: {str(e)}")
            return False
    
    def add_task(self, title: str, description: str = "", 
                 priority: Priority = Priority.MEDIUM, due_date: Optional[str] = None) -> Optional[Task]:
        """
        Add a new task
        
        Args:
            title (str): Task title
            description (str): Task description
            priority (Priority): Task priority
            due_date (str): Due date in YYYY-MM-DD format
            
        Returns:
            Task: Created task or None if error
        """
        try:
            task = Task(self.next_task_id, title, description, priority, due_date)
            self.tasks.append(task)
            self.next_task_id += 1
            self.save_tasks()
            print(f"✓ Task added: {task}")
            return task
        except Exception as e:
            print(f"✗ Error adding task: {str(e)}")
            return None
    
    def remove_task(self, task_id: int) -> bool:
        """
        Remove a task by ID
        
        Args:
            task_id (int): ID of task to remove
            
        Returns:
            bool: True if removal successful
        """
        task = self.find_task(task_id)
        if task:
            self.tasks.remove(task)
            self.save_tasks()
            print(f"✓ Task {task_id} removed")
            return True
        print(f"✗ Task {task_id} not found")
        return False
    
    def find_task(self, task_id: int) -> Optional[Task]:
        """
        Find a task by ID
        
        Args:
            task_id (int): Task ID to find
            
        Returns:
            Task: Found task or None
        """
        for task in self.tasks:
            if task.task_id == task_id:
                return task
        return None
    
    def complete_task(self, task_id: int) -> bool:
        """
        Mark a task as completed
        
        Args:
            task_id (int): ID of task to complete
            
        Returns:
            bool: True if successful
        """
        task = self.find_task(task_id)
        if task:
            task.mark_completed()
            self.save_tasks()
            print(f"✓ Task {task_id} marked as completed")
            return True
        print(f"✗ Task {task_id} not found")
        return False
    
    def incomplete_task(self, task_id: int) -> bool:
        """
        Mark a task as incomplete
        
        Args:
            task_id (int): ID of task to mark incomplete
            
        Returns:
            bool: True if successful
        """
        task = self.find_task(task_id)
        if task:
            task.mark_incomplete()
            self.save_tasks()
            print(f"✓ Task {task_id} marked as incomplete")
            return True
        print(f"✗ Task {task_id} not found")
        return False
    
    def update_task(self, task_id: int, title: Optional[str] = None, 
                   description: Optional[str] = None, priority: Optional[Priority] = None,
                   due_date: Optional[str] = None) -> bool:
        """
        Update a task's details
        
        Args:
            task_id (int): ID of task to update
            title (str): New title
            description (str): New description
            priority (Priority): New priority
            due_date (str): New due date
            
        Returns:
            bool: True if update successful
        """
        task = self.find_task(task_id)
        if task:
            if title:
                task.title = title
            if description is not None:
                task.description = description
            if priority:
                task.priority = priority
            if due_date:
                task.due_date = due_date
            self.save_tasks()
            print(f"✓ Task {task_id} updated")
            return True
        print(f"✗ Task {task_id} not found")
        return False
    
    def get_tasks_by_priority(self, priority: Priority) -> List[Task]:
        """
        Get all tasks with a specific priority
        
        Args:
            priority (Priority): Priority level to filter
            
        Returns:
            List[Task]: List of tasks with matching priority
        """
        return [task for task in self.tasks if task.priority == priority]
    
    def get_incomplete_tasks(self) -> List[Task]:
        """
        Get all incomplete tasks
        
        Returns:
            List[Task]: List of incomplete tasks
        """
        return [task for task in self.tasks if not task.completed]
    
    def get_completed_tasks(self) -> List[Task]:
        """
        Get all completed tasks
        
        Returns:
            List[Task]: List of completed tasks
        """
        return [task for task in self.tasks if task.completed]
    
    def get_overdue_tasks(self) -> List[Task]:
        """
        Get all overdue tasks
        
        Returns:
            List[Task]: List of overdue tasks
        """
        return [task for task in self.tasks if task.is_overdue()]
    
    def get_tasks_due_today(self) -> List[Task]:
        """
        Get all tasks due today
        
        Returns:
            List[Task]: List of tasks due today
        """
        today = datetime.now().strftime("%Y-%m-%d")
        return [task for task in self.tasks if task.due_date == today and not task.completed]
    
    def get_tasks_due_this_week(self) -> List[Task]:
        """
        Get all tasks due this week
        
        Returns:
            List[Task]: List of tasks due this week
        """
        today = datetime.now().date()
        week_end = today + timedelta(days=7)
        return [task for task in self.tasks 
                if task.due_date and not task.completed and
                today <= datetime.strptime(task.due_date, "%Y-%m-%d").date() <= week_end]
    
    def search_tasks(self, keyword: str) -> List[Task]:
        """
        Search tasks by keyword in title or description
        
        Args:
            keyword (str): Search keyword
            
        Returns:
            List[Task]: List of matching tasks
        """
        keyword_lower = keyword.lower()
        return [task for task in self.tasks 
                if keyword_lower in task.title.lower() or 
                keyword_lower in task.description.lower()]
    
    def display_all_tasks(self):
        """Display all tasks"""
        if not self.tasks:
            print("\n📋 No tasks found")
            return
        
        print("\n" + "="*80)
        print("📋 ALL TASKS")
        print("="*80)
        for task in sorted(self.tasks, key=lambda t: (t.completed, -t.priority.value)):
            print(task)
        print("="*80 + "\n")
    
    def display_incomplete_tasks(self):
        """Display incomplete tasks"""
        incomplete = self.get_incomplete_tasks()
        if not incomplete:
            print("\n✓ All tasks completed!")
            return
        
        print("\n" + "="*80)
        print("📝 INCOMPLETE TASKS")
        print("="*80)
        for task in sorted(incomplete, key=lambda t: -t.priority.value):
            print(task)
        print("="*80 + "\n")
    
    def display_completed_tasks(self):
        """Display completed tasks"""
        completed = self.get_completed_tasks()
        if not completed:
            print("\n📋 No completed tasks")
            return
        
        print("\n" + "="*80)
        print("✓ COMPLETED TASKS")
        print("="*80)
        for task in completed:
            print(f"✓ [{task.task_id}] {task.title} (Completed: {task.completed_at})")
        print("="*80 + "\n")
    
    def display_overdue_tasks(self):
        """Display overdue tasks"""
        overdue = self.get_overdue_tasks()
        if not overdue:
            print("\n✓ No overdue tasks")
            return
        
        print("\n" + "="*80)
        print("⚠ OVERDUE TASKS")
        print("="*80)
        for task in overdue:
            print(task)
        print("="*80 + "\n")
    
    def display_stats(self):
        """Display task statistics"""
        total = len(self.tasks)
        completed = len(self.get_completed_tasks())
        incomplete = len(self.get_incomplete_tasks())
        overdue = len(self.get_overdue_tasks())
        
        print("\n" + "="*80)
        print("📊 STATISTICS")
        print("="*80)
        print(f"Total Tasks:      {total}")
        print(f"Completed:        {completed} ({(completed/total*100 if total > 0 else 0):.1f}%)")
        print(f"Incomplete:       {incomplete}")
        print(f"Overdue:          {overdue}")
        print(f"Low Priority:     {len(self.get_tasks_by_priority(Priority.LOW))}")
        print(f"Medium Priority:  {len(self.get_tasks_by_priority(Priority.MEDIUM))}")
        print(f"High Priority:    {len(self.get_tasks_by_priority(Priority.HIGH))}")
        print(f"Urgent:           {len(self.get_tasks_by_priority(Priority.URGENT))}")
        print("="*80 + "\n")
    
    def clear_completed_tasks(self) -> int:
        """
        Clear all completed tasks
        
        Returns:
            int: Number of tasks cleared
        """
        completed_count = len(self.get_completed_tasks())
        self.tasks = self.get_incomplete_tasks()
        self.save_tasks()
        print(f"✓ Cleared {completed_count} completed task(s)")
        return completed_count
    
    def export_tasks(self, export_file: str) -> bool:
        """
        Export tasks to a JSON file
        
        Args:
            export_file (str): Path to export file
            
        Returns:
            bool: True if export successful
        """
        try:
            data = {
                'total_tasks': len(self.tasks),
                'tasks': [task.to_dict() for task in self.tasks],
                'export_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            with open(export_file, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"✓ Tasks exported to {export_file}")
            return True
        except Exception as e:
            print(f"✗ Error exporting tasks: {str(e)}")
            return False
    
    def import_tasks(self, import_file: str) -> bool:
        """
        Import tasks from a JSON file
        
        Args:
            import_file (str): Path to import file
            
        Returns:
            bool: True if import successful
        """
        try:
            if not os.path.exists(import_file):
                print(f"✗ File not found: {import_file}")
                return False
            
            with open(import_file, 'r') as f:
                data = json.load(f)
                imported_tasks = [Task.from_dict(task_data) for task_data in data.get('tasks', [])]
                
                for task in imported_tasks:
                    if self.find_task(task.task_id) is None:
                        self.tasks.append(task)
                        self.next_task_id = max(self.next_task_id, task.task_id + 1)
                
                self.save_tasks()
                print(f"✓ Imported {len(imported_tasks)} task(s) from {import_file}")
                return True
        except Exception as e:
            print(f"✗ Error importing tasks: {str(e)}")
            return False


# Example usage and interactive menu
def main():
    """Main function to run the to-do list application"""
    todo = ToDoList("my_tasks.json")
    
    while True:
        print("\n" + "="*60)
        print("📋 TO-DO LIST APPLICATION")
        print("="*60)
        print("1. Add Task")
        print("2. View All Tasks")
        print("3. View Incomplete Tasks")
        print("4. View Completed Tasks")
        print("5. View Overdue Tasks")
        print("6. View Tasks Due Today")
        print("7. Complete Task")
        print("8. Mark Task Incomplete")
        print("9. Remove Task")
        print("10. Update Task")
        print("11. Search Tasks")
        print("12. View Statistics")
        print("13. Clear Completed Tasks")
        print("14. Export Tasks")
        print("15. Import Tasks")
        print("0. Exit")
        print("="*60)
        
        choice = input("\nEnter your choice: ").strip()
        
        if choice == "1":
            title = input("Task title: ").strip()
            description = input("Task description (optional): ").strip()
            priority_input = input("Priority (LOW/MEDIUM/HIGH/URGENT) [MEDIUM]: ").strip().upper() or "MEDIUM"
            due_date = input("Due date (YYYY-MM-DD) [optional]: ").strip() or None
            
            try:
                priority = Priority[priority_input]
                todo.add_task(title, description, priority, due_date)
            except KeyError:
                print("✗ Invalid priority level")
        
        elif choice == "2":
            todo.display_all_tasks()
        
        elif choice == "3":
            todo.display_incomplete_tasks()
        
        elif choice == "4":
            todo.display_completed_tasks()
        
        elif choice == "5":
            todo.display_overdue_tasks()
        
        elif choice == "6":
            tasks = todo.get_tasks_due_today()
            if tasks:
                print("\n📅 TASKS DUE TODAY:")
                for task in tasks:
                    print(task)
            else:
                print("\n✓ No tasks due today")
        
        elif choice == "7":
            task_id = int(input("Enter task ID to complete: "))
            todo.complete_task(task_id)
        
        elif choice == "8":
            task_id = int(input("Enter task ID to mark incomplete: "))
            todo.incomplete_task(task_id)
        
        elif choice == "9":
            task_id = int(input("Enter task ID to remove: "))
            todo.remove_task(task_id)
        
        elif choice == "10":
            task_id = int(input("Enter task ID to update: "))
            title = input("New title (press Enter to skip): ").strip() or None
            description = input("New description (press Enter to skip): ").strip() or None
            priority_input = input("New priority (press Enter to skip): ").strip().upper() or None
            due_date = input("New due date (press Enter to skip): ").strip() or None
            
            priority = None
            if priority_input:
                try:
                    priority = Priority[priority_input]
                except KeyError:
                    print("✗ Invalid priority level")
            
            todo.update_task(task_id, title, description, priority, due_date)
        
        elif choice == "11":
            keyword = input("Enter search keyword: ").strip()
            results = todo.search_tasks(keyword)
            if results:
                print(f"\n🔍 Found {len(results)} task(s):")
                for task in results:
                    print(task)
            else:
                print("\n✗ No tasks found matching keyword")
        
        elif choice == "12":
            todo.display_stats()
        
        elif choice == "13":
            confirm = input("Are you sure? This will delete all completed tasks (y/n): ").lower()
            if confirm == 'y':
                todo.clear_completed_tasks()
        
        elif choice == "14":
            export_file = input("Enter export filename [tasks_export.json]: ").strip() or "tasks_export.json"
            todo.export_tasks(export_file)
        
        elif choice == "15":
            import_file = input("Enter import filename: ").strip()
            todo.import_tasks(import_file)
        
        elif choice == "0":
            print("\n✓ Goodbye!")
            break
        
        else:
            print("✗ Invalid choice")


if __name__ == "__main__":
    # Demo mode
    print("\n" + "="*80)
    print("🚀 TO-DO LIST APPLICATION - DEMO MODE")
    print("="*80)
    
    # Create to-do list
    todo = ToDoList("demo_tasks.json")
    
    # Add sample tasks
    print("\n➕ Adding sample tasks...\n")
    todo.add_task("Complete project report", "Finish the Q3 report", Priority.HIGH, "2026-07-15")
    todo.add_task("Buy groceries", "Milk, eggs, bread", Priority.LOW, "2026-07-10")
    todo.add_task("Team meeting", "Weekly sync with team", Priority.MEDIUM, "2026-07-08")
    todo.add_task("Fix bug in authentication", "Login page not working", Priority.URGENT, "2026-07-09")
    todo.add_task("Learn Python", "Complete Python course on Udemy", Priority.MEDIUM)
    
    # Display all tasks
    todo.display_all_tasks()
    
    # Display statistics
    todo.display_stats()
    
    # Mark task as completed
    print("✓ Completing task 2...")
    todo.complete_task(2)
    
    # Display incomplete tasks
    todo.display_incomplete_tasks()
    
    # Search tasks
    print("🔍 Searching for 'report'...")
    results = todo.search_tasks("report")
    for task in results:
        print(task)
    
    # Get tasks due today
    print("\n📅 Tasks due today:")
    today_tasks = todo.get_tasks_due_today()
    if today_tasks:
        for task in today_tasks:
            print(task)
    else:
        print("No tasks due today")
    
    # Display stats again
    todo.display_stats()
    
    # Export tasks
    print("💾 Exporting tasks...")
    todo.export_tasks("demo_tasks_export.json")
    
    print("\n" + "="*80)
    print("✓ Demo completed! Tasks have been saved to 'demo_tasks.json'")
    print("="*80 + "\n")
    
    # Uncomment the line below to run the interactive menu
    # main()
