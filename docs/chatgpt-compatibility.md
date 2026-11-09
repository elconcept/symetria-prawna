# Kompatybilność ChatGPT web

Od 0.4.2 i w 0.5.0 instalacja jest skills-only: brak mcp.json, .mcp.json oraz requires_local_executor. Zachowujemy repozytoryjny kod lokalnego MCP wyłącznie jako narzędzie uruchamiane osobno. Nie podpinaj go przez stdio do ChatGPT web. W 0.5.0 jest jeden skill z implicit invocation; nie jest to gwarantowany hook przed wysłaniem odpowiedzi. Weryfikuj manifest testem scripts/verify_marketplaces.py oraz sesje użytkowe benchmarkiem docs/activation-benchmark.md.
