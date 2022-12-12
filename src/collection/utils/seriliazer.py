class Seriliazer:
    def __init__(self) -> None:
        self.dict_to_seriliaze = []
    
    def convert_list_json(self, query):
        for element in query:
            self.dict_to_seriliaze.append({element.ID,element.TODO,element.DESCRIPTION})
        
        print(self.dict_to_seriliaze)
        return self.dict_to_seriliaze
