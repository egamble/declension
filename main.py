# main.py
from sentence import generate_sentence
from diagnose import diagnose

def main():
    print("=== German Declension Trainer ===")
    print("Type 'quit' or 'exit' to stop.\n")

    score = 0
    total = 0

    while True:
        data = generate_sentence()
        print("EN:", data["english"])

        try:
            from prompt_toolkit import prompt
            user = prompt("DE: ")
        except ImportError:
            user = input("DE: ")

        if user.lower() in ("quit", "exit"):
            print(f"Final score: {score}/{total}")
            break

        total += 1
        result = diagnose(user, data["german_correct"], data["meta"])
        if "✅" in result:
            score += 1

        print(result)
        print(f"Score: {score}/{total}\n")

if __name__ == "__main__":
    main()
