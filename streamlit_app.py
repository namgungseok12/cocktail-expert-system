import streamlit as st
from CocktailTree import CocktailTree
from UserData import UserData

# 트리 로드
tree = CocktailTree()
tree.build_tree_from_json("cocktails.json")
my_ingredient = set()

# 사용자 정보 로드드
user_data = UserData()

def search_Page():
    st.title("🍸 칵테일 전문가 시스템")
    
    # 칵테일 이름으로 검색
    query = st.text_input("🔍 칵테일 이름을 입력하세요")
    if st.button("검색"):
        node = tree.find_node_by_name(query)
        if node:
            st.subheader(f"📋 {query}의 재료")
            for ing in node.get_full_ingredients():
                st.markdown(f"- {ing}")
        else:
            st.error("해당 칵테일을 찾을 수 없습니다.")
            

def home_Page():
    st.title("🍸 칵테일 전문가 시스템")
    
    st.write("다음 중 실행할 기능의 버튼을 눌러주세요")
    c1, c2, c3, c4, c5, c6, c7, c8 = st.columns(8)
    mode = 0
    with c1:
        if st.button("칵테일 검색"):
            mode = 1
    with c2:
        if st.button("현재 재료 보기"):
            mode = 2
    
    if mode == 1:
        search_Page()
    elif mode == 2:
        st.write("asdfadsf")
        search_Page()
            
        
        
def register_Page():        
    st.title("🍸 칵테일 전문가 시스템 로그인")
    userPin = st.text_input('사용할 핀 번호를 입력해주세요')
    
    if st.button('회원가입하기'):
        if not userPin:
            st.error("핀 번호호를 입력하세요.")
        else:
            userPin = int(userPin)
            if not user_data.isValid(userPin):
                global my_ingredient
                my_ingredient = set()
                user_data.save_data(userPin, my_ingredient)
                st.session_state['authenticated'] = True
                st.session_state['registered'] = False
                # 현재 상태 값을 true로 변경 후 다시 실행하여 화면을 변경함
                st.rerun()
            else:
                st.error('이미 사용중인 핀번호입니다.')

        
def login_Page():
    st.title("🍸 칵테일 전문가 시스템 로그인")
    userPin = st.text_input('핀 번호를 입력해주세요')

    if st.button('로그인'):
        if not userPin:
            st.error("로그인 ID를 입력하세요.")
        else:
            userPin = int(userPin)
            if user_data.isValid(userPin):
                global my_ingredient
                my_ingredient = user_data.load_data(userPin)
                st.session_state['authenticated'] = True
                # 현재 상태 값을 true로 변경 후 다시 실행하여 화면을 변경함
                st.rerun()
            else:
                st.error('로그인 실패')
    elif st.button('회원가입'):
        st.session_state['registered'] = True
        st.rerun()


# 초기 페이지 값 세팅
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = True
if 'registered' not in st.session_state:
    st.session_state['registered'] = False
    
# 로그인, 회원가입, 홈페이지 구현
if st.session_state['registered']:
    register_Page()
elif st.session_state['authenticated']:
    home_Page()
else:
    login_Page()