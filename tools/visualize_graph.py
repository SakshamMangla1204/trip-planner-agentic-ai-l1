"""
Graph Visualization Utility for LangGraph Workflows.

Generates Mermaid and PNG visualizations of a compiled LangGraph
without running the full application. Designed for development
and debugging purposes.
"""

import logging
import sys
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# Logging Configuration
# ---------------------------------------------------------------------------

logger = logging.getLogger("visualize_graph")
logger.setLevel(logging.INFO)

_console_handler = logging.StreamHandler(sys.stdout)
_console_handler.setLevel(logging.INFO)
_formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
_console_handler.setFormatter(_formatter)
if not logger.handlers:
    logger.addHandler(_console_handler)

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = PROJECT_ROOT / "docs"
MERMAID_FILE = DOCS_DIR / "workflow.mmd"
PNG_FILE = DOCS_DIR / "workflow.png"


def ensure_docs_dir() -> None:
    """Create the docs/ directory if it does not already exist."""
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    logger.info("Ensured docs directory exists at: %s", DOCS_DIR)


def build_graph():
    """
    Build and return the compiled LangGraph.

    Imports happen inside this function so that the module can be
    imported without triggering the full instrumentation chain.
    """
    # Ensure the project root is on sys.path so 'graph' can be imported
    import sys as _sys
    if str(PROJECT_ROOT) not in _sys.path:
        _sys.path.insert(0, str(PROJECT_ROOT))

    # Suppress Phoenix/OpenTelemetry logs during import
    logging.getLogger("phoenix").setLevel(logging.WARNING)
    logging.getLogger("opentelemetry").setLevel(logging.WARNING)

    import graph as graph_module  # type: ignore[import-untyped]
    return graph_module.build_graph()


def export_mermaid(compiled_graph) -> str:
    """
    Export the compiled graph as a Mermaid diagram string.

    Args:
        compiled_graph: The compiled LangGraph instance.

    Returns:
        Mermaid diagram source code.
    """
    mermaid_source: str = compiled_graph.get_graph().draw_mermaid()
    logger.info("Mermaid diagram generated (%d characters)", len(mermaid_source))
    return mermaid_source


def save_mermaid(mermaid_source: str, path: Path = MERMAID_FILE) -> None:
    """
    Write the Mermaid source to a file.

    Args:
        mermaid_source: Mermaid diagram source code.
        path: Destination file path.
    """
    path.write_text(mermaid_source, encoding="utf-8")
    logger.info("Mermaid file saved: %s", path)


def export_png(compiled_graph, path: Path = PNG_FILE) -> bool:
    """
    Generate a PNG image of the graph using LangGraph's built-in renderer.

    Args:
        compiled_graph: The compiled LangGraph instance.
        path: Destination file path for the PNG image.

    Returns:
        True if the PNG was generated successfully, False otherwise.
    """
    try:
        png_data: bytes = compiled_graph.get_graph().draw_mermaid_png()
        path.write_bytes(png_data)
        logger.info("PNG image saved: %s", path)
        return True
    except Exception as exc:
        logger.warning("PNG generation skipped: %s", exc)
        return False


def main() -> None:
    """
    Entry point for the visualization utility.

    Workflow:
        1. Ensure docs/ directory exists.
        2. Build the compiled graph from graph.py.
        3. Export the graph as a Mermaid diagram.
        4. Save the Mermaid diagram to docs/workflow.mmd.
        5. Attempt to export a PNG image; gracefully skip if unavailable.
        6. Print a summary of the generated outputs.
    """
    logger.info("=" * 40)
    logger.info("LangGraph Visualization Utility")
    logger.info("=" * 40)

    # Step 1: Ensure output directory exists
    ensure_docs_dir()

    # Step 2: Build the graph
    try:
        logger.info("Building compiled graph from graph.py …")
        compiled_graph = build_graph()
        logger.info("Graph built successfully.")
    except Exception as exc:
        logger.error("Failed to build graph: %s", exc)
        sys.exit(1)

    # Step 3 & 4: Export & save Mermaid
    try:
        mermaid_source = export_mermaid(compiled_graph)
        save_mermaid(mermaid_source, MERMAID_FILE)
    except Exception as exc:
        logger.error("Failed to generate or save Mermaid diagram: %s", exc)
        sys.exit(1)

    # Step 5: PNG generation (best-effort)
    png_generated = export_png(compiled_graph, PNG_FILE)

    # Step 6: Summary output
    print()
    print("=" * 40)
    print("LangGraph Visualization Generated")
    print("=" * 40)
    print()
    print("Mermaid:")
    print(f"  {MERMAID_FILE}")
    print()
    print("PNG:")
    if png_generated:
        print(f"  {PNG_FILE}")
    else:
        print("  PNG generation skipped because required dependency is unavailable.")
    print()


if __name__ == "__main__":
    main()