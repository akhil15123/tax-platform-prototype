"""Validate the zero-build prototype's essential document structure."""

from html.parser import HTMLParser
from pathlib import Path


class PrototypeParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: set[str] = set()
        self.duplicate_ids: set[str] = set()
        self.has_title = False
        self.has_script = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        if attributes.get("id"):
            if attributes["id"] in self.ids:
                self.duplicate_ids.add(attributes["id"])
            self.ids.add(attributes["id"])
        self.has_title |= tag == "title"
        self.has_script |= tag == "script"


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    document = (root / "index.html").read_text(encoding="utf-8")
    parser = PrototypeParser()
    parser.feed(document)
    assert parser.has_title, "index.html needs a title"
    assert parser.has_script, "interactive prototype script is missing"
    assert not parser.duplicate_ids, f"duplicate HTML ids: {parser.duplicate_ids}"
    assert "priorityScore" in document, "priority-ranking logic is missing"
    assert "console.assert" in document, "embedded self-checks are missing"
    print(f"Validated prototype HTML with {len(parser.ids)} unique element ids")


if __name__ == "__main__":
    main()
