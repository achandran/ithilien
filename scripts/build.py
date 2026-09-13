"""Run the complete Ithilien audit and generation pipeline."""

from audit_palette import main as audit
from generate_themes import main as generate


if __name__ == "__main__":
    audit("ithilien-dawn")
    generate()

    from generate_preview import main as generate_preview
    generate_preview()
