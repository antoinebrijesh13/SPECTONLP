from google import genai
from google.genai import types
import re
from dotenv import load_dotenv
from load_config import *
load_dotenv()
def generate():
    try:
        with open(SIMPLIFIED_FILE,'r',encoding='utf-8') as f:
            input_text = f.read().strip()
    except FileNotFoundError:
        print("error simplified expression not found")
        return
    except Exception as e:
        print(f"error reading the file {str(e)}")
        return
    
    # Define output file
    output_file = FINAL_RESULT_FILE
    
    client = genai.Client(
        api_key=GOOGLE_API_KEY,
    )

    model = SIMPLIFIER_MODEL
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text="""Guideline for simplifying the logical statement
Example input format: 
simplified statement: (A && ((!B && C) || (!B && !C && D) || (!B && !C && !D && E))) -> F
A = dw.is_ModeManager == IN_Standby
B = inp.DiscEject
C = inp.RadioReq == FM
D = inp.RadioReq == CD
E = inp.RadioReq == AM
F = rtDW.is_ModeManager == IN_ON

Step 1: Split the logical statement into pieces according to the way they are grouped

the example logical statement can be splitted into the following:

(A 
&& 
((!B && C) 
|| 
(!B && !C && D) 
|| (!B && !C && !D && E))) -> F
Step 2: Simplify each part by applying the De Morgan's rule :
This rule is only applicable to the parts left to the implication (->)
Step3:Joining the simplified parts back together:
After step 3: 
(A && ((!B && C) || (!B && !C && D) || (!B && !C && !D && E))) -> F
Step4: Factoring out the common term::
Look for a common term if exist factor it out
example:
(!B && C) || (!B && !C && D) || (!B && !C && !D && E)
We can factor out !B:
After step 4:Further Simplification can be done using the following rules if necessary or ignore this step::
Rules:
Identity Laws:
A && TRUE ≡ A
A || FALSE ≡ A
Domination Laws:
A && FALSE ≡ FALSE
A || TRUE ≡ TRUE
Idempotent Laws:
A && A ≡ A
A || A ≡ A
Commutative Laws:
A && B ≡ B && A
A || B ≡ B || A
Associative Laws:
(A && B) && C ≡ A && (B && C)
(A || B) || C ≡ A || (B || C)
Distributive Laws:
A && (B || C) ≡ (A && B) || (A && C)
A || (B && C) ≡ (A || B) && (A || C)
Absorption Laws:
A && (A || B) ≡ A
A || (A && B) ≡ A
Negation Laws:
A && !A ≡ FALSE
A || !A ≡ TRUE
Other Laws:
A || (!A && B) = A || B
Example:


(A &&!B && (C || (!C && D) || (!C && !D && E)) -> F
Further simplification
Simplify the inner part: C || (!C && D) || (!C && !D && E)
We know that A || (!A && B) is equivalent to A || B.
Let A = C and B = D. So, C || (!C && D) simplifies to C || D.

Substitute the simplified part back:
The inner part now becomes (C || D) || (!C && !D && E).

Apply De Morgan's Law: !C && !D is equivalent to !(C || D).
So, the expression is (C || D) || (!(C || D) && E).
Apply A || (!A && B) = A || B again:
Let A = C || D and B = E.

Therefore, the simplified form of the given logical statement is:
!B && (C || D || E)
Final simplified logical statement: (A &&!B && (C || D || E) -> F
Step 5:  change the term names back to their original names
Example:
Statement : (A &&!B && (C || D || E) -> F
Using the variable mapping from the input Change the variable name to its originals
Note: if two names are mapped to a single variable example: (C -> \"dw.is_ON == IN_CDMode\" = \"rtDW.is_ON == IN_CDMode\")
The first variable name goes at the left of the implication and the second variable name goes to the right of the variable name

display the final result strictly in the following format:
simplified final statement : (dw.is_ModeManager == IN_Standby && !inp.DiscEject && (inp.RadioReq == FM ||inp.RadioReq ==CD || inp.RadioReq == AM)) -> rtDW.is_ModeManager == IN_ON
""")
            ],
        ),
        types.Content(
            role="model",
            parts=[
                types.Part.from_text(text="""Here's a thinking process to arrive at the provided guideline for simplifying logical statements:

1.  **Understand the Goal:** The user wants a step-by-step guideline to simplify complex logical statements, specifically those involving implications (`->`), conjunctions (`&&`), disjunctions (`||`), and negations (`!`). The input format includes a mapping of simple variables (A, B, C...) to more complex conditions. The output should be the simplified statement with the original condition names restored.

2.  **Analyze the Example:**
    *   **Input Statement:** `(A && ((!B && C) || (!B && !C && D) || (!B && !C && !D && E))) -> F`
    *   **Variable Mapping:** A, B, C, D, E, F are mapped to specific conditions.
    *   **Target Output:** `(dw.is_ModeManager == IN_Standby && !inp.DiscEject && (inp.RadioReq == FM || inp.RadioReq == CD || inp.RadioReq == AM)) -> rtDW.is_ModeManager == IN_ON`

3.  **Break Down the Simplification Process (Reverse Engineer the Example):**
    *   How did `(A && ((!B && C) || (!B && !C && D) || (!B && !C && !D && E))) -> F` become `(A && !B && (C || D || E)) -> F`?
    *   **Focus on the antecedent (left side of `->`):** `A && ((!B && C) || (!B && !C && D) || (!B && !C && !D && E))`
    *   **Inner Part:** `(!B && C) || (!B && !C && D) || (!B && !C && !D && E)`
    *   **Observation 1: Factoring:** `!B` is common in all three terms inside the inner parentheses. Factor it out using the distributive law `(X && Y) || (X && Z) ≡ X && (Y || Z)` extended to three terms.
        *   `!B && (C || (!C && D) || (!C && !D && E))`
    *   **Observation 2: Simplifying the remaining part:** `C || (!C && D) || (!C && !D && E)`
        *   Apply the rule `X || (!X && Y) ≡ X || Y` to the first two terms: `C || (!C && D)`. Let `X = C`, `Y = D`. This simplifies to `C || D`.
        *   Now we have: `(C || D) || (!C && !D && E)`
        *   Notice `!C && !D`. By De Morgan's Law, this is `!(C || D)`.
        *   So the expression becomes: `(C || D) || (!(C || D) && E)`
        *   Apply the rule `X || (!X && Y) ≡ X || Y` again. Let `X = (C || D)`, `Y = E`. This simplifies to `(C || D) || E`, which is `C || D || E`.
    *   **Combine:** Substitute the simplified inner part back: `!B && (C || D || E)`
    *   **Put it back into the full antecedent:** `A && !B && (C || D || E)`
    *   **Full Simplified Statement (variables):** `(A && !B && (C || D || E)) -> F`
    *   **Restore Original Names:** Replace A, B, C, D, E, F with their mapped conditions. This matches the target output.

4.  **Structure the Guideline Steps based on the Reverse Engineering:**

    *   **Step 0 (Implicit but important):** Start with the full logical statement and the variable mapping.
    *   **Step 1: Decomposition:** The example shows splitting the statement visually. This helps understand the structure. It's more about visualization than actual simplification, but it's good for clarity. Let's formalize this as \"Split the logical statement into pieces according to the way they are grouped.\"
    *   **Step 2: De Morgan's Rule?** The example mentions De Morgan's rule in Step 2, but *doesn't actually apply it* at that stage. It says \"This rule is only applicable to the parts left to the implication (->)\". This seems misplaced or potentially confusing. De Morgan's is a *tool* for simplification, not necessarily the *first* step after splitting. It *was* used later inside the `C || (!C && D) || (!C && !D && E)` simplification. Let's keep De Morgan's in mind as a tool but maybe not a mandatory early step unless needed. *Correction:* Re-reading the example, Step 2 *doesn't apply* De Morgan's, it just mentions it. Step 3 just repeats the statement. This suggests Steps 2 and 3 in the *example* are perhaps not well-defined simplification steps themselves but lead into the *real* simplification.
    *   **Step 3: Joining back?** The example's Step 3 just shows the statement again. This isn't a transformation step. Let's skip this as a distinct *action* step.
    *   **Step 4: Factoring:** This was a crucial step in the example (`!B` was factored out). This should definitely be a key step. \"Look for a common term and factor it out.\" This applies primarily within `&&` groups connected by `||`, or `||` groups connected by `&&` (using distributive laws).
    *   **Step 4 (Continued): Further Simplification:** The example *then* applies other rules, specifically `X || (!X && Y) ≡ X || Y` and De Morgan's implicitly (`!C && !D = !(C || D)`). This indicates a need for a general simplification step using standard Boolean algebra rules *after* factoring (or sometimes before, depending on the expression). Listing the common rules is helpful here.
        *   Identity Laws
        *   Domination Laws
        *   Idempotent Laws
        *   Commutative Laws
        *   Associative Laws
        *   Distributive Laws (used for factoring and expansion)
        *   Absorption Laws
        *   Negation Laws
        *   De Morgan's Laws: `!(A && B) ≡ !A || !B` and `!(A || B) ≡ !A && !B` (Crucial, should be listed explicitly)
        *   Other useful laws like `A || (!A && B) ≡ A || B` and `A && (!A || B) ≡ A && B`.
    *   **Step 5: Restore Names:** The final step is clearly substituting the original variable names back. Need to address the note about multiple mappings (left side vs. right side of implication).

5.  **Refine the Guideline Steps:**

    *   **Step 0: Input:** State the input clearly (statement + mapping).
    *   **Step 1: Parsing/Understanding:** Break down the structure visually or mentally. Focus on the antecedent (left of `->`) as that's where most simplification usually occurs in these examples. (Combine original Step 1 and the note about simplifying the left side).
    *   **Step 2: Factoring:** Apply distributive laws to factor out common terms within OR groups (like `!B` in the example) or AND groups. This often simplifies significantly.
    *   **Step 3: Apply Boolean Algebra Rules:** Use the standard set of rules (De Morgan's, Absorption, `A || (!A && B) = A || B`, Identity, Negation, etc.) iteratively on the factored expression (or the original if factoring wasn't applicable/helpful) until no further simplification seems possible or obvious. Focus on the antecedent first.
    *   **Step 4: Reconstruct:** Put the simplified antecedent back with the implication (`->`) and the consequent (right side).
    *   **Step 5: Substitute Names:** Replace the placeholder variables (A, B, C...) with their original, mapped conditions, respecting the left/right side distinction if applicable.

6.  **Review Against Example:** Let's trace the example using the *refined* steps:

    *   **Input:** `(A && ((!B && C) || (!B && !C && D) || (!B && !C && !D && E))) -> F` + Mapping.
    *   **Step 1 (Parse):** Focus on `A && ((!B && C) || (!B && !C && D) || (!B && !C && !D && E))`.
    *   **Step 2 (Factor):** Factor `!B` from the inner OR group: `A && !B && (C || (!C && D) || (!C && !D && E))`.
    *   **Step 3 (Boolean Algebra):**
        *   Simplify `C || (!C && D) || (!C && !D && E)`.
        *   Apply `X || (!X && Y) = X || Y` to `C || (!C && D)` -> `C || D`.
        *   Expression becomes `(C || D) || (!C && !D && E)`.
        *   Recognize `!C && !D = !(C || D)` (De Morgan's).
        *   Expression becomes `(C || D) || (!(C || D) && E)`
        *   Apply `X || (!X && Y) = X || Y` again -> `(C || D) || E` -> `C || D || E`.
        *   Substitute back: `A && !B && (C || D || E)`.
    *   **Step 4 (Reconstruct):** `(A && !B && (C || D || E)) -> F`.
    *   **Step 5 (Substitute):** `(dw.is_ModeManager == IN_Standby && !inp.DiscEject && (inp.RadioReq == FM || inp.RadioReq == CD || inp.RadioReq == AM)) -> rtDW.is_ModeManager == IN_ON`.

7.  **Final Polish:** Make the language clear and consistent. Ensure the list of rules is comprehensive enough for typical cases. Clarify the scope (usually simplifying the antecedent). Add the note about variable naming convention. The original guideline structure was slightly confusing (Steps 2/3 seemed inactive). The refined structure (Parse -> Factor -> Boolean Algebra -> Reconstruct -> Substitute) seems more logical and actionable. Let's adapt the user's original step numbering and phrasing where possible while incorporating the refined logic.

    *   Keep Step 1 (Split/Visualize).
    *   Modify Step 2 (De Morgan's) to be part of a broader \"Apply Simplification Rules\" step, perhaps combining it with the rules listed later. Or, make De Morgan's its own step if it's often the *first* rule applied (though factoring seems more prominent in the example). Let's merge it into a general simplification step.
    *   Keep Step 4 (Factoring) but maybe move it *before* general simplification rules, as it often enables further simplification.
    *   Add a dedicated step for applying the *other* Boolean rules.
    *   Keep Step 5 (Substitute Names).

    Let's try to follow the user's *exact* structure but make the descriptions more accurate:

    *   **Step 1: Split:** Okay as is (visual aid).
    *   **Step 2: Simplify using rules (including De Morgan's):** Combine the original Step 2 and the list of rules from later. State that simplification primarily targets the antecedent. *Correction:* The example separates factoring. Let's stick to that.
    *   **Step 2 (as user): De Morgan's:** Mention De Morgan's as *one* tool for simplification, applicable to the antecedent. (Maybe this step isn't strictly necessary as a *separate* step).
    *   **Step 3 (as user): Joining:** This seems redundant; simplification happens *on* the parts. Let's remove or repurpose this. Maybe Step 3 becomes \"Apply Simplification Rules (excluding factoring)\".
    *   **Step 4 (as user): Factoring:** Keep this as a distinct step. Emphasize using the Distributive Law.
    *   **Step 4 Continued / New Step: Further Simplification:** Apply *other* Boolean algebra rules (Absorption, `A || (!A && B) = A || B`, etc.) to the factored expression. List the rules here.
    *   **Step 5 (as user): Substitute Names:** Keep as is.

    This looks closer to the user's example flow, even if Steps 2/3 seem a bit weak on their own. Let's refine the wording based on this structure.

    *Self-Correction:* The user's example *explicitly* puts Factoring *after* mentioning De Morgan's and joining. And *then* applies further simplification rules (`A || (!A && B) = A || B`). So, the order presented *is* deliberate, even if Factor/Simplify could sometimes be swapped. Let's stick to the user's presented order: Split -> Mention De Morgan's (as applicable) -> Re-state -> Factor -> Simplify Further (using other rules) -> Substitute.

    Okay, the provided text seems to follow this structure. The core actions are: Splitting (visualization), Factoring, Applying simplification rules (like `A || (!A && B)`), and Substituting names back. The mention of De Morgan's early on seems more like a reminder than a mandatory action at that specific point. The \"Joining\" step is just showing the result before factoring. The \"Further Simplification\" step is where most non-factoring Boolean algebra happens. The provided guideline text accurately reflects the *example's* flow."""),
                types.Part.from_text(text="""Okay, here is the guideline structured according to your example steps, incorporating the rules and process demonstrated.

**Guideline for Simplifying Logical Statements**

This guideline outlines a step-by-step process to simplify logical statements, particularly those involving implications (`->`), conjunctions (`&&`), disjunctions (`||`), and negations (`!`), often found in system specifications or code generation.

**Input Format:**

1.  **Logical Statement:** The complex statement to be simplified, using placeholders (like A, B, C...).
2.  **Variable Mapping:** A list defining what each placeholder variable represents in terms of the original system conditions.

**Example Input:**

*   **Statement:** `(A && ((!B && C) || (!B && !C && D) || (!B && !C && !D && E))) -> F`
*   **Mapping:**
    *   `A = dw.is_ModeManager == IN_Standby`
    *   `B = inp.DiscEject`
    *   `C = inp.RadioReq == FM`
    *   `D = inp.RadioReq == CD`
    *   `E = inp.RadioReq == AM`
    *   `F = rtDW.is_ModeManager == IN_ON` (Note: Could also be `dw.is_ModeManager == IN_ON` if `rtDW` aliases `dw` depending on context, but we follow the example's naming).

---

**Simplification Steps:**

**Step 1: Split the logical statement into pieces according to the way they are grouped**

*   **Goal:** Understand the structure of the statement, especially the antecedent (the part before the `->`).
*   **Action:** Visually or mentally break down the statement based on parentheses and operators.
*   **Example:**
    ```
    (
      A 
      && 
      (
        (!B && C) 
        || 
        (!B && !C && D) 
        || 
        (!B && !C && !D && E)
      )
    ) 
    -> 
    F
    ```
    *Focus simplification efforts primarily on the antecedent (left side of `->`).*

**Step 2: Apply De Morgan's Rule (If Applicable)**

*   **Goal:** Simplify negated groups. De Morgan's rules are:
    *   `!(X && Y) ≡ !X || !Y`
    *   `!(X || Y) ≡ !X && !Y`
*   **Action:** Look for negated expressions within the antecedent (`!(...)`) and apply De Morgan's rules to push the negation inward or simplify the structure.
*   **Example:** *In the provided example statement, there are no top-level negations like `!(...)` in the antecedent where De Morgan's would be immediately applied in this step. It might be used later within sub-expressions during further simplification (Step 4).*

**Step 3: Joining the simplified parts back together**

*   **Goal:** Reassemble the statement after any initial simplifications from Step 2.
*   **Action:** Write down the statement incorporating any changes made. If no changes were made in Step 2, the statement remains the same.
*   **Example (after Step 2, assuming no changes were made):**
    `(A && ((!B && C) || (!B && !C && D) || (!B && !C && !D && E))) -> F`

**Step 4: Factoring out common terms**

*   **Goal:** Simplify expressions by using the distributive laws to factor out common variables or sub-expressions.
    *   ` (X && Y) || (X && Z) ≡ X && (Y || Z)`
    *   ` (X || Y) && (X || Z) ≡ X || (Y && Z)` (Less common for simplification, but valid)
*   **Action:** Examine parts of the antecedent involving `||` groups where terms share a common factor connected by `&&`, or `&&` groups where terms share a common factor connected by `||`. Factor the common term out.
*   **Example:**
    *   Focus on the inner part: `(!B && C) || (!B && !C && D) || (!B && !C && !D && E)`
    *   The common term in all three parts connected by `||` is `!B`.
    *   Factor out `!B`: `!B && (C || (!C && D) || (!C && !D && E))`
    *   Substitute back into the main statement: `(A && !B && (C || (!C && D) || (!C && !D && E))) -> F`

**Step 4 (Continued): Further Simplification using Boolean Algebra Rules**

*   **Goal:** Apply standard Boolean algebra rules to simplify the expression further, especially the part modified by factoring.
*   **Action:** Iteratively apply simplification rules until the expression is in its simplest form. Focus on the inner parts first.
*   **Common Rules:**
    *   **Identity:** `X && TRUE ≡ X`, `X || FALSE ≡ X`
    *   **Domination:** `X && FALSE ≡ FALSE`, `X || TRUE ≡ TRUE`
    *   **Idempotent:** `X && X ≡ X`, `X || X ≡ X`
    *   **Commutative:** `X && Y ≡ Y && X`, `X || Y ≡ Y || X`
    *   **Associative:** `(X && Y) && Z ≡ X && (Y && Z)`, `(X || Y) || Z ≡ X || (Y || Z)`
    *   **Distributive:** `X && (Y || Z) ≡ (X && B) || (X && C)`, `X || (Y && Z) ≡ (X || Y) && (X || Z)`
    *   **Absorption:** `X && (X || Y) ≡ X`, `X || (X && Y) ≡ X`
    *   **Negation:** `X && !X ≡ FALSE`, `X || !X ≡ TRUE`
    *   **De Morgan's:** `!(X && Y) ≡ !X || !Y`, `!(X || Y) ≡ !X && !Y`
    *   **Other Useful Laws:**
        *   `X || (!X && Y) ≡ X || Y`
        *   `X && (!X || Y) ≡ X && Y`
*   **Example (Continuing from Step 4):**
    *   Simplify the inner part: `C || (!C && D) || (!C && !D && E)`
    *   Apply `X || (!X && Y) ≡ X || Y` to `C || (!C && D)` (let `X=C`, `Y=D`). Result: `C || D`.
    *   The expression becomes: `(C || D) || (!C && !D && E)`
    *   Apply De Morgan's implicitly or explicitly: `!C && !D ≡ !(C || D)`.
    *   The expression becomes: `(C || D) || (!(C || D) && E)`
    *   Apply `X || (!X && Y) ≡ X || Y` again (let `X = (C || D)`, `Y = E`). Result: `(C || D) || E`.
    *   Using associativity: `C || D || E`.
    *   Substitute the fully simplified inner part back: `!B && (C || D || E)`
    *   Final simplified statement (with variables): `(A && !B && (C || D || E)) -> F`

**Step 5: Change the term names back to their original names**

*   **Goal:** Present the simplified statement using the original condition names.
*   **Action:** Replace each placeholder variable (A, B, C...) with its corresponding full condition from the mapping provided in the input.
*   **Handling Multiple Mappings:** If a variable maps to different names depending on context (like `dw.X` vs `rtDW.X`), use the appropriate name based on its position. As per the example note: typically, use the first name listed if it appears on the left side (antecedent) of `->`, and the second name if it appears on the right side (consequent). *Clarification based on example:* It seems `A` maps to `dw...` (left side) and `F` maps to `rtDW...` (right side), following this pattern.
*   **Example:**
    *   Simplified statement: `(A && !B && (C || D || E)) -> F`
    *   Apply mapping:
        *   A -> `dw.is_ModeManager == IN_Standby`
        *   !B -> `!inp.DiscEject`
        *   C -> `inp.RadioReq == FM`
        *   D -> `inp.RadioReq == CD`
        *   E -> `inp.RadioReq == AM`
        *   F -> `rtDW.is_ModeManager == IN_ON`
    *   **Final Result:**
        `(dw.is_ModeManager == IN_Standby && !inp.DiscEject && (inp.RadioReq == FM || inp.RadioReq == CD || inp.RadioReq == AM)) -> rtDW.is_ModeManager == IN_ON`

--- dont over simplify the logical statement to boolean values, provide the simplified logical statement,never use ` this in the simplified logical statement"""),
            ],
        ),
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=input_text),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        temperature=SIMPLIFIER_TEMPERATURE,
        top_p=SIMPLIFIER_TOP_P,
        top_k=SIMPLIFIER_TOP_K,
        max_output_tokens=SIMPLIFIER_MAX_TOKENS,
        response_mime_type="text/plain",
    )

    complete_response = ""
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        print(chunk.text)
        chunk_text = chunk.text
        if chunk_text is not None:  # Add check for None values
            complete_response += chunk_text

    try:
    # Extract only the simplified logical statement
    # Look for the pattern "simplified final statement :" followed by the actual statement
        pattern = r'simplified final statement\s*:\s*([^\n]+)'
        match = re.search(pattern, complete_response, re.IGNORECASE)
    
        if match:
            final_expression = match.group(1).strip()
        else:
            # Fallback: try to find any logical statement with an arrow (->)
            pattern = r'\([^()]*?(?:\([^()]*?\)[^()]*)*->[^()]*?(?:\([^()]*?\)[^()]*)*\)'
            matches = re.findall(pattern, complete_response)
            if matches:
                final_expression = matches[-1].strip()  # Get the last match
            else:
                print("\nError: Could not find final result in the response")
                final_expression = None

        if final_expression:
            # Clean the expression
            # 1. Remove backticks or other formatting characters
            final_expression = final_expression.replace('`', '')
            final_expression = final_expression.replace('*', '')  # remove trailing asterisks
            final_expression = final_expression.strip()

            # 2. Optionally remove any other unwanted characters
            allowed_pattern = r'[^A-Za-z0-9_\.\(\)\s!&|<>=+-]'
            final_expression = re.sub(allowed_pattern, '', final_expression)

                # Save the cleaned result to a file
            with open(output_file, "w", encoding='utf-8') as f:
                f.write(final_expression)
            print(f"\nFinal result has been saved to '{output_file}'")
    except Exception as e:
        print(f"\nError saving final result: {str(e)}")
    except Exception as e:
        print(f"Error during AI simplification: {str(e)}")
        print("Please check your API key and internet connection.")
        return

def main():
    """Main entry point for the simplifier module."""
    print("Logical Expression Simplifier")
    print("-----------------------------")
    generate()

if __name__ == "__main__":
    main() 