# Tests

Run all tests:

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

This suite currently includes:
- project-wide smoke compile tests for all Python files
- `pybuspro` unit tests (generics, telegram helper, control dedup)
- Home Assistant-facing flow tests (user/options/reconfigure)
- integration setup tests (`async_setup_entry` options override)
