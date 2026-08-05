'''1. Variables and primitive data types — 10 minutes
Read the Python 3.12 documentation sections on numbers, variable assignment and strings. Python distinguishes
integers such as 20, floating-point values such as 1.6, and strings such as "1975"; assignment associates a 
variable name with a value.'''

participant_id = "SYN-001"
age = 42
temperature_c = 36.8
consent_confirmed = True
missing_value = None

print(participant_id, type(participant_id))
print(age, type(age))
print(temperature_c, type(temperature_c))
print(consent_confirmed, type(consent_confirmed))
print(missing_value, type(missing_value))

'''2. Conditions — 8 minutes
Read the official if, elif and else section. An if chain evaluates conditions in sequence; elif avoids unnecessary
nested indentation, while else handles cases not matched earlier.'''
age = 42
if age < 18:
    print("Minor")
elif age < 65:
    print("Adult")
else:
    print("Older Adult")

# 1. ASSIGNMENT (=): Setting the patient's age when they arrive
patient_age = 42   # "Store 42 inside patient_age"


# 2. COMPARISON (==): Checking if the patient is eligible for a senior discount
if patient_age == 65:
    print("Eligible for senior discount!")
else:
    print("Standard adult rate applies.")

# List ages and iterate through them
ages = [42, 99, 80]

for age in ages:
    if age < 18:
        print(f"Age {age}: Minor")
    elif age < 65:
        print(f"Age {age}: Adult")
    else:
        print(f"Age {age}: Older Adult")

'''3. Boolean logic — 5 minutes
Read the official documentation on boolean operations and logical operators in Python.'''
x = True
y = False
z = x and y  # False
w = x or y   # True
v = not x    # False

age = 42
consent_confirmed = True
eligible = age >= 18 and consent_confirmed
print(eligible)

age = 42
consent_confirmed = False
eligible = age >= 18 and consent_confirmed
print(eligible)

age = 42
age >= 18 and consent_confirmed # type: ignore
age < 18 or age > 18 # type: ignore
not consent_confirmed # type: ignore
'''OR''' '''OR''' '''OR''' '''OR''' '''OR''' '''OR''' '''OR''' '''OR''' '''OR''' '''OR''' '''OR''' '''OR'''
print(age >= 18 and consent_confirmed)
print(age < 18 or age > 18)
print(not consent_confirmed)

'''4. for and range() — 5 minutes
Read the official documentation on for loops and the range() function. A for loop iterates over a sequence of values,
Python’s for statement iterates over items in a sequence. range() produces a sequence of integers for iteration,
and its ending value is excluded. For example, range(1, 6) produces 1, 2, 3, 4, 5.'''

for visit_number in range(1, 6):
    print(f"Visit {visit_number}")

'''5. while loops — 5 minutes
Read the official documentation on while loops. A while loop continues to execute as long as a condition is true.
A while loop continues as long as its condition remains true. Python uses indentation to determine which statements
belong to the loop.'''

count = 0
while count < 5:
    print(f"Count {count}")
    count += 1

attempt = 1
while attempt <= 3:
    print(f"Attempt: {attempt}")
    attempt += 1

attempt = 5
while attempt <= 400:
    print(f"Attempt: {attempt}")
    attempt *= 5

attempt = 5
while attempt <= 400:
    print(f"Attempt: {attempt}")
    attempt -= (-50)

attempt = 5
while attempt <= 400:
    print(f"Attempt: {attempt}")
    attempt -= -50

'''6. Functions — 5 minutes
A function is introduced with def, followed by its name and parameters. Its body must be indented.
A return statement sends a value back to the caller; a function without an explicit return produces None.'''

def classify_age(age: int) -> str:
    """Return a broad synthetic-study age category."""
    '''Condition inside a function body is indented. The function returns a string based on the age input.'''
    if age < 18:
        return "minor"
    if age < 65:
        return "adult"
    return "older_adult"


result = classify_age(42)
print(result)
