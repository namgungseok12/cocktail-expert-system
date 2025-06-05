# app.py

import streamlit as st
from click import clear

from CocktailTree import CocktailTree
from UserData import UserData

# ─── 세션 상태 초기화 ───────────────────────────────────────────────────────────
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.pin = None
    st.session_state.my_ingredients = set()

# ─── 백엔드 객체 로드 ───────────────────────────────────────────────────────────
tree = CocktailTree()
tree.build_tree_from_json("cocktails.json")  # JSON 파일 이름을 cocktails.json 으로 사용

userData = UserData()


# ─── 로그인/회원가입 화면 ─────────────────────────────────────────────────────────
def login_page():
    st.title("🍸 Cocktail Expert System")
    st.subheader("로그인 또는 회원가입")

    # ── 로그인 폼 ────────────────────────────────────────────────────────────
    with st.form(key="login_form"):
        st.markdown("**🔑 PIN 번호를 입력하세요**")
        pin_input = st.text_input("PIN", key="login_pin")
        login_btn = st.form_submit_button("로그인")

        if login_btn:
            try:
                pin = int(pin_input)
                if userData.isValid(pin):
                    # 로그인 성공 → 세션 상태 업데이트
                    st.session_state.logged_in = True
                    st.session_state.pin = pin
                    st.session_state.my_ingredients = userData.load_data(pin)
                    st.success("로그인 성공! 메인 메뉴로 이동합니다.")
                    # 자동 rerun
                    st.rerun()
                else:
                    st.error("유효하지 않은 PIN 번호입니다.")
            except ValueError:
                st.error("PIN 번호는 숫자만 입력하세요.")

    st.markdown("---")

    # ── 회원가입 폼 ────────────────────────────────────────────────────────────
    with st.form(key="signup_form"):
        st.markdown("**📗 신규 PIN 번호를 입력하세요**")
        pin_signup = st.text_input("New PIN", key="signup_pin")
        signup_btn = st.form_submit_button("회원가입")

        if signup_btn:
            try:
                pin2 = int(pin_signup)
                if userData.isValid(pin2):
                    st.error("이미 사용 중인 PIN 번호입니다.")
                else:
                    userData.save_data(pin2, set())
                    st.success("회원가입 완료! 방금 가입하신 PIN으로 로그인해 주세요.")
                    # 폼 초기화 및 화면 갱신
                    st.rerun()
            except ValueError:
                st.error("PIN 번호는 숫자만 입력하세요.")


