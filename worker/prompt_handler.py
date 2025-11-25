"""
Handles complex prompt templates with markdown, special characters, and long context
"""
import re
from typing import Dict, Optional


class PromptHandler:
    """Manages prompt templates and context injection"""

    @staticmethod
    def prepare_prompt(template: str, topic: str, content_type: str) -> str:
        """
        Prepare a prompt by safely replacing {topic} placeholder
        while preserving all markdown and special formatting
        """
        if not template:
            return f"Create content about: {topic}"

        # Preserve the template exactly as is, only replace {topic}
        # Use a more robust replacement that handles edge cases

        # First, escape the topic if it contains special regex characters
        safe_topic = topic.replace("\\", "\\\\").replace('"', '\\"')

        # Replace all variations of {topic} placeholder
        prompt = template
        prompt = prompt.replace("{topic}", safe_topic)
        prompt = prompt.replace("{{topic}}", safe_topic)  # Handle escaped braces
        prompt = prompt.replace("[topic]", safe_topic)  # Alternative format
        prompt = prompt.replace("<<topic>>", safe_topic)  # Alternative format

        # If no placeholder was found, append topic at the end
        if safe_topic not in prompt and topic not in prompt:
            prompt += f"\n\nTopic: {safe_topic}"

        # Add content type context if not already in prompt
        if content_type and content_type.lower() not in prompt.lower():
            type_context = f"\n\nContent Type: {content_type}"
            # Only add if it provides value
            if content_type not in ["mixed", "short_posts"]:
                prompt = type_context + "\n" + prompt

        return prompt

    @staticmethod
    def validate_prompt_length(prompt: str, max_chars: int = 100000) -> bool:
        """
        Check if prompt is within reasonable limits
        Gemini can handle very long prompts but we set a sanity limit
        """
        return len(prompt) <= max_chars

    @staticmethod
    def extract_requirements(prompt: str) -> Dict[str, any]:
        """
        Extract key requirements from prompt for logging/debugging
        """
        requirements = {
            "has_markdown": "##" in prompt or "**" in prompt or "###" in prompt,
            "has_lists": "- " in prompt or "* " in prompt or "1. " in prompt,
            "has_quotes": '"' in prompt or "'" in prompt,
            "length": len(prompt),
            "lines": prompt.count("\n") + 1,
            "has_topic_placeholder": "{topic}" in prompt,
        }
        return requirements

    @staticmethod
    def clean_generated_content(content: str) -> str:
        """
        Clean up generated content while preserving formatting
        """
        # Remove any potential prompt leakage
        # (sometimes models repeat parts of the prompt)

        # Remove common prefixes models add
        prefixes_to_remove = [
            "Here's the content:",
            "Here is the generated content:",
            "Generated content:",
            "Output:",
            "Response:",
        ]

        for prefix in prefixes_to_remove:
            if content.lower().startswith(prefix.lower()):
                content = content[len(prefix) :].strip()

        # Remove excessive newlines (more than 3 in a row)
        content = re.sub(r"\n{4,}", "\n\n\n", content)

        # Ensure content ends with single newline
        content = content.rstrip() + "\n"

        return content

