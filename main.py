from openai import OpenAI, RateLimitError, APIError
from config import (
    API_KEY,
    BASE_URL,
    MODEL,
    INSTRUCTIONS,
    MAX_CONTEXT_MESSAGES,
    MAX_OUTPUT_TOKENS,
)
from state_manager import load_history, save_history, append_message, build_model_context
from telemetry import print_telemetry

client = OpenAI(api_key=API_KEY, base_url=BASE_URL, max_retries=0)


def main() -> None:
    history = load_history()
    stateless_mode = False
    last_response = None

    print("lessgooo")
    print("Commands: /stateless, /context, /raw, /reset, /exit\n")

    while True:
        user_input = input("You: ").strip()
        if not user_input:
            continue

        if user_input == "/exit":
            break
        elif user_input == "/reset":
            history = []
            save_history(history)
            print("[All Cleared]\n")
            continue
        elif user_input == "/stateless":
            stateless_mode = not stateless_mode
            print(f"[stateless mode = {stateless_mode}]\n")
            continue
        elif user_input == "/context":
            ctx = build_model_context(history, MAX_CONTEXT_MESSAGES, stateless=stateless_mode)
            print(f"\n[Full app history messages: {len(history)} | Model context messages sent: {len(ctx)}]")
            for item in ctx:
                print(f"  - {item['role']}: {item['content'][:80]}")
            print()
            continue
        elif user_input == "/raw":
            if last_response is None:
                print("[No response yet]\n")
            else:
                print(last_response.model_dump_json(indent=2))
            continue

        append_message(history, "user", user_input)
        context_to_send = build_model_context(history, MAX_CONTEXT_MESSAGES, stateless=stateless_mode)
        messages_payload = [{"role": "system", "content": INSTRUCTIONS}, *context_to_send]

        print("Sending request...", flush=True)
        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=messages_payload,
                max_tokens=MAX_OUTPUT_TOKENS,
                timeout=30,
                stream = True #initializes streaming of resposne. 
            )

        except (RateLimitError, APIError) as e:
            history.pop()
            save_history(history)
            print(f"\n[API Error]: {type(e).__name__}: {e}\n")
            continue 

        reply_parts = []

        print("Assistant: ", end="", flush=True)

        for chunk in response:
            if not chunk.choices:
                continue
            token = chunk.choices[0].delta.content
            if token:
                print(token, end="", flush=True)
                reply_parts.append(token)
        print("\n")

        reply_text = "".join(reply_parts)
        append_message(history, "assistant", reply_text)
        print(response)


if __name__ == "__main__":
    main()
