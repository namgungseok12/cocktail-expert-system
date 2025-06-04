import pickle

class UserData:
    def __init__(self):
        with open("userData.pickle", "rb") as fr:
            self.data = pickle.load(fr)
    
    def save_data(self, pin, ings) -> None:
        self.data[pin] = ings
        with open("userData.pickle", "wb") as fw:
            pickle.dump(self.data, fw)
            
    def isValid(self, pin) -> bool:
        return pin in self.data
    
    def load_data(self, pin) -> dict:
        return self.data[pin]
    
    