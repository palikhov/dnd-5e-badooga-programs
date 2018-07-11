from random import *
from subprocess import check_call
from fractions import Fraction

#This file was made by badooga for your convenience; just import what you need from this module into whatever file you are using and you'll be able to use these functions with ease.
#You are free to distribute this file wherever you want (the most updated version can probably be found at https://github.com/badooga/Python-Files) - just give me credit when doing so
#Anyway, the comments below document how the code actually works, if you are interested.


#for all input-related functions - prompt = what you want to ask

#Data - used in the statistical analysis functions, or can be used by itself; takes a list of numbers as its parameter when called, allowing statistical information to be derived via these methods
class Data(object):
    def __init__(self, data):
        self.data = sorted(data) #sorts the data list automatically so that you don't have to
        self.data_len = len(self.data)

        frequency_dict = {x:0 for x in self.data}
        for point in self.data:
            frequency_dict[point] += 1

        self.frequency_dict = frequency_dict

    def median(self):
        if self.data_len == 2:
            median = (self.data[0] + self.data[1])/2
        elif self.data_len % 2 == 0:
            median = (self.data[int(self.data_len/2)] + self.data[int(-1 + self.data_len/2)])/2
        else:
            median = self.data[int(self.data_len/2 - .5)]
        return median
        
    def mean(self):
        mean = 0
        for data_point in self.data:
            mean += data_point/self.data_len
        return mean

    def mode(self, string=False): #string - if you want this method to return a string of the modes instead of a list of them, then make this parameter True when calling the method
        counter = 0
        mode_list = []
        for data_point in self.frequency_dict.keys():
            if self.frequency_dict[data_point] >= counter and data_point not in mode_list:
                counter = self.frequency_dict[data_point]
                mode_list.append(data_point)
        i = 0
        while i < len(mode_list):
            if self.frequency_dict[mode_list[i]] < counter:
                del mode_list[i]
            else:
                i += 1
        if mode_list == []:
            mode_list = None
            return mode_list
        if string == True:
            if len(mode_list) > 1:
                mode_string = ""
                for k in range(len(mode_list)):
                    if k == 0:
                        mode_string += "{}".format(mode_list[k])
                    else:
                        mode_string += ", {}".format(mode_list[k])
            else:
                mode_string = str(mode_list[0])
            return mode_string
        else:
            return mode_list

    def variance(self,pop_or_samp=True): #pop_or_samp - population or standard deviation, True is population, False is sample
        s_mean = self.mean()
        variance = 0
        n = self.data_len
        if not pop_or_samp:
            n = n - 1
        for i in self.data:
            variance += 1/n * (i - s_mean)**2
        return variance

    def standard_deviation(self,pop_or_samp=True): #pop_or_samp - see above
        return self.variance(pop_or_samp) ** .5

    def range(self): #fun fact - there is no need for a minimum or maximum method; just use self.data[0] for the minimum and self.data[-1] for the maximum
        return self.data[-1] - self.data[0]

    def q1(self):
        if self.data_len % 2 == 0:
            splice = int(self.data_len/2)
        else:
            splice = int(self.data_len/2-.5)
        first_half = self.data[:splice]
        if self.data_len == 2:
            q1 = self.data[0]
        elif self.data_len == 3:
            q1 = (self.data[0] + self.data[1])/2
        elif len(first_half) % 2 == 0:
            if len(first_half) == 2:
                q1 = (first_half[0] + first_half[1])/2
            else:
                q1 = (first_half[1 + int(len(first_half)/2)] + first_half[-1 + int(len(first_half)/2)])/2
        else:
            q1 = first_half[int(len(first_half)/2 - .5)]
        return q1

    def q3(self):
        if self.data_len % 2 == 0:
            splice = int(self.data_len/2+1)
        else:
            splice = int(self.data_len/2+.5)
        second_half = self.data[splice:]
        if self.data_len == 2:
            q3 = self.data[1]
        elif self.data_len == 3:
            q3 = (self.data[1] + self.data[2])/2
        elif len(second_half) % 2 == 0:
            if len(second_half) == 2:
                q3 = (second_half[0] + second_half[1])/2
            else:
                q3 = (second_half[int(1 + len(second_half)/2)] + second_half[int(-1 + len(second_half)/2)])/2
        else:
            q3 = second_half[int(len(second_half)/2 - .5)]
        return q3

    def iqr(self): #interquartile range
        return self.q3() - self.q1()

    def z_score(self, number, pop_or_samp=True): #z_score - calculates the z-score of a given number; pop_or_samp - see above
        return (number - self.mean())/self.standard_deviation()

    def outliers(self): #returns a list of data outliers according to the following definition: an outlier is a point which falls more than 1.5 times the interquartile range above the third quartile or below the first quartile.
        upper_bound = self.q3() + 1.5 * self.iqr()
        lower_bound = self.q1() - 1.5 * self.iqr()
        outliers = []
        for point in self.data:
            if point > upper_bound or point < lower_bound:
                outliers.append(point)
        return outliers
    
    def frequency(self, number): #obtains the frequency of a given number within the data list; if it's not present, 0 is returned; if you just want to detect if a number is in the list or not, try using bool() on the output or using a conditional for > 1
        try:
            return self.frequency_dict[number]
        except KeyError:
            return 0
        
