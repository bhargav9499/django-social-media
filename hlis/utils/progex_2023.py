############################################################################
#
#   IPDS Programming Exercise: January 2023
#
############################################################################
#
#   This file contains all of the information necessary for completing
#   the exercise. It is in 4 parts
#
############################################################################
import math


############################################################################
####################                                ########################
####################  PART 1: GENERAL INSTRUCTIONS  ########################
####################                                ########################
############################################################################

############################################################################
#
#   Part 1 of the file contains important information
#   in a series of comment boxes (like this one)
#
#   Make sure you read all of Part 1 before proceeding
#
############################################################################
#
#   Part 2 contains our program that can be used for testing your code
#   The 'high-level' functions in this program have already been implemented
#   and tested. They call the ones you are required to implement for the
#   exercise, and make use of the values your functions return.
#
#   There is no need to change part 2, but you may do so if you wish to
#   implement your own tests. Part 2 will be removed before marking, so
#   any changes you do make will be ignored by our tester program.
#
############################################################################
#
#   Part 3 of the file contains specifications and code stubs for
#   the functions you are required to implement.
#
#   For each of these functions we have provided
#     a function header, giving its name and parameter list
#     a set of comments that specify what the function should do
#     a code stub that returns an incorrect value
#
#   Your job is to provide a body for each function, which implements
#   its specification and returns the correct data value(s) when tested
#
#   You are not allowed to use any external modules
#   in the solution of these problems (NO IMPORTS)
#
#   Make sure you do not change any of the function headers
#
#   Only code that appears in Part 3 will be marked
#
############################################################################
#
#   Part 4 currently contains an instruction that runs the main program,
#   which can be used for testing your functions
#
#   Part 4 will be removed before marking, so any changes you make to it
#   will not be marked
#
############################################################################

############################################################################
#
#   WHAT YOU HAVE TO DO
#
#   You need to revise Part 3 of this file so that each function meets its
#   specification
#
#   When you have finished you should upload your revised version of the
#   file to Canvas
#     * Please make sure you have inserted your SRN into the
#       code in the manner set out in Part 3
#     * You may change the name of the file if you wish
#       (we suggest you make frequent backups as well)
#     * You may submit as many times as you like
#       (only your final submission will be marked)
#     * Late submissions cannot be accepted
#
#   Your functions will be tested by an automated tester.
#     * Marks are available for each test that is passed
#     * You will get 0 marks for each test that is failed
#     * If your code contains syntax errors it will not be possible to
#       test it, so you may end up with 0 marks for the assignment
#
############################################################################
##########################               ###################################
########################## End of Part 1 ###################################
##########################               ###################################
############################################################################

############################################################################
########################                     ###############################
######################## PART 2: OUR PROGRAM ###############################
########################                     ###############################
############################################################################

############################################################################

#   The code in Part 2 will be removed before marking, so any changes you
#   make to the code in this part of the file will not be marked
#
############################################################################


def Main():
    # 'Top-level' function (main program)
    theList = []  # Start with an empty list of numbers
    # because the user hasn't entered any yet
    # Main loop - repeatedly displays the menu,
    #              gets the user to choose an operation
    #             and carries out that operation
    while True:
        ShowMenu()
        chosen = GetMenuChoice()
        if chosen in ["x", "X"]:  # option x is 'exit the program'
            break
        else:
            theList = ExecuteChoice(chosen, theList)
    print("Thanks for using the program: goodbye")


def ShowMenu():
    print("MENU")
    print("x Exit the program")
    print("1 Display the current list of numbers")
    print("2 Add numbers to the list")
    print("3 Remove numbers from the list")
    print("4 Clear the list of numbers")
    print("5 Find the number of negative numbers in the list")
    print("6 Find the indexes of all the positive numbers in the list")
    print("7 Get the whole number quotients after dividing each element by the same number")
    print("8 Get the signs of all the numbers in the list")
    print("9 Find the product of the negative numbers in the list")
    print("0 Show the list with odd numbers removed")


def GetMenuChoice():
    # Gets a menu choice from the user and returns it
    choice = input("Please enter a choice from the menu: ")
    print()
    return choice


