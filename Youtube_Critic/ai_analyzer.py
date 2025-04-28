# ai_analyzer.py
import google.generativeai as genai
import config # To get model name and generation config
import json # To potentially parse the JSON response later if needed

def configure_genai(api_key):
    """Configures the Google Generative AI client."""
    try:
        genai.configure(api_key=api_key)
        print("Generative AI client configured.")
    except Exception as e:
        print(f"FATAL: Failed to configure Generative AI: {e}")
        raise SystemExit(f"Could not configure Generative AI: {e}")


def build_genai_model():
    """Builds and returns the Generative AI model instance."""
    try:
        model = genai.GenerativeModel(
            model_name=config.AI_MODEL_NAME,
            generation_config=config.GENERATION_CONFIG,
            # safety_settings= Adjust safety settings if needed
        )
        print(f"Generative AI model '{config.AI_MODEL_NAME}' initialized.")
        return model
    except Exception as e:
        print(f"FATAL: Failed to initialize Generative AI model '{config.AI_MODEL_NAME}': {e}")
        raise SystemExit(f"Could not build Generative AI model: {e}")


def analyze_transcripts(model, channel_name, combined_transcript_text):
    """
    Sends transcript text to the AI model for critique using a detailed prompt
    and expects a JSON response.
    """
    if not combined_transcript_text:
        print(f"  Skipping AI analysis for '{channel_name}' - No transcript text provided.")
        # Return a JSON-like error string for consistency
        return json.dumps({
            "error": "AI Analysis Skipped",
            "channel_name": channel_name,
            "reason": "No transcript text available."
        }, indent=2)

    print(f"  Analyzing transcripts for '{channel_name}' with AI (expecting JSON)...")

    # --- Enhanced Prompt Definition ---
    prompt = f"""
Act as an insightful YouTube Content Strategist & Critic. Your mission is to evaluate the channel '{channel_name}' by analyzing the textual blueprint provided – the combined transcripts of several videos. You must distill the essence of the channel's communication style and effectiveness *solely* from this text.

**Evaluation Criteria:**

Carefully assess the transcripts based on the following criteria. Use *only* the specified rating scale: **Poor, Fair, Good, Excellent**.

1.  **Clarity & Conciseness:**
    *   **Focus:** How effectively is information conveyed? Is the language precise? Are complex topics broken down logically? Is there minimal rambling or unnecessary jargon?
    *   **Ratings:**
        *   `Poor`: Confusing, overly verbose, hard to follow.
        *   `Fair`: Generally understandable but often unclear or wordy.
        *   `Good`: Clear explanations, mostly concise, logical flow.
        *   `Excellent`: Exceptionally clear, succinct, breaks down complexity masterfully.

2.  **Engagement & Flow:**
    *   **Focus:** Does the text read in an interesting way? Does it use rhetorical questions, varied sentence structure, or storytelling elements (even small ones) to maintain interest? Are transitions between ideas smooth?
    *   **Ratings:**
        *   `Poor`: Monotonous, dry, abrupt transitions, lacks engaging elements.
        *   `Fair`: Some attempts at engagement but often falls flat; flow is inconsistent.
        *   `Good`: Generally engaging, reads well, mostly smooth transitions.
        *   `Excellent`: Captivating text, natural rhythm, uses engaging techniques effectively, seamless flow.

3.  **Authenticity & Personality:**
    *   **Focus:** Does the text sound like a genuine human voice with a distinct style, or does it feel generic, overly scripted, or potentially AI-generated? Is passion or unique perspective evident?
    *   **Ratings:**
        *   `Poor`: Sounds robotic, generic, lacks any discernible personality. Strong AI-generation suspicion.
        *   `Fair`: Reads like a standard script; little unique voice or personality.
        *   `Good`: Sounds like a real person; some unique style or passion comes through.
        *   `Excellent`: Distinct, authentic voice shines through; feels genuine and relatable.

4.  **Structure & Coherence:**
    *   **Focus:** How well-organized is the information within the transcripts provided? Is there a clear logical progression of ideas? Can you identify patterns like introductions, supporting points, and conclusions (even if informal)?
    *   **Ratings:**
        *   `Poor`: Disorganized, jumps between topics illogically, hard to see structure.
        *   `Fair`: Some structure is present but often inconsistent or unclear.
        *   `Good`: Mostly well-structured, logical progression is apparent.
        *   `Excellent`: Clearly and logically structured, easy to follow the argument or explanation.

**Output Format:**

Generate a **valid JSON object** containing your critique. Adhere strictly to this format, using the exact keys and rating scale provided. **Do not include ```json ``` markers or any text outside the JSON object itself.**

```json
{{
  "channel_name": "{channel_name}",
  "overall_impression": "A brief (1-2 sentence) summary of the channel's communication style based *only* on the transcripts.",
  "critique_based_on_transcripts": {{
    "clarity_conciseness": "(Poor | Fair | Good | Excellent)",
    "engagement_flow": "(Poor | Fair | Good | Excellent)",
    "authenticity_personality": "(Poor | Fair | Good | Excellent)",
    "structure_coherence": "(Poor | Fair | Good | Excellent)"
  }},
  "analysis_highlights": {{
    "standout_feature_textual": "Identify one positive aspect evident *from the text* (e.g., 'exceptionally clear analogies', 'strong narrative hook in intros'). If none, state 'None discernible'.",
    "area_for_improvement_textual": "Identify one area needing improvement based *only on the text* (e.g., 'tendency to ramble', 'abrupt topic shifts', 'overly generic language'). If none, state 'None discernible'."
  }},
  "confidence_note": "A mandatory note acknowledging the limitations: 'Critique based solely on provided text transcripts. Visuals, delivery, and audio nuances are not assessed.'"
}}
Transcripts to Analyze:

--- START OF COMBINED VIDEO TRANSCRIPTS ---
{combined_transcript_text}
--- END OF COMBINED VIDEO TRANSCRIPTS ---

Now, provide the JSON critique for '{channel_name}'.
"""
    # --- End of Enhanced Prompt Definition ---
    try:
        response = model.generate_content(prompt)

        # The response should be directly usable JSON text because of the mime_type setting
        critique_json_text = response.text

        # Optional: Validate if it's proper JSON before saving
        try:
            # This just checks if it parses, doesn't modify the string
            json.loads(critique_json_text)
            print(f"  AI analysis complete for '{channel_name}' (JSON validated).")
            return critique_json_text
        except json.JSONDecodeError as json_err:
            print(f"  WARNING: AI response for '{channel_name}' was NOT valid JSON. Error: {json_err}")
            print(f"  Raw AI Response:\n---\n{critique_json_text}\n---")
            # Return a JSON-like error string instead
            return json.dumps({
                "error": "AI Analysis Failed",
                "channel_name": channel_name,
                "reason": "AI did not return valid JSON.",
                "raw_response": critique_json_text # Include raw response for debugging
            }, indent=2)

    except Exception as e:
        print(f"  ERROR during AI analysis call for '{channel_name}': {e}")
        # Log the specific error for debugging
        return json.dumps({
            "error": "AI Analysis Failed",
            "channel_name": channel_name,
            "reason": f"An exception occurred: {type(e).__name__}"
        }, indent=2)