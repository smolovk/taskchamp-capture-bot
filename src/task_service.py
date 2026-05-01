"""Taskwarrior CLI service for adding and syncing tasks."""
import re
import subprocess
from dataclasses import dataclass
from typing import Optional


@dataclass
class TaskResult:
    """Result of a task operation."""
    success: bool
    message: str
    task_id: Optional[str] = None
    error_type: Optional[str] = None


def add_task(description: str) -> TaskResult:
    """Add a new task to taskwarrior.
    
    Args:
        description: The task description with optional attributes
        
    Returns:
        TaskResult with success status and details
    """
    try:
        result = subprocess.run(
            ["task", "add", description],
            capture_output=True,
            text=True,
            check=False
        )
        
        if result.returncode != 0:
            # Parse common error types
            error_msg = result.stderr.strip() if result.stderr else result.stdout.strip()
            error_type = _categorize_error(error_msg)
            
            return TaskResult(
                success=False,
                message=error_msg,
                error_type=error_type
            )
        
        # Extract task ID from output like "Created task 42."
        task_id = _extract_task_id(result.stdout)
        
        return TaskResult(
            success=True,
            message="Task created successfully",
            task_id=task_id
        )
        
    except FileNotFoundError:
        return TaskResult(
            success=False,
            message="Taskwarrior not found. Is task installed?",
            error_type="not_installed"
        )
    except Exception as e:
        return TaskResult(
            success=False,
            message=f"Unexpected error: {str(e)}",
            error_type="unknown"
        )


def sync_tasks() -> TaskResult:
    """Sync tasks with the Taskchampion sync server.
    
    Returns:
        TaskResult with sync status
    """
    try:
        result = subprocess.run(
            ["task", "sync"],
            capture_output=True,
            text=True,
            check=False
        )
        
        if result.returncode != 0:
            return TaskResult(
                success=False,
                message=result.stderr.strip() if result.stderr else "Sync failed",
                error_type="sync_failed"
            )
        
        return TaskResult(
            success=True,
            message="Synced successfully"
        )
        
    except FileNotFoundError:
        return TaskResult(
            success=False,
            message="Taskwarrior not found",
            error_type="not_installed"
        )
    except Exception as e:
        return TaskResult(
            success=False,
            message=f"Sync error: {str(e)}",
            error_type="unknown"
        )


def _extract_task_id(output: str) -> Optional[str]:
    """Extract task ID from taskwarrior output."""
    match = re.search(r'Created task (\d+)\.', output)
    if match:
        return match.group(1)
    return None


def _categorize_error(error_msg: str) -> Optional[str]:
    """Categorize error message for better UX."""
    error_lower = error_msg.lower()
    
    if "not a valid date" in error_lower or "date" in error_lower:
        return "invalid_date"
    elif "project" in error_lower:
        return "invalid_project"
    elif "priority" in error_lower:
        return "invalid_priority"
    elif "recur" in error_lower or "recurrence" in error_lower:
        return "invalid_recurrence"
    
    return None