def ExecuteChoice(c, numbers):
    # performs the operation specified by c on the list called numbers
    if c == "1":  # Display the current list of numbers
        ShowList(numbers)
    elif c == "2":  # Add numbers to the list
        ShowList(numbers)
        print("Add numbers to the list")
        numbers = AddNumsToList(numbers)
        ShowList(numbers)
    elif c == "3":  # Remove numbers from the list
        ShowList(numbers)
        print("Remove numbers from the list")
        numbers = RemoveNumsFromList(numbers)
        ShowList(numbers)
    elif c == "4":  # Clear the list of numbers
        numbers = []
        ShowList(numbers)
    elif c == "5":
        ShowList(numbers)
        result = NumberOfNegatives(numbers)
        print("Count of negative numbers is ", result)
        print()
    elif c == "6":
        ShowList(numbers)
        result = PositionsOfPos(numbers)
        print("Indexes of positive numbers are:")
        print(result)
        print()
    elif c == "7":
        divisor = int(input("Enter a whole number divisor: "))
        ShowList(numbers)
        result = Quotients(numbers, divisor)
        print("Whole number quotients are:")
        print(result)
        print()
    elif c == "8":
        ShowList(numbers)
        result = ListOfSigns(numbers)
        print("The signs of these numbers are:")
        print(result)
        print()
    elif c == "9":
        ShowList(numbers)
        result = ProductOfNegatives(numbers)
        if result == 0:
            print("No negative numbers in the list")
        else:
            print("The product of the negative numbers in the list is ", result)
        print()
    elif c == "0":
        ShowList(numbers)
        result = RemoveOddsFrom(numbers)
        print("The list with odd numbers removed is:")
        print(result)
        print()
    else:
        print("Option", c, "not on menu")
    return numbers


def AddNumsToList(numList):
    # gets numbers from the user and adds them to the list
    while True:
        numstr = input("Please type in a whole number, or q to quit: ")
        if numstr == 'q':
            break
        else:
            try:
                number = int(numstr)
            except:
                continue
        numList.append(number)
    return numList


def RemoveNumsFromList(numList):
    # gets numbers from the user and removes them from the list
    while True:
        numstr = input("Please type in a whole number, or q to quit: ")
        if numstr == 'q':
            break
        else:
            try:
                number = int(numstr)
            except:
                continue
        if number in numList:
            numList.remove(number)
            print(number, "removed")
        else:
            print(number, "was not in the list")
    return numList


def ShowList(numList):
    # shows a formatted version of numList on screen
    if numList == []:
        print("The list is empty")
    else:
        print("The current list of numbers is")
        print(numList)
    print()


############################################################################
##########################               ###################################
########################## End of Part 2 ###################################
##########################               ###################################
############################################################################


############################################################################
################                                        ####################
################ PART 3: FUNCTIONS FOR YOU TO IMPLEMENT ####################
################                                        ####################
################    DO NOT CHANGE THIS COMMENT BOX:     ####################
################ it must appear at the start of Part 3  ####################
################                                        ####################
############################################################################

############################################################################
#
#   Code from Part 3 will be marked
#
#   Do not change the 'def' line of any of the functions,
#   or your work may be marked incorrect
#
#   The pre-condition of each function tells you what data items the
#   function expects as parameters
#     * The function needs to work for any set of data items that makes
#       its pre-condition true
#     * Only data items that meet the pre-condition will be used
#       for testing, so your function does not need to check whether
#       the pre-condition has been met
#
#   The post-condition of each function specifies the relationship
#   between the function's parameters and its return value
#     * The function must return a value that makes the post-condition
#       true for any set of data items that makes the pre-condition true
#
#   You need to write code that implements each of the functions, and
#   test that they do what their specifications say they should
#
#   You are not allowed to use any external modules
#   in the solution of these problems (NO IMPORTS)
#
############################################################################

############################################################################
#
# IMPORTANT
# Insert your Student Registration Number (SRN) between the
# quotation marks in the assignment statement below:

SRN = ""


# For example, if your SRN is 7654321 the assignment statement
# should read  SRN = "7654321"
#
############################################################################


