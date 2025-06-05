import streamlit as st
from CocktailTree import CocktailTree
from UserData import UserData

# 트리 로드
tree = CocktailTree()
tree.build_tree_from_json("cocktails.json")

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
