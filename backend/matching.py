from math import sqrt
from typing import Dict, List


def euclidean_distance(x1: float, y1: float, x2: float, y2: float) -> float:
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def score_edge(item: Dict, request: Dict) -> float:
    if item["status"] != "disponivel":
        return -1
    if request["status"] != "aberta":
        return -1
    if item["category"] != request["category"]:
        return -1

    distance = euclidean_distance(item["x"], item["y"], request["x"], request["y"])
    quantity_bonus = min(item["quantity"], request["needed_quantity"])
    # Grafo ponderado: maior pontuacao significa maior compatibilidade entre no do item e no da necessidade.
    return (quantity_bonus * 10) - distance


def build_matches(items: List[Dict], requests: List[Dict], max_distance: float | None = None) -> List[Dict]:
    edges = []
    for item in items:
        for request in requests:
            score = score_edge(item, request)
            if score < 0:
                continue
            distance = euclidean_distance(item["x"], item["y"], request["x"], request["y"])
            if max_distance is not None and distance > max_distance:
                continue
            edges.append(
                {
                    "item_id": item["id"],
                    "request_id": request["id"],
                    "distance": round(distance, 2),
                    "score": round(score, 2),
                    "allocated_quantity": min(item["quantity"], request["needed_quantity"]),
                    "category": item["category"],
                }
            )

    # Aproximacao gulosa de matching em grafo bipartido: seleciona as arestas com maior score sem repetir nos.
    edges.sort(key=lambda edge: (-edge["score"], edge["distance"]))
    used_items = set()
    used_requests = set()
    matches = []
    for edge in edges:
        if edge["item_id"] in used_items or edge["request_id"] in used_requests:
            continue
        used_items.add(edge["item_id"])
        used_requests.add(edge["request_id"])
        matches.append(edge)
    return matches

