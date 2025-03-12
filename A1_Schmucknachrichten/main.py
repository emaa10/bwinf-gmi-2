import argparse
import heapq

parser = argparse.ArgumentParser()
parser.add_argument("--file", required=True, help="Pfad zur Eingabedatei")
args = parser.parse_args()

with open(args.file, "r", encoding="utf-8") as file:
    count = int(file.readline().strip())
    sizes = list(map(int, file.readline().strip().split()))
    message = file.readline().strip()

count_dict = {}
for char in message:
    if(char in count_dict):
        count_dict[char] += 1
    else:
        count_dict[char] = 1

counts = []
for char, count in count_dict.items():
    counts.append([char, count])
    
counts.sort(key=lambda x: x[1], reverse=True)


print("Count:", count)
print("Sizes:", sizes)
print("Message:", message)
print("Häufigkeiten:", counts)
