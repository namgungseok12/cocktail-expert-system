import pickle

class UserData:
    """
    userData.pickle 파일에서 모든 사용자의 재료 정보를 딕셔너리 자료형으로 불러오는 클래스
    - save_data(pin, ings): pin 번호를 key 값, ings를 value로 딕셔너리에 저장
    - isValid(pin): pin 번호가 이미 key값으로 사용되면 True, 아니면 False 리턴
    - load_data(pin): key가 pin 번호인 value(set) 리턴
    """
    def __init__(self):
        with open("userData.pickle", "rb") as fr:
            self.data = pickle.load(fr)
    
    def save_data(self, pin:int, ings:set) -> None:
        self.data[pin] = ings
        with open("userData.pickle", "wb") as fw:
            pickle.dump(self.data, fw)
            
    def isValid(self, pin:int) -> bool:
        return pin in self.data
    
    def load_data(self, pin:int) -> set:
        return self.data[pin]
    
    