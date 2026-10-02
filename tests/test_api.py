# Optional starter test file.
# Run with: pytest

def test_project_structure():
    from pathlib import Path

    root = Path(__file__).resolve().parents[1]
    assert (root / "backend" / "main.py").exists()
    assert (root / "backend" / "routes.py").exists()
    assert (root / "frontend" / "app.py").exists()
