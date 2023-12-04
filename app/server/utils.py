import re


def most_frequent_element(lst):
    frequency = {}
    for element in lst:
        if element in frequency:
            frequency[element] += 1
        else:
            frequency[element] = 1
    return max(frequency, key=frequency.get)


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
                if "title" in json_data and isinstance(json_data["title"], str):
                    result[field]["title"].append(json_data["title"])
                if (
                    "axis" in json_data
                    and isinstance(json_data["axis"], dict)
                    and "title" in json_data["axis"]
                    and isinstance(json_data["axis"]["title"], str)
                ):
                    result[field]["title"].append(json_data["axis"]["title"])
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


def get_ftt_str(json, data, num_values=5):
    data_columns = data.columns
    ftt = get_ftt(json)
    ftt_str = ""

    for field, value in ftt.items():
        if field in data_columns:
            ftt_str += f"Field: {field}"
            value["title"] = list(set(filter(None, value["title"])))
            if value["title"]:
                ftt_str += f" ({', '.join(value['title'])})"
            if value["type"]:
                dtype = most_frequent_element(value["type"])
                ftt_str += f", Type: {dtype}"
                if dtype in ["nominal", "ordinal"]:
                    column = data[field]
                    ftt_str += f", Value: {column.unique()[:num_values]}"
            ftt_str += "\n"
    return ftt_str.rstrip("\n")


def get_nl(text, pattern):
    try:
        match = re.search(pattern, text, flags=re.DOTALL)
        return match.group(1).strip()
    except:
        return "<GET_NL_ERROR>"


def get_instruction(instructions, semantics):
    utterance_first = []

    views = instructions.split("<%>")
    views = [view for view in views if view != ""]

    for i, view in enumerate(views):
        split_string = view.split(";")

        selected_elements_first = [
            element.strip()
            for element in split_string
            if any(f"[{semantic}]" in element for semantic in semantics)
        ]

        result_first = "; ".join(selected_elements_first)
        result_first = f"View #{i+1}. " + result_first

        if result_first:
            utterance_first.append(result_first)
        else:
            utterance_first.append("")

    return utterance_first
