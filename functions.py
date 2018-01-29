import random

#This file was made by badooga so that you don't have to make these noob functions; just import what you need from this module into whatever file you are using and you'll be able to use these functions with ease. Made by a python novice, so if you look at the code and think "that's inefficient", that's probably why. But it *should* work, so it's not a problem - if for some reason something goes wrong though, that's a different story.
#You are free to distribute this file whoever and wherever you want - just give me credit when doing so
#Anyway, the comments below document how the code actually works, if you are interested.


#for all input-related functions - prompt = what you want to ask

#input_num - asks for input, only accepts a number that satisfies the parameter-specified conditions repeats prompt until it gets one
#float_or_int - if you want the input number to be a float or int (False is either); bound_lower and bound_upper - the lower and upper bounds that a number must be within, False is infinity, double False means bound check is ignored completely; inclusive_lower and inclusive_upper - if a particular bound is inclusive or not (i.e. greater than or equal to or just greater than), bool; convert_string - if set to True, returns the str() version of the number
def input_num(prompt, float_or_int=False, bound_lower=False, bound_upper=False, inclusive_lower=True, inclusive_upper=True, convert_string=False):
    bound = [bound_lower, bound_upper]
    inclusive = [inclusive_lower, inclusive_upper]

    input_type_2 = ""
    if float_or_int == float:
        input_type = "float"
    elif float_or_int == int:
        input_type = "integer"
        input_type_2 = "n"
    else:
        input_type = "number"
    invalid_input = "Please input a valid {}.".format(input_type)

    inclusive_0 = ""
    inclusive_1 = ""
    if inclusive[0]:
        inclusive_0 = "or equal to "
    if inclusive[1]:
        inclusive_1 = "or equal to "
    num_valid = False
    while not num_valid:
        num_input = input(prompt)
        try:
            try:
                if float_or_int == float:
                    num_test = int(num_input)
                    print(invalid_input)
                else:
                    if int(num_input) == float(num_input):
                        num_input = int(num_input)
                        num_valid = True
                    else:
                        num_input = float(num_input)
            except:
                if float_or_int == int:
                    print(invalid_input)
                else:
                    num_input = float(num_input)
                    num_valid = True
        except:
            if float_or_int == float:
                print(invalid_input)
            else:
                print(invalid_input)
        if num_valid and not str(bound) == "[False, False]": #str() and quotes prevent bound=[0, False] or things like that from passing
            num_valid = False
            if str(bound[0]) == "False":
                if (not inclusive[1] and not num_input < bound[1]) or (inclusive[1] and not num_input <= bound[1]):
                    print("Please input a{} {} ".format(input_type_2, input_type) + "less than " + inclusive_1 + "{}.".format(bound[1]))
                else:
                    num_valid = True
            elif str(bound[1]) == "False":
                if (not inclusive[0] and not num_input > bound[0]) or (inclusive[0] and not num_input >= bound[0]):
                    print("Please input a{} {} ".format(input_type_2, input_type) + "greater than " + inclusive_0 +  "{}.".format(bound[0]))
                else:
                    num_valid = True
            else:
                if inclusive[0] and inclusive[1]:
                    if not bound[0] <= num_input <= bound[1]:
                        print("Please input a{} {} ".format(input_type_2, input_type) + "greater than " + inclusive_0 + "{} ".format(bound[0]) + "and less than " + inclusive_1 + "{}.".format(bound[1]))
                    else:
                        num_valid = True
                elif inclusive[0]:
                    if not bound[0] <= num_input < bound[1]:
                        print("Please input a{} {} ".format(input_type_2, input_type) + "greater than " + inclusive_0 + "{} ".format(bound[0]) + "and less than " + inclusive_1 + "{}.".format(bound[1]))
                    else:
                        num_valid = True
                elif inclusive[1]:
                    if not bound[0] < num_input <= bound[1]:
                        print("Please input a{} {} ".format(input_type_2, input_type) + "greater than " + inclusive_0 + "{} ".format(bound[0]) + "and less than " + inclusive_1 + "{}.".format(bound[1]))
                    else:
                        num_valid = True
                else:
                    if not bound[0] < num_input < bound[1]:
                        print("Please input a{} {} ".format(input_type_2, input_type) + "greater than " + inclusive_0 + "{} ".format(bound[0]) + "and less than " + inclusive_1 + "{}.".format(bound[1]))
                    else:
                        num_valid = True
    if convert_string:
        return str(num_input)
    else:
        return num_input

#input_str - asks for input, only accepts a string (as in, no answers that can be converted to floats or ints), repeats prompt until it gets one
#nums_allowed - removes the "no floats or ints" rule; length - if you want the input string to be a certain length, specify here (optional); minimum - if True, changes conditional to require a string with a length greater than or equal to length
def input_str(prompt, nums_allowed=False, length=False, minimum=False):
    str_input = input(prompt)
    str_valid = False
    min_string = ""
    if minimum:
        min_string = " or more"
    while not str_valid:
        str_valid = True
        if not nums_allowed:
            for i in range(len(str_input)):
                try:
                    str_valid = False
                    str_test = float(str_input[i])
                    break
                except:
                    str_valid = True
        if not str_valid:
            print("Please input a valid string.")
            str_input = input(prompt)
        if str_valid and not str(length) == "False":
            if (not minimum and not len(str_input) == length) or (minimum and not len(str_input) >= length):
                print("Please input a string that is {}{} characters long.".format(length, min_string))
                str_input = input(prompt)
                str_valid = False
    return str(str_input)

