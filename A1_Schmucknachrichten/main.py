import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--file", required=True, help="Pfad zur Eingabedatei")
args = parser.parse_args()

with open(args.file, "r", encoding="utf-8") as file:
    count = int(file.readline().strip())
    sizes = list(map(int, file.readline().strip().split()))
    message = file.readline().strip()

print("Count:", count)
print("Sizes:", sizes)
print("Message:", message)