#input_num - asks for input, only accepts a number that satisfies the parameter-specified conditions repeats prompt until it gets one
#float_or_int - if you want the input number to be a float or int (False is either), float and False also include improper and proper fractions; bound_lower and bound_upper - the lower and upper bounds that a number must be within, False is infinity, double False means bound check is ignored completely; inclusive_lower and inclusive_upper - if a particular bound is inclusive or not (i.e. greater than or equal to or just greater than), bool; convert_string - if set to True, returns the str() version of the number
def input_num(prompt, float_or_int=False, bound_lower=False, bound_upper=False, inclusive_lower=True, inclusive_upper=True, convert_string=False):
    bound = [bound_lower, bound_upper]
    inclusive = [inclusive_lower, inclusive_upper]
    numbers = [str(i) for i in range(0,10)] + ["-"]
    input_type_2 = ""
    inclusive_0 = ""
    inclusive_1 = ""
    input_type = "number"

    if float_or_int == float:
        input_type = "float"
    elif float_or_int == int:
        input_type = "integer"
        input_type_2 = "n"
    if inclusive[0]:
        inclusive_0 = "or equal to "
    if inclusive[1]:
        inclusive_1 = "or equal to "

    invalid_input = "Please input a valid {}.".format(input_type)
    bound_error = "Please input a{} {} ".format(input_type_2, input_type) + "greater than " + inclusive_0 + "{} ".format(bound[0]) + "and less than " + inclusive_1 + "{}.".format(bound[1])

    while True:
        num_input = input(prompt)
        try:
            if float_or_int == float:
                num_input = float(Fraction(num_input))
                elif "." not in num_input:

            elif float_or_int == int:
                for j in num_input:
                    if j not in numbers:
                        raise TypeError
                else:
                    num_input = int(num_input)   
            else: 
                try:
                    if int(num_input) == float(num_input):
                        num_input = int(num_input)
                    else:
                        raise TypeError
                except:
                    num_input = float(Fraction(num_input))
        except:
            print(invalid_input)
            continue
        
        if str(bound) == "[False, False]": #str() and quotes prevent bound=[0, False] or things like that from passing
            break
        elif str(bound[0]) == "False":
            if (not inclusive[1] and not num_input < bound[1]) or (inclusive[1] and not num_input <= bound[1]):
                print("Please input a{} {} ".format(input_type_2, input_type) + "less than " + inclusive_1 + "{}.".format(bound[1]))
            else:
                break
        elif str(bound[1]) == "False":
            if (not inclusive[0] and not num_input > bound[0]) or (inclusive[0] and not num_input >= bound[0]):
                print("Please input a{} {} ".format(input_type_2, input_type) + "greater than " + inclusive_0 +  "{}.".format(bound[0]))
            else:
                break
        else:
            if inclusive[0] and inclusive[1]:
                if not bound[0] <= num_input <= bound[1]:
                    print(bound_error)
                else:
                    break
            elif inclusive[0]:
                if not bound[0] <= num_input < bound[1]:
                    print(bound_error)
                else:
                    break
            elif inclusive[1]:
                if not bound[0] < num_input <= bound[1]:
                    print(bound_error)
                else:
                    break
            else:
                if not bound[0] < num_input < bound[1]:
                    print()
                else:
                    break
    if convert_string:
        return str(num_input)
    else:
        return num_input