#input_question - asks for input that matches one of the choices in the choices list (choices_list should have at least 2 elements), returns a number equal to the index of the choice the user chooses; choices are entered as the second parameter via a list.
def input_question(prompt, choices_list):
    answer_valid = False
    invalid = "Please input "
    for choice in choices_list:
        if choice.index(choice) == len(choices_list) - 1:
            invalid = invalid + "or {} .".format(choice)
        else:
            invalid = invalid + "{}, ".format(choice)
    if len(choices_list) == 2:
        invalid = "Please input {} or {}.".format(choices_list[0] ,choices_list[1])
    while not answer_valid:
        answer = input(prompt)
        if answer not in choices_list:
            print(invalid)
        else:
            return answer

#input_characters - asks for input, only accepts it if it is only made up of characters found in the parameter string; prints a parameter specified error message if it's invalid (also prints a different message if it is the wrong length, if specified. can be used as an alternative to the above function or can be used for other purposes
def input_characters(prompt, characters_string, error_message="Input contains invalid characters. Please try again.", length=False):
    valid = False
    while not valid:
        answer = input(prompt)
        if answer == "":
            print("Please input a valid response.")
        else:
            valid = True
            for character in answer:
                if character not in characters_string and valid:
                    print(error_message)
                    valid = False
        if valid and not length:
            if len(answer) != length:
                print("Please input a response that is {} characters long.".format(length))
                valid = False
        

#input_split - asks for input, only accepts a string, splices the string into individual words and puts each word into a list.
def input_split(prompt, nums_allowed=False, length=False, minimum=False):
    return input_str(prompt, nums_allowed, length, minimum).split(" ")

#XdY+Z_roller - Rolls a Y sided die X times, can add multiple types of dice, adds modifier Z and prints total
def XdY_Z_roller():
    rolls = []
    sides = []
    add_more = "yes"
    current_dice = "Current dice: "
    while add_more == "yes":
        rolls.append(input_num("Number of dice to roll: ", int, 1))
        sides.append(input_num("Number of sides: ", int, 1))
        if len(rolls) > 1:
            current_dice = current_dice + " + "
        current_dice = current_dice + "{}d{}".format(rolls[-1], sides[-1])
        print(current_dice)
        add_more = input_question("Add more types of dice?", ["yes", "no"])
    mod = input_num("Modifier: ", int)
    result = mod
    for i in range(1, len(rolls)):
        for dice in range(rolls[i]):
            result = result + random.randint(1, sides[i])
        print(result)

#the following dicts are to be used by the metric_conversions function

metric_prefixes = {
    "peta": 10**15,
    "tera": 10**12,
    "giga": 10**9,
    "mega": 10**6,
    "kilo": 1000,
    "deca": 10,
    "deci": .1,
    "centi": .01,
    "milli": .001,
    "micro": .000001,
    "nano": 10**-9,
    "pico": 10**-12,
    "": 1
}

#keep as dict in case shorthand prefixes (e.x. cm for centimeters) are to be added at a later date
metric_units = {
    "meters": "meters",
    "grams": "grams",
    "liters": "liters",
    "joules": "joules",
    "newtons": "newtons",
    "degrees c": "degrees C",
    "kelvin": "kelvin",
    "pascals": "pascals",
    "ohms": "ohms",
    "volt": "volt",
    "coulomb": "coulomb",
    "watt": "watt",
    "tesla": "tesla",
    "weber": "weber",
    "farad": "farad",
    "lumen": "lumen",
    "hertz": "hertz"

    #add prefixes below

}

time_units = {
    "seconds": 1,
    "sec": 1,
    "s": 1,
    "minutes": 60,
    "min": 60,
    "hours": 3600,
    "h": 3600,
    "days": 3600 * 24,
    "years": 3600 * 24 * 365,
    "yr": 3600 * 24 * 365
}

#metric_conversions - pass a quantity and a unit for that quantity that is in a dict above, and it'll return a new quantity that is converted to unit2
#quantity - the amount of unit1 you have; unit1 - your original unit; unit2 - the unit you are converting to
def metric_conversions(quantity, unit1, unit2):
    final_conversion = None
    try:
        if unit1 in time_units.keys():
            final_conversion = quantity * time_units[unit1]/time_units[unit2]
        else:
            stop = True
            #first, let's get the prefix and base unit of unit1:
            for key in metric_prefixes.keys():
                if stop and unit1.replace(key, "") in metric_units.values():
                    base_unit = unit1.replace(key, "")
                    prefix_1 = key
                    stop = False
                if unit1 in metric_units.keys():
                    prefix_1 = ""
            stop = True
            #now for the prefix of unit2:
            for key2 in metric_units.keys():
                if unit2.replace(base_unit, "") in metric_prefixes.keys() and stop:
                    prefix_2 = unit2.replace(base_unit, "")
                    stop = False
            final_conversion = quantity * metric_prefixes[prefix_1]/metric_prefixes[prefix_2]
        return final_conversion
    except:
        #if you are using this function in conjunction with your own function, treat False as an error
        return False

#lorem_ipsum - prints a string 
#words - number of words this function will generate; if words is not specified (or a number less than 1 is entered), it will ask the user for input instead; print_output - if True, it will print the variable output instead of returning it (useful if you are the enduser and want to just copy the text from the cmd or something like that)
def lorem_ipsum(words=0, print_output=False):
    if words < 1:
        str_length = input_num("Words: ", int, 1)
    else:
        str_length = words
    string = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.".split(" ")
    output = ""
    loop = 0
    for i in range(str_length):
        j = i
        while j > 68:
            j = j - 69
        output += string[j] + " "
    output = output.rstrip()
    if output[-1] == ",":
        output = output.rstrip(",")
    if not output[-1] == ".":
        output += "."
    if print_output:
        print(output)
    else:
        return output

lorem_ipsum(69*2, True)
