"""Run the complete Ithilien audit and generation pipeline."""

from audit_palette import main as audit
from generate_themes import main as generate


if __name__ == "__main__":
    audit("ithilien-dusk")
    audit("ithilien-dawn")
    generate()

    from generate_readme import main as generate_readme
    generate_readme()