##########################
# Option 5 (3 marks)
##########################
def NumberOfNegatives(numList):
    # Pre-condition:
    #    theNums is a list of numbers
    # Post-condition:
    #    Returns the number of negative numbers in theNums
    # Examples:
    #    NumberOfNegatives ([1,2,-3,4,-5]) returns 2
    #    NumberOfNegatives ([4,18,0]) returns 0
    #    NumberOfNegatives ([-3,-5,-9,-17]) returns 4
    negative_count = 0
    for num in numList:
        if num < 0:
            negative_count += 1
    return negative_count  # Code stub: replace with function body


##########################
# Option 6 (3 marks)
##########################
def PositionsOfPos(numList):
    # Pre-condition:
    #    theNums is a list of numbers
    # Post-condition:
    #    Returns a list containing the positions of all of the
    #    positive numbers in theNums
    # Examples:
    #    PositionsOfPos ([1,2,-3,4,-5]) returns [0,1,3]
    #    PositionsOfPos ([4,7,18,0]) returns [0,1,2]
    #    PositionsOfPos ([0,-3,-5,-9,-17]) returns []
    lst = []
    for i, j in enumerate(numList):
        if j > 0:
            lst.append(i)
    return lst  # Code stub: replace with function body


##########################
# Option 7 (3 marks)
##########################
def Quotients(numList, d):
    # Pre-condition:
    #    theNums is a list of integers
    #    d is an integer
    # Post-condition:
    #    Returns a list containing the quotients obtained when
    #    using integer division to divide each of the numbers
    #    in theNums by d
    # Examples:
    #    Quotients ([3,4,6,8],3) = [1,1,2,2]
    #    Quotients ([1,7,2,9],4) = [0,1,0,2]
    #    Quotients ([-1,-3,8,7],6) = [0,0,1,1]
    #    Quotients ([-1,-3,8,7],-6) = [0,0,-2,-2]
    lst = []
    for i in numList:
        if i > d:
            a = i / d
            if i > 0:
                b = math.floor(a)
                lst.append(b)
            else:
                lst.append(int(a))
        elif i == d:
            lst.append(1)
        else:
            lst.append(0)
    return lst  # Code stub: replace with function body


##########################
# Option 8 (3 marks)
##########################
def ListOfSigns(numList):
    # Pre-condition:
    #    theNums is a list of numbers
    # Post-condition:
    #    Return value is a result list containing strings, each
    #    of which indicates the sign (positive, negative or zero)
    #    of the number at that position in theNums
    #    If the number in position i is positive, result[i] is 'pos'
    #    If the number in position i is negative, result[i] is 'neg'
    #    If the number in position i is zero, result[i] is 'zero'
    lst = []
    for i in numList:
        if i < 0:
            lst.append(f'{i} is neg')
        if i > 0:
            lst.append(f'{i} is pos')
        if i == 0:
            lst.append(f'{i} is zero')
    return lst  # Code stub: replace with function body


##########################
# Option 9 (4 marks)
##########################
def ProductOfNegatives(numList):
    # Pre-condition:
    #    theNums is a list of whole numbers
    # Post-condition:
    #    Return value is the product of just the negative numbers
    #    in theNums
    #    If theNums contains no negative numbers the function
    #    should return 0
    # Note: the product of two numbers a and b is a times b
    product = 1
    for number in numList:
        if number < 0:
            product *= number
        else:
            product = 0
    return product  # Code stub: replace with function body


##########################
# Option 0 (4 marks)
##########################
def RemoveOddsFrom(numList):
    # Pre-condition:
    #    theNums is a list of whole numbers
    # Post-condition:
    #    Return value is a list that contains just the even numbers
    #    that appear in theNums and no other numbers
    for number in numList:
        if number % 2 != 0:
            numList.remove(number)
    return numList  # Code stub: replace with function body


############################################################################
##########################               ###################################
########################## END OF PART 3 ###################################
##########################               ###################################
################                                        ####################
################    DO NOT CHANGE THIS COMMENT BOX:     ####################
################ it must appear at the end of Part 3    ####################
################                                        ####################
############################################################################

############################################################################
#
#   PART 4: Runs the program to test the functions you have implemented
#
#   You do not need to modify Part 4, but you may do so if you wish to
#
#   Any code you put in Part 4 will be removed before marking
#
############################################################################

Main()
