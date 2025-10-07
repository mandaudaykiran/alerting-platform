import time
import threading
from typing import Callable, Optional

class Scheduler:
    def __init__(self):
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._tasks: Dict[str, dict] = {}
    
    def start_periodic_task(self, task_id: str, interval: int, task: Callable, daemon: bool = True):
        """Start a periodic task that runs every interval seconds"""
        if task_id in self._tasks:
            print(f"⚠️ Task {task_id} is already running")
            return
        
        self._tasks[task_id] = {
            'interval': interval,
            'task': task,
            'running': True
        }
        
        def run():
            while self._tasks.get(task_id, {}).get('running', False):
                try:
                    print(f"🔄 Running scheduled task: {task_id}")
                    task()
                except Exception as e:
                    print(f"❌ Error in scheduled task {task_id}: {e}")
                time.sleep(interval)
        
        thread = threading.Thread(target=run, daemon=daemon)
        thread.start()
        
        self._tasks[task_id]['thread'] = thread
        print(f"✅ Started periodic task: {task_id} (interval: {interval}s)")
    
    def stop_task(self, task_id: str):
        """Stop a specific task"""
        if task_id in self._tasks:
            self._tasks[task_id]['running'] = False
            if 'thread' in self._tasks[task_id]:
                self._tasks[task_id]['thread'].join(timeout=5)
            del self._tasks[task_id]
            print(f"✅ Stopped task: {task_id}")
    
    def stop_all(self):
        """Stop all running tasks"""
        print("🛑 Stopping all scheduled tasks...")
        for task_id in list(self._tasks.keys()):
            self.stop_task(task_id)
        print("✅ All tasks stopped")
    
    def get_running_tasks(self) -> list:
        """Get list of currently running tasks"""
        return list(self._tasks.keys())
    
    def is_task_running(self, task_id: str) -> bool:
        """Check if a specific task is running"""
        return task_id in self._tasks and self._tasks[task_id]['running']