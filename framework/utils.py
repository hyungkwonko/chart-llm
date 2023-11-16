import re


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
    # [
    #     "Figurative",
    #     "Literal",
    #     "Figurative language uses figures of speech such as metaphors, similes, and personification to convey meaning beyond the literal interpretation of the words, while literal language uses the exact meaning of the words without imagination or exaggeration.",
    # ],
    # [
    #     "Denotative",
    #     "Connotative",
    #     "Denotative language refers to the literal or dictionary meaning of a word, while connotative language refers to the emotional or cultural associations that a word may have.",
    # ],
    # [
    #     "Concise",
    #     "Verbose",
    #     "Concise language is brief and to the point, while verbose language uses many words and may be unnecessarily long-winded.",
    # ],
]


def compress_json(json_data):
    compressed_json = re.sub(r"\s+", " ", json_data)
    return compressed_json


def get_nl(text, pattern):
    try:
        match = re.search(pattern, text, flags=re.DOTALL)
        return match.group(1).strip()
    except:
        return "<GET_NL_ERROR>"


def get_nl_all(text, pattern):
    try:
        matches = re.findall(pattern, text, flags=re.DOTALL)
        return [match.strip() for match in matches]
    except:
        return ["<GET_NL_ERROR>"]


def get_ftt(json_data):
    result = {}
    if isinstance(json_data, dict):
        if "field" in json_data:
            if isinstance(json_data["field"], str):
                field = json_data["field"]
                if field not in result:
                    result[field] = {}
                    result[field]["type"] = []
                    result[field]["title"] = []
                if "type" in json_data and isinstance(json_data["type"], str):
                    result[field]["type"].append(json_data["type"])
                # else:
                #     result[field]["type"].append("<UNKNOWN>")
                if "title" in json_data and isinstance(json_data["title"], str):
                    result[field]["title"].append(json_data["title"])
                if (
                    "axis" in json_data
                    and isinstance(json_data["axis"], dict)
                    and "title" in json_data["axis"]
                    and isinstance(json_data["axis"]["title"], str)
                ):
                    result[field]["title"].append(json_data["axis"]["title"])
                # if not result[field]["title"]:
                #     result[field]["title"].append("<UNKNOWN>")
        for _, v in json_data.items():
            if isinstance(v, (dict, list)):
                res = get_ftt(v)
                for k, val in res.items():
                    if k not in result:
                        result[k] = val
                    else:
                        result[k]["type"].extend(val["type"])
                        result[k]["title"].extend(val["title"])
    elif isinstance(json_data, list):
        for item in json_data:
            if isinstance(item, (dict, list)):
                res = get_ftt(item)
                for k, val in res.items():
                    if k not in result:
                        result[k] = val
                    else:
                        result[k]["type"].extend(val["type"])
                        result[k]["title"].extend(val["title"])
    return result


def most_frequent_element(lst):
    frequency = {}
    for element in lst:
        if element in frequency:
            frequency[element] += 1
        else:
            frequency[element] = 1
    return max(frequency, key=frequency.get)


def get_ftt_str(json, data, num_values=5):
    data_columns = data.columns
    ftt = get_ftt(json)
    ftt_str = ""

    for field, value in ftt.items():
        if field in data_columns:
            ftt_str += f"Field: {field}"
            value["title"] = list(set(filter(None, value["title"])))
            if value["title"]:
                # print("titles: ", titles, ", len(titles): ", len(titles))
                ftt_str += f" ({', '.join(value['title'])})"
            if value["type"]:
                dtype = most_frequent_element(value["type"])
                ftt_str += f", Type: {dtype}"
                if dtype in ["nominal", "ordinal"]:
                    column = data[field]
                    # ftt_str += f", Value: {column.unique()}"
                    ftt_str += f", Value: {column.unique()[:num_values]}"
            ftt_str += "\n"
    return ftt_str.rstrip("\n")