#input_str - asks for input, only accepts a string (as in, no answers that can be converted to floats or ints), repeats prompt until it gets one
#nums_allowed - removes the "no floats or ints" rule; length - if you want the input string to be a certain length, specify here (optional); minimum - if True, changes conditional to require a string with a length greater than or equal to length
def input_str(prompt, nums_allowed=False, length=False, minimum=False):
    min_string = ""
    numbers = [str(i) for i in range(0,10)]
    numbers.append("-")
    if minimum:
        min_string = " or more"
    while True:
        str_input = input(prompt)
        if not nums_allowed:
            for j in str_input:
                if j in numbers:
                    print("Please input a valid string.")
                    break
            else:
                if len(str_input) == 0:
                    print("Please input a valid string.")
                elif not str(length) == "False":
                    if (not minimum and not len(str_input) == length) or (minimum and not len(str_input) >= length):
                        print("Please input a string that is {}{} characters long.".format(length, min_string))
                else:
                    break
        else:
            break
    return str_input

#input_question - asks for input that matches one of the choices in the choices list (choices_list should have at least 2 elements), returns a number equal to the index of the choice the user chooses; choices are entered as the second parameter via a list.
#case_sensitive - bool that determines whether answers are determined with case sensitivity or not
def input_question(prompt, choices_list, case_sensitive=False):
    invalid = "Please input "
    for choice in choices_list:
        if choices_list[-2] == choice:
            invalid = invalid + "or {} .".format(choice)
        else:
            invalid = invalid + "{}, ".format(choice)
    if len(choices_list) == 2:
        invalid = "Please input {} or {}.".format(choices_list[0] ,choices_list[1])

    if not case_sensitive:
        for i in range(len(choices_list)): choices_list[i] = choices_list[i].lower()

    while True:
        answer = input(prompt)
        if not case_sensitive:
            answer = answer.lower()
        if answer not in choices_list:
            print(invalid)
        else:
            return answer

#input_characters - asks for input, only accepts it if it is only made up of characters found in the parameter list (or string); prints a parameter specified error message if it's invalid (also prints a different message if it is the wrong length, if specified. Can be used as an alternative to the above input functions or can be used for other purposes)
def input_characters(prompt, characters, error_message="Input contains invalid characters. Please try again.", length=False):
    for i in range(len(characters)):
        characters[i] = str(characters[i])
    while True:
        answer = input(prompt)
        if answer == "":
            print("Please input a valid response.")
        else:
            for character in answer:
                if character not in characters:
                    print(error_message)
                    break
            else:
                if length != False and len(answer) != length:
                    print("Please input a response that is {} characters long.".format(length))
                    continue
                return answer
        

#input_split - asks for input, only accepts a string, splices the string into individual words and puts each word into a list.
def input_split(prompt, nums_allowed=False, length=False, minimum=False):
    return input_str(prompt, nums_allowed, length, minimum).split(" ")

