"""Hook frameworks — opening patterns that win on X/LinkedIn for AI/business/finance.

The researcher/content engine picks a pattern per signal and fills the slots.
Keeping these as data lets the learning loop later reweight which patterns perform.
"""
from __future__ import annotations

HOOK_PATTERNS = {
    "contrarian": {
        "label": "Contrarian take",
        "template": "Everyone says {consensus}. They're wrong. Here's the data:",
        "fields": ["consensus"],
    },
    "missing": {
        "label": "What everyone is missing",
        "template": "The detail everyone is missing about {topic}:",
        "fields": ["topic"],
    },
    "prediction": {
        "label": "Prediction with timeline",
        "template": "Calling it now: {prediction} by {horizon}. Thread of the reasoning:",
        "fields": ["prediction", "horizon"],
    },
    "first_principles": {
        "label": "First-principles breakdown",
        "template": "Let's break {thing} down to first principles:",
        "fields": ["thing"],
    },
    "meta_lesson": {
        "label": "Meta-lesson for builders",
        "template": "What {story} teaches us about building in AI:",
        "fields": ["story"],
    },
    "numbers": {
        "label": "The number that matters",
        "template": "One number explains {situation} better than any headline:",
        "fields": ["situation"],
    },
    "before_after": {
        "label": "Before/after workflow",
        "template": "How I'd do {task} with AI today vs a year ago:",
        "fields": ["task"],
    },
    "story_hook": {
        "label": "Founder/story hook",
        "template": "The {actor} story that everyone in {industry} should read:",
        "fields": ["actor", "industry"],
    },
}


def pick_pattern(weights: dict | None = None) -> str:
    """Pick a hook pattern (default: rotate; learning loop can bias by performance)."""
    import random
    return random.choice(list(HOOK_PATTERNS.keys()))


def render(pattern_name: str, fields: dict) -> str:
    tpl = HOOK_PATTERNS[pattern_name]["template"]
    return tpl.format(**fields)