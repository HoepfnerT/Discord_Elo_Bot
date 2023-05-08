from Result import Result


class Result_List():
    def __init__(self, result_list = []): 
        self.result_list = result_list

    @classmethod
    def from_json(cls, j):
        result_list = [Result.from_json(rs) for rs in j]
        return cls(result_list)

    def add_result(self, result: Result):   
        self.result_list.append(result)

    def delete_result(self, result: Result):
        for r in self.result_list:
            if r.equals(result):
                self.result_list.remove(r)
                return True
        return True

    def clear(self):    self.result_list = []
    def __iter__(self): yield from self.result_list
    def __len__(self):  return len(self.result_list)

    def to_json(self):  return [result.to_json() for result in self.result_list]
    def __repr__(self): return ",\n".join(repr(result) for result in self.result_list)
    def __str__(self):  return ",\n".join(str(result) for result in self.result_list)