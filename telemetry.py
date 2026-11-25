def print_telemetry(response) -> None:
    usage = getattr(response, "usage", None)
    input_tokens = getattr(usage, "prompt_tokens", "N/A")
    output_tokens = getattr(usage, "completion_tokens", "N/A")
    total_tokens = getattr(usage, "total_tokens", "N/A")

    choice = response.choices[0] if getattr(response, "choices", None) else None
    finish_reason = getattr(choice, "finish_reason", "unknown")

    print("\n--- Telemetry ---")
    print(f"Model: {getattr(response, 'model', 'N/A')} | Finish reason: {finish_reason}")
    print(f"Tokens -> input: {input_tokens} | output: {output_tokens} | total: {total_tokens}")
    print("-----------------\n")