def get_instruction(instructions):
    utterance_first, utterance_second = [], []

    views = instructions.split("<%>")
    views = [view for view in views if view != ""]

    for i, view in enumerate(views):
        split_string = view.split(";")

        selected_elements_first = [
            element.strip()
            for element in split_string
            if "[Chart-Type]" in element or "[Encoding]" in element
        ]

        result_first = "; ".join(selected_elements_first)
        result_first = f"View #{i+1}: " + result_first

        if result_first:
            utterance_first.append(result_first)
        else:
            utterance_first.append("")

        selected_elements_second = [
            element.strip()
            for element in split_string
            if "[Style]" in element or "[Interaction]" in element
        ]

        result_second = "; ".join(selected_elements_second)
        result_second = f"View #{i+1}: " + result_second

        if result_second:
            utterance_second.append(result_second)
        else:
            utterance_second.append("")

    return utterance_first, utterance_second


def deprecated_get_instruction(input_string):
    views = input_string.split("<%>")

    views = [view for view in views if view != ""]

    chart_semantics = [
        "Data",
        "Chart-Type",
        "Mark",
        "Encoding",
        "Transform",
        "Style",
        "Interaction",
    ]

    output = {}
    output1 = {}
    output2 = {}

    for view in views:
        view = view.strip()
        view_name, view_content = view.split("; ", 1)
        view_name = view_name.strip("[]")
        output[view_name] = {}
        output1[view_name] = {}
        output2[view_name] = {}
        for semantic in chart_semantics:
            output[view_name][semantic] = []
            if semantic in ["Chart-Type", "Encoding"]:
                output1[view_name][semantic] = []
            elif semantic in ["Style", "Interaction"]:
                output2[view_name][semantic] = []
        instructions = view_content.split("; ")
        for instruction in instructions:
            semantic, content = instruction.split(": ", 1)
            semantic = semantic.strip("[]")
            output[view_name][semantic].append(content)
            if semantic in ["Chart-Type", "Encoding"]:
                output1[view_name][semantic].append(content)
            elif semantic in ["Style", "Interaction"]:
                output2[view_name][semantic].append(content)

    return output, output1, output2


def deprecated_get_fields_types_titles(json_data):
    fields = []
    types = []
    titles = []
    if isinstance(json_data, dict):
        if "field" in json_data:
            if isinstance(json_data["field"], str):
                fields.append(json_data["field"])
                if "type" in json_data and isinstance(json_data["type"], str):
                    types.append(json_data["type"])
                else:
                    types.append("<UNKNOWN>")
                if "title" in json_data and isinstance(json_data["title"], str):
                    titles.append(json_data["title"])
                else:
                    titles.append("<UNKNOWN>")
        for _, v in json_data.items():
            if isinstance(v, (dict, list)):
                f, tp, tt = deprecated_get_fields_types_titles(v)
                fields.extend(f)
                types.extend(tp)
                titles.extend(tt)
    elif isinstance(json_data, list):
        for item in json_data:
            if isinstance(item, (dict, list)):
                f, tp, tt = deprecated_get_fields_types_titles(item)
                fields.extend(f)
                types.extend(tp)
                titles.extend(tt)
    return fields, types, titles


def deprecated_post_field_and_type(fields, types):
    assert len(fields) == len(types), f"fields: {len(fields)} != types: {len(types)}"

    ft_dict = {}
    # ft_str = "- Field: "
    for key, value in zip(fields, types):
        if key not in ft_dict:
            ft_dict[key] = value
            # ft_str += f"{key} ({value}), "

    return ft_dict


def deprecated_get_ft_str(vl_str, data):
    fields, types, titles = deprecated_get_fields_types_titles(vl_str)
    ft_dict = deprecated_post_field_and_type(fields, types)

    ft_str = "Field (Value): "
    for key, value in ft_dict.items():
        if value in ["nominal", "ordinal"]:
            column = data[key]
            unique_values = column.unique()
            ft_str += f"{key} ({unique_values}), "
        else:
            ft_str += f"{key}, "
    ft_str = ft_str[:-2]

    return ft_str
