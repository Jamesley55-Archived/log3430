import json

import xmltodict


def format_pytest_data():
    with open("q7_pytest.xml", 'r') as xml_file:
        pytest_raw_data = xmltodict.parse(xml_file.read())["coverage"]["packages"]["package"]["clases"]['class']

    line_executed = {}

    for file in pytest_raw_data:
        line_covered = []
        for line in file["lines"]["line"]:
            if line["@hits"] == '1':
                line_covered.append(int(line["@number"]))
        line_executed['requests/' + file["@name"]] = line_covered
    return line_executed


def format_coverage_py_data():
    with open("q7_coverage_py.json", 'r') as json_file:
        coverage_py_raw_data = json.load(json_file)['files']

    line_executed = {}
    for fileName in coverage_py_raw_data.keys():
        line_executed[fileName] = coverage_py_raw_data[fileName]['executed_lines']

    return line_executed


def compared_both_methods():
    pytest_data = format_pytest_data()
    coverage_data = format_coverage_py_data()

    results = {}

    for fileName in pytest_data.keys():
        results[fileName] = sorted(list(set(pytest_data[fileName] + coverage_data[fileName])))

    with open("q7.json", 'w') as comparator_report:
        json.dump(results, comparator_report)


if __name__ == "__main__":
    compared_both_methods()