#XdY+Z_roller - Rolls a Y sided die X times, can add multiple types of dice, adds modifier Z and prints total
#allow repeats - if False, the user is only allowed to make one roll and that's it
def XdY_Z_roller(allow_repeats=True):
    rolls = []
    sides = []
    current_dice = ""
    while True:
        rolls.append(input_num("Number of dice to roll: ", int, 1))
        sides.append(input_num("Number of sides: ", int, 2))

        if len(rolls) > 1:
            current_dice = current_dice + " + "
        current_dice = current_dice + "{}d{}".format(rolls[-1], sides[-1])
        print("Current dice: " + current_dice)

        if input_question("Add more types of dice (Y/N)? ", ["y", "n"]) == "n":
            break

    mod = input_num("Modifier: ", int)
    result = mod
    mod_str = ""
    if mod != 0:
        mod_str = " + {}".format(mod)

    for i in range(len(sides)):
        for rolls_made in range(rolls[i]):
            result = result + randint(1, sides[i])          
    print("Result: " + str(result))

    while allow_repeats:
        d_loop = False
        d_continue = input_num("\nDice commands: Quit (1), Roll {} Again (2), New Roll (3)\nCommand: ".format(current_dice + mod_str))
        if d_continue == 1:
            break
        elif d_continue == 2:
            result = mod
            for i in range(len(sides)):
                for rolls_made in range(rolls[i]):
                    result = result + randint(1, sides[i])
            print("Result: " + str(result))
        elif d_continue == 3:
            d_loop = True
            break
        else:
            print("Invalid command. Please try again.")
    if d_loop:
        XdY_Z_roller()

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
                
#statistical_analysis_input - allows a data set to be inputed by the enduser; use in conjunction with other stat analysis functions
#length - how many data points to be inputed by the user, default allows the user to pick; bFrequency - if you want to allow the user to quickly add a single number multiple times to a set, set this to True
def statistical_analysis_input(length=1, bFrequency=False):
    data_final = []
    if length < 2:
        length = input_num("Length of data set: ", int, 1, False, False)
    for i in range(length):
        data_point = input_num("Data value {}: ".format(i+1))
        if bFrequency:
            frequency = input_num("Frequency: ", int, 1)
            for j in range(frequency):
                data_final.append(data_point)
        else:
            data_final.append(data_point)

    return Data(data_final)

#statistical_analysis_print - prints out the following information about a list of data (must be a Data object)
#d - the Data object you want to use; obtain via statistical_analysis_input() or manually
def statistical_analysis_print(d):
    print("Median: " + str(d.median()))
    print("Mean: " + str(d.mean()))
    print("Mode: " + str(d.mode(True)))
    print("Minimum: " +  str(d.data[0]))
    print("Maximum: " + str(d.data[-1]))
    print("Range: " + str(d.range()))
    print("Q1: " + str(d.q1()))
    print("Q3: " + str(d.q3()))
    print("Interquartile Range: " + str(d.iqr()))
    print("Variance: " + str(d.variance()))
    print("Standard Devation: " + str(d.standard_deviation()))

#copy2clip - copies given text to the clipboard. original found at https://stackoverflow.com/questions/11063458/python-script-to-copy-text-to-clipboard/41029935#41029935
#txt - text to copy; prnt - set to True if you want to also print the copied text
def copy2clip(txt, prnt=False):
    cmd='echo '+ txt +'|clip'
    content = check_call(cmd, shell=True)
    if prnt:
        print(txt)
    return content

#glitchtext - creates random glitchy text of a set length and copies it to the clipboard. original by Dan Salvato
#length - if you want to specify the length of the string when calling the function instead of having the user specify it, change this; p_c - if True, prints the glitchtext and copies it to the clipboard, otherwise it just returns the output
def glitchtext(length=0, p_c=False):
    nonunicode = "¡¢£¤¥¦§¨©ª«¬®¯°±²³´µ¶·¸¹º»¼½¾¿ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖ×ØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõö÷øùúûüýþÿĀāĂăĄąĆćĈĉĊċČčĎďĐđĒēĔĕĖėĘęĚěĜĝĞğĠġĢģĤĥĦħĨĩĪīĬĭĮįİıĲĳĴĵĶķĸĹĺĻļĽľĿŀŁłŃńŅņŇňŉŊŋŌōŎŏŐőŒœŔŕŖŗŘřŚśŜŝŞşŠšŢţŤťŦŧŨũŪūŬŭŮůŰűŲųŴŵŶŷŸŹźŻżŽž"
    if length < 1:
        length = input_num("Length: ", int, 1)
    output = ""
    for x in range(length):
        output += choice(nonunicode)
    if p_c:
        print(output)
        copy2clip(output)
    else:
        return output
