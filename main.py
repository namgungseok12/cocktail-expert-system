# main.py

import os
import sys


# 현재 파일과 동일한 디렉터리에 CocktailTree.py, CocktailNode.py가 있다고 가정
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from CocktailTree import CocktailTree
from UserData import UserData


def print_recipe_path(node):
    """
    주어진 node(칵테일)까지 올라가는 조상(ancestor) 리스트를 모아서,
    루트(Empty Glass) → ... → node 순으로 트리처럼 보이게 출력하되,
    각 단계에서 추가된 재료(ingredients)도 함께 출력한다.
    """
    # 조상 노드를 모은 뒤 역순으로 뒤집어 루트→리프 순으로 정렬
    path = []
    cur = node
    while cur:
        path.append(cur)
        cur = cur.parent
    path.reverse()

    for depth, n in enumerate(path):
        # 들여쓰기 문자열
        indent = "    " * (depth - 1) if depth > 0 else ""

        # 현재 노드에 붙어 있는 재료가 있으면 ", "로 합쳐서 표시
        if n.ingredients:
            ing_str = ", ".join(n.ingredients)
            display = f"{n.name}  + ({ing_str})"
        else:
            # 재료가 없는 경우(예: Empty Glass 직계 자식인 기본 술 단계) 그냥 이름만 표시
            display = n.name

        if depth == 0:
            # 맨 첫 단계: 루트(Empty Glass)는 별도 커넥터 없이 그냥 출력
            print(display)
        else:
            # 이후 단계: └── 칵테일 이름 + (재료)
            print(f"{indent}└── {display}")

def printMenu():
    print("")
    print("┌───────── <프로그램 기능> ────────────┐")
    print("│ 1. 칵테일 트리 전체 구조 보기        │")
    print("│ 2. 칵테일의 정보 조회하기            │")
    print("│ 3. 현재 만들 수 있는 칵테일 조회하기 │")
    print("│ 4. 갖고 있는 재료 조회하기           │")
    print("│ 5. 재료 추가하기                     │")
    print("│ 6. 로그아웃하기                      │")
    print("│ 7. 종료하기                          │")
    print("└──────────────────────────────────────┘")
    
def printLogin():
    print("")
    print("┌──── <Login> ────┐")
    print("│ 1. 로그인하기   │")
    print("│ 2. 회원가입하기 │")
    print("│ 3. 종료하기     │")
    print("└─────────────────┘")

def getPin() -> int:
    while True:
        try:
            pin = int(input("▶ 핀번호를 입력하세요: "))
            break
        except:
            print("   핀번호를 다시 입력해주세요.")
    return pin
                    
def login() -> dict:
    isRestart = True
    while True:
        if isRestart: printLogin()
        else: isRestart = True
        
        try:
            command = int(input("▶ 사용할 기능의 번호를 입력하세요: "))
        except:
            isRestart = False
            print("   번호를 다시 입력해주세요.")
            continue
        
        if command == 1:    # 로그인
            pin = getPin()
            if userData.isValid(pin):
                my_ingredients = userData.load_data(pin)
                return pin, my_ingredients
            else:
                print("  유효하지 않은 핀번호입니다.")
                isRestart = False
                
        elif command == 2:  # 회원가입
            pin = getPin()
            if userData.isValid(pin):
                print("  이미 사용중인 핀번호입니다.")
            else:
                my_ingredients = {}
                userData.save_data(pin, my_ingredients)
                print("  회원가입이 완료되었습니다.")
                return pin, my_ingredients
            
        elif command == 3:
            global shutdown
            shutdown = True
            return None, None
        
        else:
            isRestart = False
            print("  번호를 다시 입력해주세요.")
            continue

if __name__ == "__main__":
    tree = CocktailTree()
    tree.build_tree_from_docx("Cocktail_Tree.docx")   # 실제 docx 파일 경로
    userData = UserData()
    
    
    # 예시 재료 세트 (필요에 따라 수정 가능)
    my_ingredients = dict()

    isRestart = True
    islogin = False
    shutdown = False
    
    print("칵테일 프로그램을 시작합니다.")
    while not shutdown:
        if not islogin:
            pin, my_ingredients = login()
            islogin = True
        
        if shutdown: break
        
        # 번호를 잘못 입력한 경우, 메뉴를 다시 출력하지 않음
        if isRestart: printMenu()
        else: isRestart = True
        
        # command에 번호 저장
        try:
            command = int(input("▶ 사용할 기능의 번호를 입력하세요: "))
        except:
            isRestart = False
            print("번호를 다시 입력해주세요.")
            continue
        
        if command == 1: 
            print("\n📋 칵테일 트리 전체 구조")
            tree.print_tree()  # 칵테일 트리 전체 구조 보기
        elif command == 2:  # 칵테일의 정보 조회하기
            print("\n🔍 어떤 칵테일의 정보를 조회하시겠습니까?")
            cocktail_name = input("▶ 칵테일 이름을 입력하세요: ").strip()

            # 입력받은 이름으로 노드 탐색
            node = tree.find_node_by_name(cocktail_name)

            # 해당 칵테일의 재료 출력
            print(f"\n🔍 '{cocktail_name}'에 필요한 재료:")
            if node:
                for ing in node.get_full_ingredients():
                    print("-", ing)
            else:
                print("해당 칵테일을 찾을 수 없습니다.")

            # 해당 칵테일의 레시피 트리(경로) 출력
            if node:
                print(f"\n🌳 '{cocktail_name}' 레시피 트리:")
                print_recipe_path(node)
        elif command == 3:  # 현재 만들 수 있는 칵테일 조회하기
            print("\n✅ 내가 가진 재료로 만들 수 있는 칵테일:")
            possible_list = tree.find_possible_cocktails(my_ingredients)
            if possible_list:
                for name in possible_list:
                    print("-", name)
            else:
                print("아무 것도 만들 수 없습니다.")
        elif command == 4: # 현재 갖고있는 재료 조회하기
            print("\n✅ 내가 가진 재료:")
            if my_ingredients:
                for ing in my_ingredients:
                    print("-", ing)
            else:
                print("아무것도 없습니다.")
        elif command == 5:  # 재료 추가하기
            cocktail_name = input("▶ 추가할 칵테일 이름을 입력하세요: ").strip()
            my_ingredients.add(cocktail_name)
            userData.save_data(pin, my_ingredients)
        elif command == 6:
            islogin = False
        elif command == 7:  # 종료하기
            shutdown = True
            print("  프로그램을 종료합니다.")
            break
        else:
            isRestart = False
            print("  번호를 다시 입력해주세요.")
            continue