# ─── 메인 메뉴 페이지 ───────────────────────────────────────────────────────────
def main_menu():
    st.sidebar.title("Cocktail Expert System")
    menu = st.sidebar.radio(
        "",
        (
            "1. 🍹 전체 칵테일 보기",
            "2. 📙 칵테일 레시피",
            "3. 🍸 만들 수 있는 칵테일",
            "4. 🗄️ my 냉장고",
            "5. 😎 cocktail expert가 추천하는 재료",
            "6. 로그아웃"
        ),
    )

    # ───────────────────────────────────────────────────────────────────────────────
    # 1. 트리 전체 구조 보기
    if menu == "1. 🍹 전체 칵테일 보기":
        # 1) 트리 구조를 문자열 리스트에 모아서
        lines = []

        def dfs(node, prefix=""):
            for i, child in enumerate(node.children):
                connector = "└── " if i == len(node.children) - 1 else "├── "
                lines.append(f"{prefix}{connector}{child.name}")
                new_prefix = prefix + ("    " if i == len(node.children) - 1 else "│   ")
                dfs(child, new_prefix)

        # 루트(Empty Glass)부터 DFS로 줄 단위 문자열 생성
        lines.insert(0, "Empty Glass")
        dfs(tree.root)

        # 2) 줄 단위 리스트를 단일 문자열로 결합
        tree_str = "\n".join(lines)

        # 3) st.code()를 사용해 “코드 블록”으로 출력
        st.header("📋 칵테일 트리 전체 구조")
        st.write("")  # 줄 바꿈
        st.write("")  # 줄 바꿈
        st.code(tree_str, language="")  # language="" 로 하면 언어 하이라이트 없이 고정폭 폰트로 보여줌

    # ───────────────────────────────────────────────────────────────────────────────
    # 2. 칵테일 정보 조회
    elif menu == "2. 📙 칵테일 레시피":
        st.header("🔍 칵테일 정보 조회")
        st.write("")  # 줄 바꿈
        st.write("")  # 줄 바꿈
        name = st.text_input("조회할 칵테일 이름을 입력하세요")
        if st.button("검색"):
            node = tree.find_node_by_name(name.strip())
            if not node:
                st.error("해당 칵테일을 찾을 수 없습니다.")
            else:
                st.subheader(f"🍸 '{node.name}'에 필요한 전체 재료")
                for ing in node.get_full_ingredients():
                    st.write("-", ing)

                st.write("")  # 줄 바꿈
                st.write("")  # 줄 바꿈

                st.subheader(f"🌳 '{node.name}' 만드는 순서")
                path = []
                cur = node
                while cur:
                    path.append(cur)
                    cur = cur.parent
                path.reverse()
                for depth, n in enumerate(path):
                    indent = " " * (depth * 4)
                    if n.ingredients:
                        ing_str = ", ".join(n.ingredients)
                        st.text(f"{indent} ↪️ {n.name}  + ({ing_str})")
                    else:
                        st.text(f"{indent} ↪️ {n.name}")

    # ───────────────────────────────────────────────────────────────────────────────
    # 3. 현재 만들 수 있는 칵테일 목록
    elif menu == "3. 🍸 만들 수 있는 칵테일":
        st.header("✅ 내가 가진 재료로 만들 수 있는 칵테일")
        st.write("")  # 줄 바꿈
        st.write("")  # 줄 바꿈
        if st.session_state.my_ingredients:
            possible = tree.find_possible_cocktails(st.session_state.my_ingredients)
            if possible:
                for c in possible:
                    st.write("-", c)
            else:
                st.write("현재 가진 재료로 만들 수 있는 칵테일이 없습니다.")
        else:
            st.write("아직 재료가 없습니다. 먼저 재료를 추가해 주세요.")

    # ───────────────────────────────────────────────────────────────────────────────
    # 4. my 냉장고 (재료 조회 및 추가)
    elif menu == "4. 🗄️ my 냉장고":
        st.header("🗄️ my 냉장고")
        st.write("")  # 줄 바꿈
        st.write("")  # 줄 바꿈

        # 4-1) 현재 재료 목록 표시
        st.subheader("▶ 내가 가진 재료")
        if st.session_state.my_ingredients:
            for ing in sorted(st.session_state.my_ingredients):
                st.write("-", ing)
        else:
            st.write("아직 재료가 없습니다.")

        st.markdown("---")

        # ── “add_submitted=True” 플래그를 확인하여,
        # 재실행 시(add_submitted가 True) 한 번만 텍스트를 비워 줍니다.
        if st.session_state.get("add_submitted", False):
            # 입력 키 “add_ingredient_input”에 빈 문자열을 대입 → 폼 전에 실행
            st.session_state["add_ingredient_input"] = ""
            # 플래그 즉시 삭제 → 딱 한 번만 지워 줍니다
            st.session_state["add_submitted"] = False

        # 4-2) 재료 추가를 위한 폼
        with st.form(key="add_form"):
            st.subheader("➕ 냉장고에 재료 추가하기")
            new_ing = st.text_input(
                "추가할 재료를 입력하세요",
                key="add_ingredient_input"
            )
            add_btn = st.form_submit_button("추가하기")

            if add_btn:
                item = new_ing.strip()
                if item:
                    st.session_state.my_ingredients.add(item)
                    userData.save_data(st.session_state.pin, st.session_state.my_ingredients)
                    st.success(f"'{item}' 재료가 추가되었습니다.")
                    # “다음에 렌더링할 때 입력칸 비우기” 플래그 설정
                    st.session_state["add_submitted"] = True
                    # rerun하면 최상단에서 add_submitted가 True인 걸 보고
                    # add_ingredient_input을 빈 문자열로 리셋하고, 다시 False로 바꿔줍니다
                    st.rerun()
                else:
                    st.error("빈칸은 추가할 수 없습니다.")
                
        st.markdown("---")
        # 4-3) 재료 삭제 입력창
        st.subheader("➖ 냉장고의 재료 삭제하기")
        del_ing = st.text_input("삭제할 재료를 입력하세요", key="del_ingredient_input")
        if st.button("삭제하기"):
            item = del_ing.strip()
            if item and item in st.session_state.my_ingredients:
                st.session_state.my_ingredients.remove(item)
                userData.save_data(st.session_state.pin, st.session_state.my_ingredients)
                st.success(f"'{item}' 재료가 삭제되었습니다.")
                
                # 추가 후 화면 갱신
                st.rerun()
            elif item:
                st.error(f"{item} 재료는 냉장고에 없습니다.")
            else:
                st.error("빈칸은 삭제할 수 없습니다.")

    # ───────────────────────────────────────────────────────────────────────────────
    # 5. 추천 재료 보기
    elif menu == "5. 😎 cocktail expert가 추천하는 재료":

        st.header("🎯 하나만 더 추가하면 만들 수 있는 칵테일 추천")
        st.write("")  # 줄 바꿈
        st.write("")  # 줄 바꿈

        if st.session_state.my_ingredients:
            recs = tree.recommend_with_one_missing(st.session_state.my_ingredients)
            if recs:
                for missing, cock_list in recs.items():
                    st.write(f"- **'{missing}'** 만 추가하면: {', '.join(cock_list)}")
            else:
                st.write("현재 가진 재료에 하나만 추가해도 만들 수 있는 칵테일이 없습니다.")
        else:
            st.write("먼저 재료를 추가한 뒤, 추천 기능을 이용하세요.")

    # ───────────────────────────────────────────────────────────────────────────────
    # 6. 로그아웃
    elif menu == "6. 로그아웃":
        st.session_state.logged_in = False
        st.session_state.pin = None
        st.session_state.my_ingredients = set()
        st.success("로그아웃되었습니다.")
        # 로그아웃 후 바로 rerun
        st.rerun()


# ─── 앱 실행 ───────────────────────────────────────────────────────────────────
if not st.session_state.logged_in:
    login_page()
else:
    main_menu()
