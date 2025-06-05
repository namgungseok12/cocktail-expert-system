# CocktailTree.py

import json
from CocktailNode import CocktailNode


class CocktailTree:
    """
    JSON 파일(cocktails.json) 기반으로 CocktailNode 트리를 만듭니다.
    - load_from_json(json_path): JSON을 읽어서 self.root에 트리를 구성
    - print_tree(): 콘솔에 계층 구조로 출력
    - find_node_by_name(name): 이름 대소문자 무시 검색
    - find_possible_cocktails(my_ingredients): 내가 가진 재료로 만들 수 있는 칵테일
    - recommend_with_one_missing(my_ingredients): 하나만 더 추가하면 만들 수 있는 칵테일 추천
    """

    def __init__(self):
        # 초기에는 빈 트리. load_from_json을 호출해야 root가 채워집니다.
        self.root = CocktailNode(name="Empty Glass", parent=None)

    def build_tree_from_json(self, json_path: str):

        #JSON 파일을 읽어서 CocktailNode 트리로 변환합니다.
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # 1) 최상위 노드 생성
        self.root = CocktailNode(name=data["name"], parent=None)
        # JSON에 지정된 인크리멘털 재료(부모와 겹치지 않는 재료)를 바로 할당
        self.root.ingredients = data.get("ingredients", [])

        # 2) 재귀적으로 자식 노드 생성
        def build_subtree(node: CocktailNode, node_data: dict):
            for child_data in node_data.get("children", []):
                # 자식 노드 생성
                child = CocktailNode(name=child_data["name"], parent=node)
                # 인크리멘털 재료 할당
                child.ingredients = child_data.get("ingredients", []).copy()
                # 자식의 자식들 생성
                build_subtree(child, child_data)

        build_subtree(self.root, data)

    def print_tree(self):
        """
        트리를 ├──, └── 기호로 계층 구조 출력합니다.
        """

        def dfs(node: CocktailNode, prefix: str = "", is_last: bool = True):
            if node.name != "Empty Glass":
                connector = "└── " if is_last else "├── "
                print(prefix + connector + node.name)
                prefix += "    " if is_last else "│   "

            for idx, child in enumerate(node.children):
                dfs(child, prefix, idx == len(node.children) - 1)

        dfs(self.root, "", True)

    def find_node_by_name(self, target_name: str):
        """
        이름 대소문자 구분 없이 트리 전체에서 해당 노드를 찾아 반환.
        없으면 None 반환.
        """

        def dfs(node: CocktailNode):
            if node.name.strip().lower() == target_name.strip().lower():
                return node
            for c in node.children:
                res = dfs(c)
                if res:
                    return res
            return None

        return dfs(self.root)

    def find_possible_cocktails(self, my_ingredients: set):
        """
        my_ingredients: 사용자가 가진 재료 세트 (예: {"Gin", "Dry Vermouth", "Olive Brine", "Olive Garnish"})
        - 트리의 모든 노드를 순회하며 node.get_full_ingredients() 결과가 my_ingredients에 모두 포함되면
          해당 노드를 만들 수 있다고 간주하고 리스트로 반환.
        """

        possible = []

        def dfs(node: CocktailNode):
            # get_full_ingredients()는 부모부터 누적된 재료를 모두 합쳐서 반환합니다.
            full_list = node.get_full_ingredients()
            if node.name != "Empty Glass" and all(ing in my_ingredients for ing in full_list):
                possible.append(node.name)
            for c in node.children:
                dfs(c)

        dfs(self.root)
        return possible

    def recommend_with_one_missing(self, my_ingredients: set):
        """
        my_ingredients: 사용자가 가진 재료 세트 (예: {"Gin", "Dry Vermouth", "Olive Brine"})
        - 하나만 더 추가하면 만들 수 있는 칵테일 목록을 추천합니다.
        - 반환 형식: { 부족재료: [칵테일1, 칵테일2, ...], ... }
        """

        missing_to_cocktails = {}

        def dfs(node: CocktailNode):
            if node.name != "Empty Glass":
                full_list = node.get_full_ingredients()
                # 내가 가진 재료를 제외한 부족한 재료 리스트
                diff = [ing for ing in full_list if ing not in my_ingredients]
                if len(diff) == 1:
                    missing = diff[0]
                    missing_to_cocktails.setdefault(missing, []).append(node.name)

            for c in node.children:
                dfs(c)

        dfs(self.root)
        return missing_to_cocktails
