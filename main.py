# main.py

import os
import sys
from typing import Union


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
    path = []
    cur = node
    while cur:
        path.append(cur)
        cur = cur.parent
    path.reverse()

    for depth, n in enumerate(path):
        indent = "    " * (depth - 1) if depth > 0 else ""
        if n.ingredients:
            ing_str = ", ".join(n.ingredients)
            display = f"{n.name}  + ({ing_str})"
        else:
            display = n.name

        if depth == 0:
            print(display)
        else:
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
    print("│ 8. 추천 재료 보기                    │")  # 추가된 메뉴
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


def login() -> Union[int, set]:
    isRestart = True
    while True:
        if isRestart:
            printLogin()
        else:
            isRestart = True

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
                my_ingredients = set()
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
    tree.build_tree_from_json("cocktails.json")
    userData = UserData()

    my_ingredients = set()
    isRestart = True
    islogin = False
    shutdown = False

    print("칵테일 프로그램을 시작합니다.")
    while not shutdown:
        if not islogin:
            pin, my_ingredients = login()
            islogin = True

        if shutdown:
            break

        if isRestart:
            printMenu()
        else:
            isRestart = True

        try:
            command = int(input("▶ 사용할 기능의 번호를 입력하세요: "))
        except:
            isRestart = False
            print("번호를 다시 입력해주세요.")
            continue

        if command == 1:
            # 칵테일 트리 전체 구조 보기
            print("\n📋 칵테일 트리 전체 구조")
            tree.print_tree()

        elif command == 2:
            # 칵테일의 정보 조회하기
            print("\n🔍 어떤 칵테일의 정보를 조회하시겠습니까?")
            cocktail_name = input("▶ 칵테일 이름을 입력하세요: ").strip()

            node = tree.find_node_by_name(cocktail_name)
            print(f"\n🔍 '{cocktail_name}'에 필요한 재료:")
            if node:
                for ing in node.get_full_ingredients():
                    print("-", ing)
            else:
                print("해당 칵테일을 찾을 수 없습니다.")

            if node:
                print(f"\n🌳 '{cocktail_name}' 레시피 트리:")
                print_recipe_path(node)

        elif command == 3:
            # 현재 만들 수 있는 칵테일 조회하기
            print("\n✅ 내가 가진 재료로 만들 수 있는 칵테일:")
            possible_list = tree.find_possible_cocktails(my_ingredients)
            if possible_list:
                for name in possible_list:
                    print("-", name)
            else:
                print("아무 것도 만들 수 없습니다.")

        elif command == 4:
            # 현재 갖고있는 재료 조회하기
            print("\n✅ 내가 가진 재료:")
            if my_ingredients:
                for ing in my_ingredients:
                    print("-", ing)
            else:
                print("아무것도 없습니다.")

        elif command == 5:
            # 재료 추가하기
            cocktail_name = input("▶ 추가할 재료를 입력하세요: ").strip()
            my_ingredients.add(cocktail_name)
            userData.save_data(pin, my_ingredients)

        elif command == 6:
            # 로그아웃
            islogin = False

        elif command == 7:
            # 종료하기
            shutdown = True
            print("  프로그램을 종료합니다.")
            break

        elif command == 8:
            # 추천 재료 보기
            print("\n🎯 하나만 더 추가하면 만들 수 있는 칵테일 추천:")
            recs = tree.recommend_with_one_missing(my_ingredients)
            if not recs:
                print("현재 가진 재료에 하나만 추가해도 만들 수 있는 칵테일이 없습니다.")
            else:
                for missing, cocktails in recs.items():
                    cocktails_str = ", ".join(cocktails)
                    print(f"- '{missing}'만 추가하면: {cocktails_str}")

        else:
            isRestart = False
            print("  번호를 다시 입력해주세요.")
            continue
