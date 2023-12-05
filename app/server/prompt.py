AXES = [
    [
        "Colloquial",
        "Standard",
        "Colloquial language is informal and used in everyday conversation, while standard language follows established rules and conventions and is used in more formal situations.",
    ],
    [
        "Non-technical",
        "Technical",
        "Technical language is often used by experts in a particular field and includes specialized terminology and jargon. Non-technical language, on the other hand, is more accessible to a general audience and avoids the use of complex terms.",
    ],
    [
        "Subjective",
        "Objective",
        "Subjective language expresses personal opinions, feelings, or judgments, while objective language presents facts or information without bias or personal interpretation.",
    ],
    [
        "Implicit",
        "Explicit",
        "Implicit language relies on the context, shared knowledge, and non-verbal cues to convey meaning. It often requires the listener or reader to infer or deduce the intended message. Explicit language, on the other hand, is clear and direct. It leaves little room for interpretation or misunderstanding.",
    ],
]


def get_prompt_L1(vl, ftt_str, semantics):
    semantics_str = ", ".join([f"[{semantic.capitalize()}]" for semantic in semantics])
    semantics_str2 = "\n".join(f"- {semantic.capitalize()}:" for semantic in semantics)

    prompt = f"""
{vl}

Let's generate a level 1 NL description step by step.

Step 1. Determine if the visualization contains composite views, such as layered plots, trellis plots, or other types of multiple view displays, and provide a count of the number of plots if any are present.
Step 2. Analyze the semantics of each chart individually, including {semantics_str}. Refer to this:
{ftt_str}
Step 3. Generate a level 1 NL description using the semantics. It contains elemental and encoded properties of the visualization (i.e., the visual components that comprise a graphical representation's design and construction).

##
Step 1. Composite Views:
- True/False:
- (If True) Type: (layered, trellis, multiple views)
- Number of plots:
Step 2. Chart Semantics:
{semantics_str2}
- Field (Value):
Step 3. Level 1 NL Description:
"""
    return prompt


def get_prompt_L2(vl, feature):
    prompt = f"""
{vl}

Let's generate question(s) step by step. The most prominent and meaningful feature in the given chart is: {feature}

Step 1. What is the mathematical operation(s) (e.g., max, min, sum, difference, and average) required to describe the feature?
Step 2. Generate question(s) using the mathematical operation(s) required to describe the feature. If there are multiple questions, separate them with semicolon(;).

##
Step 1. Operations:
Step 2. Questions:
"""
    return prompt


def get_prompt_L2_2(info, ftt_str):
    prompt = f"""
Information: {info}

{ftt_str}

Generate a concise level 2 NL description of a visualization, with 1 or 2 sentences. It contains statistical and relational properties of the visualization (e.g., descriptive statistics, extrema, outliers, correlations, point-wise comparisons).

##
Level 2 NL Description:
"""
    return prompt


def get_prompt_utterance(vl, ftt_str, semantics):
    semantics_str = ", ".join([f"[{semantic.capitalize()}]" for semantic in semantics])

    prompt = f"""
{vl}

Step 1. Determine if the visualization contains composite views, such as layered plots, trellis plots, or other types of multiple view displays, and provide a count of the number of plots if any are present.
Step 2. Provide a list of instructions to create the chart using natural language.
- Write instructions for each view and separate with <%>
- Separate each instruction by a semicolon (;)
- Divide each instruction to contain only one specific action
- Use the following chart semantics to specify instructions: {semantics_str}
Step 3. Given the information about the fields and their synonyms, please replace the field names with their corresponding synonyms.
{ftt_str}

##
Step 1. Composite Views:
- True/False:
- (If True) Type: (layered, trellis, multiple views)
- Number of plots:
Step 2. Instructions:
[View #]; [<Chart Semantic>]: <Instruction>; [<Chart Semantic>]: <Instruction>; ... <%>
Step 3. Instructions:
[View #]; [<Chart Semantic>]: <Instruction>; [<Chart Semantic>]: <Instruction>; ... <%>
"""
    return prompt


