import sys
import json
from src.rag.policy_rag import query_policy
from src.detectors.conspiracy import detect_conspiracy
from src.detectors.audit_rules import audit_rules
from src.detectors.audit_context import audit_context

def main():
    if len(sys.argv) < 2:
        print("Uso:")
        print("  python -m src.app policy \"pergunta\"")
        print("  python -m src.app conspiracy")
        print("  python -m src.app audit_rules")
        print("  python -m src.app audit_context")
        sys.exit(1)

    cmd = sys.argv[1].lower()

    if cmd == "policy":
        if len(sys.argv) < 3:
            print("Uso: python -m src.app policy \"pergunta\"")
            sys.exit(1)
        question = " ".join(sys.argv[2:])
        out = query_policy(question)
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return

    if cmd == "conspiracy":
        out = detect_conspiracy()
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return

    if cmd == "audit_rules":
        out = audit_rules()
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return

    if cmd == "audit_context":
        out = audit_context()
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return

    print("Comando desconhecido:", cmd)
    sys.exit(1)

if __name__ == "__main__":
    main()
