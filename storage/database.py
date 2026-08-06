class Database:
    def __init__(self):
        self.store={}
    def set(self,key ,val):
        self.store[key]=val
    def get(self,key):
        return self.store.get(key)
    def delete(self,key):
        if key in self.store:
            del self.store[key]
            return True #if  found and deleted
        return False #if not found return false 