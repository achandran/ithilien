"""Run the complete Ithilien audit and generation pipeline."""

from audit_palette import main as audit
from generate_themes import main as generate
from audit_dusk import main as audit_dusk


if __name__ == "__main__":
    audit("ithilien-dawn")
    audit_dusk()
    generate()
