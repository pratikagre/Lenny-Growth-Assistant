import asyncio
from typing import AsyncGenerator, Dict, Any, List
from .base import BaseLLMProvider

class MockProvider(BaseLLMProvider):
    """
    Deterministic Mock Provider:
    Provides immediate, high-fidelity responses, Ship 30 essays, and interactive artifacts
    for testing, offline evaluation, and zero-downtime demonstration.
    """

    async def generate_response(
        self,
        messages: List[Dict[str, str]],
        system_prompt: str,
        temperature: float = 0.3
    ) -> AsyncGenerator[str, None]:
        user_message = messages[-1].get("content", "").lower() if messages else ""

        if "ship 30" in system_prompt.lower() or "ship30" in system_prompt.lower():
            response_text = (
                "# The Inconvenient Truth About Product Roadmaps\n\n"
                "Most product managers run roadmaps like politicians pleasing constituents.\n\n"
                "They build consensus. They balance priorities. And they slowly kill great products.\n\n"
                "Brian Chesky broke the mold when he rebuilt Airbnb in 2020. He didn't empower hundreds of autonomous teams to drift in different directions. He put the entire company onto one single, unified roadmap.\n\n"
                "## 1. Leaders Must Live in the Details\n\n"
                "There is a pervasive tech myth that great executive leadership is purely about delegating.\n\n"
                "**Micromanagement** is telling people what to do without context.\n"
                "**Detail mastery** is understanding the exact customer journey before signing off.\n\n"
                "As Brian Chesky noted in his conversation on Lenny's Podcast:\n\n"
                "> *'Way too many founders apologize for how they want to run the company... What everyone really wants is clarity. And what everyone really wants is to be able to row in the same direction really quickly.'* [Episode: Brian Chesky’s new playbook, Guest: Brian Chesky, Timestamp: 00:00:38]\n\n"
                "## 2. Eliminate Paid Performance Marketing Traps\n\n"
                "When the pandemic hit, Airbnb turned off nearly all digital performance marketing.\n\n"
                "**Organic brand recall** outlasted ad spend.\n"
                "**Product excellence** drove press and word-of-mouth.\n\n"
                "The result? Traffic returned to 95% of prior levels without Google Ads spending millions. Growth became a byproduct of product distinction.\n\n"
                "## 3. The 3-Step Actionable Implementation Framework\n\n"
                "1. **Consolidate to One Roadmap:** Stop running 14 disjointed team backlogs. Review the top 20 company priorities with design and engineering leads bi-weekly.\n"
                "2. **Elevate Product Marketing:** Integrate outbound narrative into product conception rather than handing off at launch.\n"
                "3. **Measure Word-of-Mouth:** If your users aren't talking to their friends without an incentive code, your core value proposition needs surgery.\n\n"
                "---\n"
                "*Grounded in verified transcripts from Lenny's Podcast archive.*"
            )
        elif "calculator" in user_message or "artifact" in user_message or "html" in user_message or "tool" in user_message:
            response_text = (
                "Here is an interactive **Product-Led Growth (PLG) Loop Calculator** grounded in the growth frameworks discussed by Elena Verna and Brian Balfour on Lenny's Podcast.\n\n"
                "This tool models your Viral Coefficient ($K$-factor), Natural Referral Rate, and Payback Cycles.\n\n"
                '<artifact type="html" title="PLG Viral Loop & Growth Calculator">\n'
                '<!DOCTYPE html>\n'
                '<html lang="en">\n'
                '<head>\n'
                '  <meta charset="UTF-8">\n'
                '  <title>PLG Viral Loop Calculator</title>\n'
                '  <style>\n'
                '    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #0f172a; color: #f8fafc; padding: 24px; margin: 0; }\n'
                '    .card { background: #1e293b; border-radius: 12px; padding: 24px; max-width: 540px; margin: 0 auto; box-shadow: 0 10px 25px rgba(0,0,0,0.3); border: 1px solid #334155; }\n'
                '    h2 { margin-top: 0; color: #38bdf8; font-size: 20px; font-weight: 700; }\n'
                '    p.subtitle { color: #94a3b8; font-size: 13px; margin-bottom: 20px; }\n'
                '    .input-group { margin-bottom: 16px; }\n'
                '    label { display: block; font-size: 13px; font-weight: 600; margin-bottom: 6px; color: #cbd5e1; }\n'
                '    input[type="range"] { width: 100%; accent-color: #38bdf8; }\n'
                '    .val-badge { float: right; color: #38bdf8; font-weight: bold; }\n'
                '    .result-box { background: #0f172a; border-radius: 8px; padding: 16px; margin-top: 24px; border: 1px solid #334155; text-align: center; }\n'
                '    .metric-value { font-size: 32px; font-weight: 800; color: #4ade80; margin: 8px 0; }\n'
                '    .metric-label { font-size: 12px; text-transform: uppercase; letter-spacing: 1px; color: #94a3b8; }\n'
                '    .verdict { font-size: 13px; color: #e2e8f0; margin-top: 10px; line-height: 1.4; }\n'
                '  </style>\n'
                '</head>\n'
                '<body>\n'
                '  <div class="card">\n'
                '    <h2>Product-Led Growth Loop Engine</h2>\n'
                '    <p class="subtitle">Based on Elena Verna & Casey Winters frameworks on Lenny\'s Podcast</p>\n'
                '    <div class="input-group">\n'
                '      <label>Invites Sent per Active User (i): <span class="val-badge" id="invitesVal">4</span></label>\n'
                '      <input type="range" id="invites" min="1" max="15" value="4" oninput="calculate()">\n'
                '    </div>\n'
                '    <div class="input-group">\n'
                '      <label>Invite Acceptance Rate (c %): <span class="val-badge" id="convVal">18%</span></label>\n'
                '      <input type="range" id="conv" min="1" max="50" value="18" oninput="calculate()">\n'
                '    </div>\n'
                '    <div class="input-group">\n'
                '      <label>Monthly Cohort Retention (r %): <span class="val-badge" id="retVal">65%</span></label>\n'
                '      <input type="range" id="ret" min="10" max="95" value="65" oninput="calculate()">\n'
                '    </div>\n'
                '    <div class="result-box">\n'
                '      <div class="metric-label">Viral Coefficient (K-Factor)</div>\n'
                '      <div class="metric-value" id="kFactor">0.72</div>\n'
                '      <div class="verdict" id="verdict">Strong Loop: Sustainable compound organic lift.</div>\n'
                '    </div>\n'
                '  </div>\n'
                '  <script>\n'
                '    function calculate() {\n'
                '      const i = parseFloat(document.getElementById("invites").value);\n'
                '      const c = parseFloat(document.getElementById("conv").value) / 100;\n'
                '      const r = parseFloat(document.getElementById("ret").value) / 100;\n'
                '      document.getElementById("invitesVal").innerText = i;\n'
                '      document.getElementById("convVal").innerText = (c * 100).toFixed(0) + "%";\n'
                '      document.getElementById("retVal").innerText = (r * 100).toFixed(0) + "%";\n'
                '      const k = (i * c).toFixed(2);\n'
                '      document.getElementById("kFactor").innerText = k;\n'
                '      const el = document.getElementById("verdict");\n'
                '      if (k >= 1.0) {\n'
                '        el.innerText = "True Virality (K >= 1.0): Exponential self-sustaining compounding loop!";\n'
                '        document.getElementById("kFactor").style.color = "#22c55e";\n'
                '      } else if (k >= 0.5) {\n'
                '        el.innerText = "High-Leverage Loop (K >= 0.5): Amplifies paid/organic acquisition significantly.";\n'
                '        document.getElementById("kFactor").style.color = "#38bdf8";\n'
                '      } else {\n'
                '        el.innerText = "Sub-critical Loop: Focus on viral exposure mechanisms inside the core workflow.";\n'
                '        document.getElementById("kFactor").style.color = "#f59e0b";\n'
                '      }\n'
                '    }\n'
                '    calculate();\n'
                '  </script>\n'
                '</body>\n'
                '</html>\n'
                '</artifact>\n\n'
                "You can test the interactive calculator in the **Artifact Viewer** to the right!"
            )
        elif "sourdough" in user_message or "bake" in user_message or "recipe" in user_message:
            response_text = (
                "I do not have sufficient information in Lenny's podcast archive to answer this question. "
                "My answers are strictly limited to verified statements and operational frameworks discussed by Lenny Rachitsky and his product, growth, and leadership guests."
            )
        else:
            response_text = (
                "Based on conversations from Lenny's Podcast archive:\n\n"
                "Brian Chesky shared on the podcast that Airbnb fundamentally restructured how product management operated. "
                "Rather than having PMs act as isolated project managers running small, disconnected roadmaps, Chesky combined product management with product marketing, "
                "placing designers and PMs directly into company-wide strategic releases [Episode: Brian Chesky’s new playbook, Guest: Brian Chesky, Timestamp: 00:01:27].\n\n"
                "Key strategic tenets from the conversation:\n"
                "- **Single Shared Roadmap:** The entire company aligns around a bi-annual release cycle.\n"
                "- **Design-Led Product:** Product managers must collaborate intimately with design before engineering commits.\n"
                "- **Deep Executive Details:** Leaders stay close to the product details rather than delegating blindly [Episode: Brian Chesky’s new playbook, Guest: Brian Chesky, Timestamp: 00:00:38]."
            )

        # Stream words with small micro-delay to simulate realistic token streaming
        words = response_text.split(" ")
        for i, word in enumerate(words):
            yield word + (" " if i < len(words) - 1 else "")
            await asyncio.sleep(0.015)

    async def check_health(self) -> Dict[str, Any]:
        return {
            "status": "ready",
            "available": True,
            "provider": "mock",
            "description": "Deterministic offline mock provider"
        }
