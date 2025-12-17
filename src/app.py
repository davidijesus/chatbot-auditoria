import sys
import json
from src.rag.policy_rag import query_policy

def main():
    if len(sys.argv) < 3:
        print("Digite: python -m src.app policy \"sua pergunta\"")
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == "policy":
        question = " ".join(sys.argv[2:])
        out = query_policy(question)
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return

    print("Comando desconhecido:", cmd)
    sys.exit(1)

if __name__ == "__main__":
    main()
