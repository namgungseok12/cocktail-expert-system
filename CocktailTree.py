# CocktailTree.py

import re
from collections import deque
from docx import Document
from CocktailNode import CocktailNode


class CocktailTree:
    """
    과제: 'Cocktail_Tree.docx'에서 트리를 읽어 와서 메모리에 트리 구조를 만든 뒤,
    - print_tree(): 트리 형태로 콘솔에 출력
    - find_node_by_name(name): 이름으로 노드를 찾아 리턴
    - find_possible_cocktails(my_ingredients): 주어진 재료(my_ingredients 세트)로 만들 수 있는 칵테일 목록을 리턴
    """

    def __init__(self):
        # 루트 노드: 더미로 쓰는 'Empty Glass'
        self.root = CocktailNode(name="Empty Glass")

    def build_tree_from_docx(self, docx_path):
        """
        DOCX 파일을 한 줄씩(paragraph 단위) 읽어와서,
        1) 줄 앞에 붙은 탭(\t) 개수를 indent로 활용
        2) 앞쪽 박스 그리기 문자(│, ├, └ 등)와 공백·탭을 전부 정규표현식으로 스트립 → clean_line
        3) clean_line이 '+'로 시작하면 pending[indent]에 해당 재료들을 추가
        4) clean_line이 '+'로 시작하지 않으면 '칵테일 이름'으로 간주 →
           (a) stack을 indent 기준으로 pop하여 올바른 부모(parent)를 찾음
           (b) 새 노드를 만들고, pending[indent-1]에 모여 있던 재료를 이 노드의 ingredients로 부여
           (c) stack에 (이 노드, indent) 추가
        """
        doc = Document(docx_path)
        stack = deque()
        # 새로 시작할 때마다 항상 root부터 초기화
        self.root = CocktailNode("Empty Glass", None)
        stack.append((self.root, -1))

        # pending: {indent_level: [ingredient1, ingredient2, ...]}
        pending = {}

        for para in doc.paragraphs:
            raw_line = para.text.rstrip()
            if not raw_line.strip():
                continue

            # 1) indent = raw_line 내에 포함된 '\t' 개수
            indent = raw_line.count("\t")

            # 2) 앞쪽에 붙은 박스 그리기 문자/공백/탭 등을 모두 지우고 깔끔한 텍스트만 남김
            #    r'^[\s│\t├└┬┴┼─┐└]+' → 공백(\s), '│', 탭(\t), '├', '└', '┬', '┴', '┼', '─', '┐' 등을 한 번에 제거
            clean_line = re.sub(r'^[\s│\t├└┬┴┼─┐└]+', '', raw_line).strip()
            if not clean_line:
                continue

            # 3) 만약 clean_line이 "+ 재료1 + 재료2 + ..." 형태라면 pending에 임시로 보관
            if clean_line.startswith("+"):
                ingredients = [item.strip() for item in clean_line.split("+")[1:] if item.strip()]
                if indent in pending:
                    pending[indent].extend(ingredients)
                else:
                    pending[indent] = ingredients.copy()
            else:
                # 4) '칵테일 이름' 줄이라고 판단한다면
                #    stack에서 현재 indent보다 크거나 같은(>=) 모든 엔트리를 pop하여 올바른 부모 노드 찾기
                while stack and stack[-1][1] >= indent:
                    stack.pop()
                parent_node, _ = stack[-1]

                # 새 노드 생성
                node = CocktailNode(name=clean_line, parent=parent_node)

                # pending[indent-1]에 쌓여 있던 재료를 가져와서 node.ingredients로 설정
                ing_key = indent - 1
                if ing_key in pending:
                    node.ingredients = pending[ing_key]
                    del pending[ing_key]

                # 새 노드를 stack에 (node, indent)로 push
                stack.append((node, indent))

    def print_tree(self):
        """
        트리를 박스 형태(├──, └──)로 출력.
        - children 순서는 삽입된 순서대로 (CocktailNode.__init__ 시 자동 append).
        """
        def dfs(node, prefix="", is_last=True):
            if node.name != "Empty Glass":
                connector = "└── " if is_last else "├── "
                print(prefix + connector + node.name)
                prefix += "    " if is_last else "│   "
            for i, child in enumerate(node.children):
                dfs(child, prefix, i == len(node.children) - 1)

        dfs(self.root, "", True)

    def find_node_by_name(self, target_name):
        """
        트리 전체에서 이름이 target_name과 일치하는 노드를 (대소문자 무시) 탐색 후 반환.
        못 찾으면 None 반환.
        """
        def dfs(node):
            if node.name.strip().lower() == target_name.strip().lower():
                return node
            for child in node.children:
                result = dfs(child)
                if result:
                    return result
            return None

        return dfs(self.root)

    def find_possible_cocktails(self, my_ingredients):
        """
        my_ingredients: 사용자가 가진 재료 세트 (e.g. {"Gin", "Dry Vermouth", "Olive Brine", "Olive Garnish"})
        - 트리 내의 모든 노드를 DFS 돌며 get_full_ingredients()를 호출 →
          그 결과가 my_ingredients에 모두 포함된다면 '만들 수 있는 칵테일'로 간주.
        - 단, 'Empty Glass' 노드는 제외.
        """
        possible = []

        def dfs(node):
            full_ings = node.get_full_ingredients()
            if node.name != "Empty Glass" and all(ing in my_ingredients for ing in full_ings):
                possible.append(node.name)
            for child in node.children:
                dfs(child)

        dfs(self.root)
        return possible
