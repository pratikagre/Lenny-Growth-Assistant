import re
from typing import List, Dict, Any, Tuple

ARTIFACT_SYSTEM_INSTRUCTION = """
### Artifact Generation Guidelines:
When the user requests an interactive tool, calculator, visual component, dashboard, or standalone document, create it as a distinct **Artifact**.
Use the following exact XML wrapper tags:

<artifact type="html" title="Short Descriptive Title">
<!DOCTYPE html>
<html>
... complete standalone HTML with inline CSS and JavaScript ...
</html>
</artifact>

OR for pure formatted documents/playbooks:

<artifact type="markdown" title="Short Descriptive Title">
# Document Title
... content ...
</artifact>

Rules for HTML Artifacts:
1. Make them self-contained: include all CSS in a `<style>` block and all interactivity in a `<script>` block.
2. Use clean, modern styling (sleek dark/light themes, smooth transitions, responsive layouts).
3. Do not assume external network scripts are loaded; write vanilla JS or self-contained logic.
"""

ARTIFACT_REGEX = re.compile(
    r'<artifact\s+type=[\'"](?P<type>html|markdown)[\'"]\s+title=[\'"](?P<title>[^\'"]+)[\'"]>(?P<content>.*?)(?:</artifact>|$)',
    re.DOTALL | re.IGNORECASE
)

def extract_artifacts(text: str) -> Tuple[str, List[Dict[str, str]]]:
    """
    Parses any <artifact> tags out of the LLM completion text.
    Returns: (cleaned_message_text, list_of_artifacts)
    """
    artifacts = []
    
    for match in ARTIFACT_REGEX.finditer(text):
        art_type = match.group("type").lower()
        title = match.group("title").strip()
        content = match.group("content").strip()

        # Clean up any trailing incomplete tags
        if content.endswith("</artifact>"):
            content = content[:-11].strip()

        artifacts.append({
            "type": art_type,
            "title": title,
            "content": content
        })

    # In the cleaned text, we can leave the text or replace with an artifact card indicator
    cleaned_text = ARTIFACT_REGEX.sub(r'\n\n*[Interactive Artifact Generated: "\g<title>"]*\n\n', text).strip()
    return cleaned_text, artifacts
