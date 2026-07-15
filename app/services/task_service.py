class TaskService:

    tasks = [
    {
        "id": 1,
        "title": "Learn FastAPI",
        "priority": "high"
    },
    {
        "id": 2,
        "title": "Study REST",
        "priority": "low"
    }
]

    def get_tasks(self,priority: str | None = None):
        if priority is None:
            return self.tasks  
        return [task for task in self.tasks if task["priority"] == priority]
    
    def get_task(self,task_id: int):       

        for task in self.tasks:
            if task["id"] == task_id:
                return task
        return "Not valid ID"   
        # return [task for task in self.tasks if task["id"] == task_id]
    
    def create_task(self,task):
        # self.tasks.append(task)
        return task
