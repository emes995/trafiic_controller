
class PriorityControl(set):

    def __init__(self, priority):
        self._priority = priority

    @property
    def priority(self):
        return self._priority

    def addObject(self, controllableObj):
        self.add(controllableObj)
