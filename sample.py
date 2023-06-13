import re


def normalize_code(input_str):
    # Remove non-alphanumeric characters and convert to lowercase
    normalized_str = re.sub(r'[^a-zA-Z0-9]', '', input_str.lower())
    return normalized_str


def normalize_input(input_str):
    input_str = input_str.lower()
    return input_str


def normalize_professor(name):
    # remove professor, prof, dr., etc from name
    name = re.sub(r'professor', '', name.lower())
    name = re.sub(r'prof.', '', name.lower())
    name = re.sub(r'prof', '', name.lower())
    name = re.sub(r'dr.', '', name.lower())
    name = re.sub(r'dr', '', name.lower())
    return name


def format_list_to_string(list_obj):
    return '\n'.join(list_obj)


courses = ['nlp201', 'nlp202', 'nlp203', 'nlp204']

print(format_list_to_string(courses))

prof = "prof. Ian lane"
print(normalize_professor(prof))
exit()

# Prompt the user for input
user_input = input("Enter your input: ")

# Normalize the input
normalized_input = normalize_code(user_input)

# Compare the normalized input with a reference value
reference_value = "nlp201"
if normalized_input == normalize_code(reference_value):
    print('match')
else:
    print('no match')
