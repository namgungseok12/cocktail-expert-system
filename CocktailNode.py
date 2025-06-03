# CocktailNode.py

class CocktailNode:
    """
    트리의 각 노드를 나타내는 클래스.
    - name: 칵테일 이름 혹은 분기 이름 (예: "Dry Martini", "Dirty Martini" 등)
    - parent: 부모 노드를 가리키는 참조
    - ingredients: "이 노드(칵테일)를 만들기 위해 필요한 재료 리스트"
    - children: 자식 노드 리스트
    """

    def __init__(self, name, parent=None, ingredients=None):
        self.name = name.strip()
        self.parent = parent
        self.ingredients = ingredients or []
        self.children = []

        # 부모가 있으면 자동으로 부모.children에 추가
        if parent:
            parent.children.append(self)

    def get_full_ingredients(self):
        """
        이 노드(칵테일)를 만들기 위해 필요했던 모든 재료를 순서대로 반환.
        1) 맨 먼저, 루트(Empty Glass) 바로 아래에 있는 '기본술(예: Gin, Vodka, Tequila, Whiskey)' 이름을 포함시킨다.
        2) 그다음, 이 노드를 만들기 위해 각 분기(edge)별로 추가된 재료(ingredient)를
           조상(ancestor) 노드 순서대로 (상위 → 하위) 합친다.
        → 이렇게 해서 최종 리스트: ["기본술", "Dry Vermouth", "Olive Brine", "Olive Garnish"] 같은 형태로 출력.
        """

        # 1) 기본술(Spirit) 찾기:
        #    self에서 위로 거슬러 올라가다가 '부모가 Empty Glass'인 노드를 찍는다.
        spirit_name = None
        node = self
        while node.parent:
            if node.parent.name == "Empty Glass":
                spirit_name = node.name
                break
            node = node.parent

        # 2) 재료(ingredient) 합치기
        #    가장 상위(루트 직계) 노드에서부터 내려오도록,
        #    self를 루트 방향으로 순회하며 node.ingredients를 모았다가 뒤집는다.
        stack = []
        node = self
        while node and node.name != "Empty Glass":
            if node.ingredients:
                # 각 노드에 붙어 있는 재료(ingredient) 리스트가 있다면,
                # 순서를 위해 스택에 넣어두고 나중에 뒤집는다.
                stack.append(list(node.ingredients))
            node = node.parent

        # 결과를 담을 리스트
        full_ings = []
        if spirit_name:
            full_ings.append(spirit_name)

        # 스택에 들어있던 ingredient 리스트들을 LIFO형으로 꺼내어 순서대로 extend
        while stack:
            ings = stack.pop()
            full_ings.extend(ings)

        return full_ings

    def __repr__(self):
        return f"<CocktailNode {self.name}>"
