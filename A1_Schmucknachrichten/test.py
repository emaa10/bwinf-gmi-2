import heapq
from collections import defaultdict

class Node:
    def __init__(self, freq, cost=0, char=None):
        self.freq = freq
        self.cost = cost
        self.char = char
        self.children = []

    def __lt__(self, other):
        if self.cost == other.cost:
            return self.freq < other.freq  # Tiebreaker: Niedrigere Frequenz zuerst
        return self.cost < other.cost

def build_nary_huffman(freq_dict, diameters, n):
    heap = []
    for char, freq in freq_dict.items():
        heapq.heappush(heap, Node(freq, 0, char))

    # Dummy-Knoten hinzufügen
    num_nodes = len(heap)
    d = (n - 1 - (num_nodes - 1) % (n - 1)) % (n - 1)
    min_diameter = min(diameters)
    for _ in range(d):
        heapq.heappush(heap, Node(0, 0))

    diameters = sorted(diameters)  # Aufsteigend sortiert

    while len(heap) > 1:
        nodes = heapq.nsmallest(n, heap, key=lambda x: x.cost)
        for node in nodes:
            heap.remove(node)
        
        # Sortiere Knoten nach Häufigkeit (absteigend)
        nodes_sorted = sorted(nodes, key=lambda x: -x.freq)
        assigned_diameters = diameters[:len(nodes)]  # Kleinste Durchmesser zuweisen

        # Berechne Kosten
        cost_increment = sum(node.freq * diam for node, diam in zip(nodes_sorted, assigned_diameters))
        combined_cost = sum(node.cost for node in nodes_sorted) + cost_increment
        
        # Erstelle Elternknoten
        parent = Node(sum(node.freq for node in nodes_sorted), combined_cost)
        parent.children = list(zip(assigned_diameters, nodes_sorted))
        heapq.heappush(heap, parent)
    
    return heap[0] if heap else None

def generate_codes(root):
    codes = {}
    def traverse(node, code_str, current_diameters):
        if node.char is not None:
            codes[node.char] = (code_str, current_diameters.copy())
            return
        for i, (diam, child) in enumerate(node.children):
            traverse(child, code_str + str(i), current_diameters + [diam])
    if root:
        traverse(root, "", [])
    return codes

def generate_codes(root):
    codes = {}
    def traverse(node, code_str, current_diameters):
        if node.char is not None:
            codes[node.char] = (code_str, current_diameters.copy())
            return
        for i, (diam, child) in enumerate(node.children):
            current_diameters.append(diam)
            traverse(child, code_str + str(i), current_diameters)
            current_diameters.pop()
    if root:
        traverse(root, "", [])
    return codes

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=str, help="Pfad zur Eingabedatei")
    args = parser.parse_args()

    if args.file:
        with open(args.file, 'r', encoding='utf-8') as f:
            lines = f.read().splitlines()
            k = int(lines[0].strip())
            diameters = list(map(float, lines[1].strip().split()))
            text = " ".join(lines[2:]).replace("\n", " ")
    else:
        k = int(input("Anzahl der Farben: "))
        diameters = list(map(float, input("Durchmesser der Farben (leer-getrennt): ").split()))
        text = input("Text: ")

    freq = defaultdict(int)
    for char in text:
        freq[char] += 1

    root = build_nary_huffman(freq, diameters, k)
    codes = generate_codes(root)

    total = sum(sum(diam_list) * freq[char] for char, (_, diam_list) in codes.items())

    print("\nCodetabelle:")
    for char in sorted(codes.keys()):
        code_str, diam_list = codes[char]
        diam_str = "+".join(map(str, diam_list)) if diam_list else "0"
        print(f"{repr(char)[1:-1]}: Code={code_str} (Durchmesser: {diam_str})")
    print(f"\nGesamtlänge: {total:.1f} mm")

if __name__ == "__main__":
    main()
