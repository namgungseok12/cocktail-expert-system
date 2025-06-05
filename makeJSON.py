
import json
from CocktailTree import CocktailTree

# 1) DOCX 파일 경로 (CocktailTree.build_tree_from_docx가 이를 읽습니다)
DOCX_PATH = "Cocktail_Tree.docx"

# 2) JSON으로 저장할 파일명
OUTPUT_JSON_PATH = "cocktails.json"


def build_json_from_tree(tree: CocktailTree) -> dict:
    """
    CocktailTree의 root부터 재귀 순회하며,
    node.name, node.ingredients(인크리멘털), node.children 구조로 딕셔너리를 만든다.
    """

    def node_to_dict(node):
        return {
            "name": node.name,
            "ingredients": node.ingredients.copy(),
            "children": [node_to_dict(child) for child in node.children]
        }

    # 'Empty Glass'도 JSON 최상단에 포함
    return {
        "name": tree.root.name,
        "ingredients": tree.root.ingredients.copy(),
        "children": [node_to_dict(child) for child in tree.root.children]
    }


if __name__ == "__main__":
    # 3) 트리 생성
    tree = CocktailTree()
    tree.build_tree_from_docx(DOCX_PATH)

    # 4) JSON으로 변환
    tree_dict = build_json_from_tree(tree)

    # 5) JSON 파일로 저장
    with open(OUTPUT_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(tree_dict, f, ensure_ascii=False, indent=4)

    print(f"‘{OUTPUT_JSON_PATH}’ 파일이 생성되었습니다.")
