# Contributing

Thanks for your interest in improving `unicode-animations`.

## Ground Rules

- Be respectful and collaborative. Please follow the
  [Code of Conduct](CODE_OF_CONDUCT.md).
- Keep pull requests focused and small when possible.
- Include tests for behavior changes.

## Development Setup

From the project root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -e ".[dev]"
```

## Running Tests

```bash
python3 -m pytest -q
python3 -m ruff check .
```

## Running the Demos

Terminal demo (Python API):

```bash
python examples/terminal_demo.py
```

CLI demo:

```bash
unicode-animations --list
unicode-animations helix
unicode-animations --web
```

## Release-shaped validation

```bash
python3 scripts/release_check.py
```

## Pull Request Checklist

- [ ] Code is readable and follows existing project style
- [ ] Tests pass locally (`pytest`)
- [ ] New behavior is covered by tests
- [ ] Documentation is updated when needed

## Reporting Issues

If you find a bug or have a feature request, please open an issue with:

- What you expected to happen
- What happened instead
- Steps to reproduce
- Python version and OS details

## License

By contributing to this project, you agree that your contributions will be
licensed under the [MIT License](LICENSE).
