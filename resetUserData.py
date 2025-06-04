import pickle

남궁석 = 20222890
송민혁 = 20202939

userData = { 
    남궁석 : {"Gin", "Dry Vermouth", "Olive Brine", "Olive Garnish"},
    송민혁 : {"Gin", "Dry Vermouth", "Olive Brine", "Olive Garnish"},
}

# 파일로 저장
with open('userData.pickle', 'wb') as f:
    pickle.dump(userData, f)
    
# 파일 불러오기
with open('userData.pickle', 'rb') as f:
    loaded_dict = pickle.load(f)
    
print(loaded_dict)