from google import genai
from google.genai import types
from pathlib import Path
from dotenv import load_dotenv
import os  
from load_config import *

load_dotenv()

def generate():
    client = genai.Client(
        api_key=GOOGLE_API_KEY,
    )

    # Path to the input file
    input_path = FINAL_RESULT_FILE

    # Read the logical statement from the specified file
    with open(input_path, 'r', encoding='utf-8') as file:
        logical_statement = file.read().strip()

    model = NL_MODEL
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=f"""Guideline for Natural Language Specification:
1.the Logical Statement:
{logical_statement}

2. Step 1: Logical Decomposition
o Expert A (Simplified Language):
  Role: Provide an initial breakdown in simplified terms, focusing on
  clarity and understanding.
  Focus: Break down the logical statement into manageable conditions
  while retaining the core meaning.
  Simplified Translation: Identify the core conditions (such as modes,
  states, inputs) and break them into key criteria for the transition.

o Expert B (Technical Precision):
  Role: Translate the statement using technical terminology and ensure
  accuracy in logical expressions.
  Focus: Use precise language to explain the conditions without
  oversimplifying.
  Precise Translation: Define the conditions and logical relationships
  (AND, OR, NOT) explicitly with accurate terminology and variable
  names.

o Expert C (Contextual Example):
  Role: Use real-world analogies or contextual explanations to clarify
  the system's behavior for technical users.
  Focus: Provide relevant analogies that align with technical scenarios,
  but without oversimplifying.
  Contextual Example: Provide relatable comparisons to real-world
  systems (e.g., decision-making processes, system transitions) to clarify
  the conditions, without reducing the complexity of the logic.

3. Step 2: Refining the Explanation
o Expert A (Simplified Language):
  Role: Organize the conditions into clear steps, using simple language.
  Focus: Break the logic down into digestible parts while preserving key
  technical details.
  Simplified Explanation: Clearly list out the conditions that must be
  met for the transition, using straightforward language and bullet points
  for ease of understanding.

o Expert B (Technical Precision):
  Role: Ensure the translation is technically precise, using consistent
  terms and logical operators.
  Focus: Ensure all logical operators and conditions are clearly
  explained using proper technical terminology.
  Refined Technical Explanation: Present the explanation with a focus
  on accuracy, where each condition is listed clearly, ensuring all
  technical variables and their relationships are intact.

o Expert C (Contextual Example):
  Role: Refine the example or analogy to ensure it remains relevant,
  accurate, and helpful.
  Focus: Provide an example that aligns with the technical scenario,
  ensuring the analogy helps clarify the logic.
  Contextual Example: Provide a more concise, yet accurate example
  that mirrors the technical scenario and simplifies the understanding of
  the system's transitions.

4. Step 3: Final Combined Result
o Combined Result:
  Include the logical statement in the begining
  Role: Combine all insights from the previous steps into a final refined
  translation.
  Focus: The final translation should be clear, precise, and concise,
  ensuring the explanation is suitable for a technical audience.
  Final Combined Translation: Provide a final cohesive explanation,
  ensuring that all key technical details, conditions, and relationships are
  presented clearly. List conditions as needed and provide an overview
  of how they interrelate.
  """),
            ],
        ),
        types.Content(
            role="model",
            parts=[
                types.Part.from_text(text="""Let's break down this logical statement according to the provided guidelines.

**1. Logical Statement:**
[The provided logical statement from the input]

**2. Step 1: Logical Decomposition**

*   **Expert A (Simplified Language):**

    *   **Role:** Simplify the statement for initial understanding.
    *   **Focus:** Break down the complex condition into smaller, easier-to-understand parts.
    *   **Simplified Translation:**
        *   The system is currently in \"Standby\" mode.
        *   There's no request to eject a disc.
        *   There's no request to switch to FM radio.
        *   There's no request to switch to CD mode.
        *   There's no request to switch to AM radio.
        *   *If all of the above are true, the system remains in \"Standby\" mode.*

*   **Expert B (Technical Precision):**

    *   **Role:** Translate using precise technical terms.
    *   **Focus:** Maintain accuracy in logical expressions.
    *   **Precise Translation:**
        *   `rtDW.is_ModeManager == IN_Standby`: The Mode Manager's current state is \"Standby.\"
        *   `!inp.DiscEject`: The `DiscEject` input signal is logically FALSE (no disc eject requested).
        *   `!(inp.RadioReq == FM)`: The `RadioReq` input is not equal to `FM`.
        *   `!(inp.RadioReq == CD)`: The `RadioReq` input is not equal to `CD`.
        *   `!(inp.RadioReq == AM)`: The `RadioReq` input is not equal to `AM`.
        *   `->`: This is a logical implication.  If the entire left side of the expression is TRUE, then the right side must also be TRUE.
        *   Therefore, if the Mode Manager is in Standby, and there's no disc eject request, and the radio request is not FM, CD, or AM, then the Mode Manager *remains* in Standby.

*   **Expert C (Contextual Example):**

    *   **Role:** Provide a real-world analogy.
    *   **Focus:** Relate the logic to a familiar scenario.
    *   **Contextual Example:**
        Imagine a car's entertainment system.  If the system is currently off (Standby), and you don't press the \"Eject\" button for the CD player, and you don't select FM, CD, or AM radio, then the system will remain off (Standby).  The system only changes state if you actively request a different mode or action. This statement is just about *remaining* in standby, not *entering* standby.

**3. Step 2: Refining the Explanation**

*   **Expert A (Simplified Language):**

    *   **Role:** Organize conditions into clear steps.
    *   **Focus:** Break down the logic for easy understanding.
    *   **Simplified Explanation:**
        The system stays in Standby mode if *all* of the following are true:
        1.  The system is *already* in Standby mode.
        2.  The user is *not* trying to eject a disc.
        3.  The user has *not* selected FM radio.
        4.  The user has *not* selected CD mode.
        5.  The user has *not* selected AM radio.
        If any of these conditions are *not* met, this rule doesn't tell us what happens. It only describes when the system *stays* in Standby.

*   **Expert B (Technical Precision):**

    *   **Role:** Ensure technical precision and consistency.
    *   **Focus:** Explain logical operators and conditions clearly.
    *   **Refined Technical Explanation:**
        This logical statement defines a condition for maintaining the `IN_Standby` state within the `ModeManager`.  It utilizes a logical implication (`->`) where the antecedent (left side) is a conjunction (AND) of several conditions:

        1.  **Current State:** `rtDW.is_ModeManager == IN_Standby` (Mode Manager must be in Standby).
        2.  **Disc Eject Input:** `!inp.DiscEject` (Disc Eject input must be FALSE).
        3.  **Radio Request Input:** The following conditions must ALL be true:
            *   `!(inp.RadioReq == FM)` (Radio Request input is not FM).
            *   `!(inp.RadioReq == CD)` (Radio Request input is not CD).
            *   `!(inp.RadioReq == AM)` (Radio Request input is not AM).

        The consequent (right side) is `rtDW.is_ModeManager == IN_Standby`, meaning if the antecedent is TRUE, the Mode Manager remains in the `IN_Standby` state. This statement does *not* describe how the system enters `IN_Standby`; it only specifies a condition under which it *remains* there.

*   **Expert C (Contextual Example):**

    *   **Role:** Refine the analogy for accuracy and relevance.
    *   **Focus:** Provide a concise, accurate example.
    *   **Contextual Example:**
        Think of a microwave that's currently idle (Standby). If you don't open the door (similar to DiscEject), and you don't press any buttons to start cooking (like selecting FM, CD, or AM), the microwave will simply remain idle. This rule is about the microwave *staying* idle, not about how it *becomes* idle.

**4. Step 3: Final Combined Result**

*   **Combined Result:**
        print the logical statement 
    *   **Role:** Combine all insights into a final, refined translation.
    *   **Focus:** Clarity, precision, and conciseness for a technical audience.
    *   **Final Combined Translation:**
        This logical statement describes the conditions under which a system's `ModeManager` *remains* in the `IN_Standby` state. It does *not* define how the system enters this state. The statement can be interpreted as follows:

        **\"If the ModeManager is currently in the IN_Standby state, AND there is no Disc Eject request, AND the Radio Request input is NOT FM, CD, or AM, THEN the ModeManager will remain in the IN_Standby state.\"**

        More precisely:

        1.  **`rtDW.is_ModeManager == IN_Standby`:** The Mode Manager must already be in the `IN_Standby` state.
        2.  **`!inp.DiscEject`:** The `DiscEject` input signal must be FALSE (no eject request).
        3.  **`!(inp.RadioReq == FM) && !(inp.RadioReq == CD) && !(inp.RadioReq == AM)`:** The `RadioReq` input signal must *not* be `FM`, `CD`, or `AM`. This is equivalent to saying the user has not requested any of these radio modes.

        The logical implication (`->`) ensures that if *all* conditions on the left-hand side (the antecedent) are true, then the right-hand side (the consequent), `rtDW.is_ModeManager == IN_Standby`, must also be true. This means the system stays in Standby. If *any* of the conditions on the left are false, the statement provides no information about the resulting state of the `ModeManager`.
        This rule focuses solely on the persistence of the Standby state.

This final combined result provides a clear, technically accurate, and contextually understandable explanation of the original logical statement, suitable for a technical audience. It emphasizes the crucial point that the statement describes conditions for *remaining* in Standby, not for *entering* it. It separates the conditions and uses proper logical terminology.

Strictly follow the structure of the guidelines and the example provided. in the output just display the final translation and nothing else do not add the vebose of the previous steps""")
            ],
        ),
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=logical_statement),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        temperature=NL_TEMPERATURE,
        top_p=NL_TOP_P,
        top_k=NL_TOP_K,
        max_output_tokens=NL_MAX_TOKENS,
        response_mime_type="text/plain",
    )

    complete_response = ""
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        print(chunk.text)
        complete_response += chunk.text

    # Extract the final translation with fallback
    try:
        start_marker = "**Final Combined Translation:**"
        start_index = complete_response.find(start_marker)

        if start_index != -1:
            final_translation = complete_response[start_index + len(start_marker):].strip()
        else:
            print("\nMarker not found — saving full response instead.")
            final_translation = complete_response.strip()

        results_dir = Path(NLP_TRANSLATION_FILE)
        results_dir.mkdir(parents=True, exist_ok=True)

        output_file = results_dir / "nlp_translation.txt"
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write("FINAL TRANSLATION\n")
            file.write("================\n\n")
            for line in final_translation.split('\n'):
                if not line.strip():
                    file.write('\n')
                elif line.strip().startswith('**'):
                    file.write(line.strip() + '\n')
                elif line.strip()[0].isdigit() and len(line.strip()) > 1 and line.strip()[1] == '.':
                    file.write('  ' + line.strip() + '\n')
                elif line.strip().startswith('*'):
                    file.write('    ' + line.strip() + '\n')
                else:
                    file.write('  ' + line.strip() + '\n')

        print(f"\nFinal translation saved to {output_file}")
    except Exception as e:
        print(f"\nError saving the final translation: {str(e)}")


if __name__ == "__main__":
    generate()