def get_prompt_utterance2(utteranceType, inst_first_concat, consider):
    if utteranceType == "command":
        prompt = f"""{inst_first_concat}

The above are instructions to generate a chart. Let's generate combined instructions for each view step by step.

Step 1. Identify the primary information in each view.
Step 2. Identify the secondary information in each view.
Step 3. Generate an utterance for each view using only the primary info. Please follow these rules:
- Use imperative voice
- Write in a single sentence
- Use only the primary info
- Make it concise and simple
- {consider}

##
View #<Number>:
Step 1. Primary Information:
Step 2. Secondary Information:
Step 3. Utterance:
"""
    elif utteranceType == "query":
        prompt = f"""{inst_first_concat}

The above are instructions to generate a chart. Let's generate combined instructions for each view step by step.

Step 1. Identify the primary information in each view.
Step 2. Identify the secondary information in each view.
Step 3. Generate an utterance for each view using only the primary info. Please follow these rules:
- Refrain from using verbs and articles (e.g., a, the)
- Use only variables, fields, attributes, mathematical formulas (e.g., sum, avg, mix, max, count, order), abbreviations (e.g., vs), and prepositions (e.g., of, by, for, with, over, from, to)
- Write in a single sentence
- Use only the primary info
- Make it concise and simple
- {consider}

##
View #<Number>:
Step 1. Primary Information:
Step 2. Secondary Information:
Step 3. Utterance:
"""
    else:
        prompt = f"""{inst_first_concat}

The above are instructions to generate a chart. Let's generate combined instructions for each view step by step.

Step 1. Identify the primary information in each view.
Step 2. Identify the secondary information in each view.
Step 3. Generate an utterance for each view using only the primary info. Please follow these rules:
- Ask an inquiry as a question
- Write in a single sentence
- Use only the primary info
- Make it concise and simple
- {consider}

##
View #<Number>:
Step 1. Primary Information:
Step 2. Secondary Information:
Step 3. Utterance:
"""
    return prompt


def get_prompt_question(vl, decision, questionType, visualizationType):
    if questionType == "lookup" and visualizationType == "visual":
        prompt = f"""
{vl}

Let's generate a lookup question for a given Vega-Lite spec step by step. The lookup question requires a single value retrieval. The higher-level decision by analyzing this chart is:
{decision}

Step 1. What is a possible conclusion that can be reached from this decision?
Step 2. What specific value can be retrieved to reach this conclusion?
Step 3. Generate a lookup question using this value, without including any visual attributes such as color, length, size, or position.

##
Step 1. Conclusion: 
Step 2. Specific Value:
Step 3. Question: 
"""
    elif questionType == "lookup" and visualizationType == "nonvisual":
        prompt = f"""
{vl}

Let's generate a lookup question for a given Vega-Lite spec step by step. The lookup question requires a single value retrieval. The higher-level decision by analyzing this chart is:
{decision}

Step 1. What is a possible conclusion that can be reached from this decision?
Step 2. What specific value can be retrieved to reach this conclusion?
Step 3. Generate a lookup question using this value, by including visual attributes such as color, length, size, or position.

##
Step 1. Conclusion: 
Step 2. Specific Value:
Step 3. Question: 
"""
    elif questionType == "compositional" and visualizationType == "visual":
        prompt = f"""
{vl}

Let's generate a compositional question for a given Vega-Lite spec step by step. The compositional question requires multiple operations. The higher-level decision by analyzing this chart is:
{decision}

Step 1. What is a possible conclusion that can be reached from this decision?
Step 2. What are the mathematical operations (e.g., max, min, sum, difference, and average) to reach the conclusion?
Step 3. Generate a compositional question using this value, without including any visual attributes such as color, length, size, or position.

##
Step 1. Conclusion: 
Step 2. Operations: 
Step 3. Question: 
"""
    elif questionType == "compositional" and visualizationType == "nonvisual":
        prompt = f"""
{vl}

Let's generate a compositional question for a given Vega-Lite spec step by step. The compositional question requires multiple operations. The higher-level decision by analyzing this chart is:
{decision}

Step 1. What is a possible conclusion that can be reached from this decision?
Step 2. What are the mathematical operations (e.g., max, min, sum, difference, and average) to reach the conclusion in Step 2?
Step 8. Generate a compositional question using this operations, by including visual attributes such as color, length, size, or position.

##
Step 1. Conclusion: 
Step 2. Operations: 
Step 3. Question: 
"""
    else:
        prompt = f"""
{vl}

Let's generate an open-ended question for a given Vega-Lite spec step by step. The higher-level decision by analyzing this chart is:
{decision}

Step 1. What is a possible conclusion that can be reached from this decision?
Step 2. Generate an open-ended question to reach the conclusion.

##
Step 1. Conclusion: 
Step 2. Question: 
"""

    return prompt


def get_prompt_paraphrase(nl, selectedAxis, axisScore):
    if selectedAxis == "clarity":
        num = 0
    elif selectedAxis == "expertise":
        num = 1
    elif selectedAxis == "formality":
        num = 2
    elif selectedAxis == "subjectivity":
        num = 3
    else:
        num = -1

    prompt = f"""
{AXES[num][2]}
Score of 1 indicates a higher tendency to use {AXES[num][0]} language and a Score of 5 indicates a higher tendency to use {AXES[num][1]} language. Rewrite the following sentence as if it were spoken by a person with a given score for language usage.

Sentence: {nl}
Score: {axisScore}

##
Paraphrase:
"""
    return prompt
