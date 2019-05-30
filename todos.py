import json
from pathlib import Path
from datetime import date


class TodoManager(object):
    STATUS_ALL = 'all'
    STATUS_DONE = 'done'
    STATUS_PENDING = 'pending'
    CATEGORY_GENERAL = 'general'

    def __init__(self, base_todos_path, create_dir=True):
        self.base_todos_path = base_todos_path
        self.path = Path(self.base_todos_path)
        # continue here
        if self.path.exists() and not self.path.is_dir(): #if path does exist and is not a directory
            raise ValueError('Invalid path directory')
        if not self.path.exists():
            self.path.mkdir(parents = True)
    

    def list(self, status=STATUS_ALL, category=CATEGORY_GENERAL):
        todos_dict = {}
        for todo_path in self.path.glob('*.json'):
            with todo_path.open('r') as fp:
                document = json.load(fp)
                if not 'category_name' or not 'todos':
                    raise ValueError('Invalid JSON todo format')
                category_todos = []
                for todo in document['todos']:
                    if status == self.STATUS_ALL or todo['status']==status:
                        category_todos.append(todo)
                todos_dict[document['category_name']] = category_todos
        return todos_dict
                
    """
    todos_dict = {
                    docoument[category_name]:
                        [
                        {document[todos]},{document[todos]}
                        ],
                    document.[category_name]:
                        [
                        {document[todos]},{document[todos]}
                        ]
    }
    """        
                    

    def new(self, task, category=CATEGORY_GENERAL, description=None,
            due_on=None):

        if due_on:
            if type(due_on) == date:
                due_on = due_on.isoformat()
            elif type(due_on) == str:
                # all good
                pass
            else:
                raise ValueError('Invalid due_on type. Must be date or str')

        # continue here
        todo_file_name = '{}.json'.format(category) 
        new_path = self.path / todo_file_name
        
        if new_path.exists():
            with new_path.open('r') as fp:
                todos_dict = json.load(fp)
        else:
              todos_dict = {
                'category_name':category.title(),
                'todos':[]           
                }          
        
        todo = {
            'task':task,
            'description': description,
            'due_on': due_on,
            'status':self.STATUS_PENDING
        }
        
        todos_dict['todos'].append(todo)
        
        with new_path.open('w') as fp:
            todos= json.dump(todos_dict,fp,indent =2 )