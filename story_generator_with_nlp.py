import spacy
import language_tool_python

# Load spaCy English model
nlp = spacy.load("en_core_web_sm")

# Language tool for grammar correction
tool = language_tool_python.LanguageTool('en-US')

def smart_story(prompt):
    # NLP noun chunk extraction
    doc = nlp(prompt)
    keywords = [chunk.text.strip() for chunk in doc.noun_chunks][:3]

    # Construct user story
    user_story = f"As a user, I want to {prompt.lower()} so that I can achieve better outcomes."
    dev_story = f"Developer needs to implement functionality related to: {', '.join(keywords)}."

    # Acceptance Criteria as Gherkin
    ac = f"""
Feature: {keywords[0] if keywords else 'User need'}

  Scenario: Implement the feature
    Given the user has access
    When they try to {prompt.lower()}
    Then it should succeed
"""

    # Grammar correction
    user_story = tool.correct(user_story)
    dev_story = tool.correct(dev_story)

    return user_story.strip(), dev_story.strip(), ac.strip()
