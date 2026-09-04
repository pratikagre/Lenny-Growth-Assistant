import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.skills.artifact_generator import extract_artifacts

def test_extract_artifacts():
    sample_text = (
        "Here is your interactive ROI calculator:\n\n"
        '<artifact type="html" title="PLG Calculator">\n'
        '<!DOCTYPE html><html><body><h1>Calculator</h1></body></html>\n'
        '</artifact>\n\n'
        "Let me know if you need any adjustments."
    )
    cleaned, artifacts = extract_artifacts(sample_text)
    assert len(artifacts) == 1
    assert artifacts[0]["type"] == "html"
    assert artifacts[0]["title"] == "PLG Calculator"
    assert "<h1>Calculator</h1>" in artifacts[0]["content"]
    assert '<artifact' not in cleaned
    assert "Interactive Artifact Generated" in cleaned

def test_extract_markdown_artifact():
    sample_text = (
        "Here is the strategy document:\n\n"
        '<artifact type="markdown" title="Growth Strategy Playbook">\n'
        '# Strategy Playbook\n'
        '1. Consolidate roadmap\n'
        '2. Drive organic loops\n'
        '</artifact>'
    )
    cleaned, artifacts = extract_artifacts(sample_text)
    assert len(artifacts) == 1
    assert artifacts[0]["type"] == "markdown"
    assert artifacts[0]["title"] == "Growth Strategy Playbook"
    assert "Consolidate roadmap" in artifacts[0]["content"]
