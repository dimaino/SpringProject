from __future__ import unicode_literals
from django.contrib import messages
from django.db import models
from datetime import date
import datetime
import bcrypt
import re

# Matches the email to make sure the format is atleast one letter (lower or uppercase),
# number, or of of there characters . + _ -  Then an @ sign with the same format and
# lastly make sure there is a . followed by the same pattern.
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# The password is any characters and there are atleast 7.
PASSWORD_REGEX = re.compile(r'^.{7,}$')

# The username checks for numbers and letters that can contain _ or . just not next to
# eachother, plus there has to be 5 through 18 characters.
USERNAME_REGEX = re.compile(r'^[a-zA-Z0-9]([._](?![._])|[a-zA-Z0-9]){5,18}[a-zA-Z0-9]$')

# The date just checks for a year with 4 numbers a month with 2 numbers and a day with 2
# numbers.
DATE_REGEX = re.compile(r'^[0-9]{4}-[0-9]{2}-[0-9]{2}$')

class UserManager(models.Manager):
    # Call this function to check for validation of all field for registation.
    # How to call: Table.userManager.registration(request.POST)
    def registration(self, userInput):
        # errorList - Keeps tracks of all errors with the validation.
        errorList = []
        age = None

        # Checks to see if first_name is greater than 2 characters.
        if len(userInput['first_name']) < 2:
            errorList.append('First name needs to be greater than 2 letters!\n')

        # Checks to see if last_name is greater than 2 characters.
        if len(userInput['last_name']) < 2:
            errorList.append('Last name needs to be greater than 2 letters!\n')

        # Checks to see if first_name contains only alphabetical letters.
        if not userInput['first_name'].isalpha():
            errorList.append('First name may only contain letters!\n')

        # Checks to see if last_name contains only alphabetical letters.
        if not userInput['last_name'].isalpha():
            errorList.append('Last name may only contain letters!\n')

        # Checks if the username matches the USERNAME_REGEX.
        if not USERNAME_REGEX.match(userInput['username']):
            errorList.append('Username does not match the required conventions. Only alphabetical and numerical characters plus _ and . are accepted but not ._ or ._ !!!\n')

        # Checks if the date of birth matches the DATE_REGEX.
        if not DATE_REGEX.match(userInput['dob']):
            errorList.append('Incorrect format please re-enter the values with the date picker!\n')
        age = datetime.datetime.strptime(userInput['dob'], "%Y-%m-%d")
        # Try to get the date if it exists otherwise go to the exception.
        try:

            #print 'age', age
            print "_*"*5000
            #oldEnough = datetime.datetime(now(), "%Y-%m-%d") - age
            #print 'how old', oldEnough
            # Checks if user is old enough to signup.
            # if not oldEnough >= 14:
            #     errorList.append('Sorry you are not currently old enough to signup with our service!\n')
        except Exception as e:
            # Checks to see if the Date of Birth is the proper regex just doesn't exist.
            if DATE_REGEX.match(userInput['dob']):
                errorList.append("Not an actual date for Date of Birth!\n")
        print age

        # Checks if the email matches the EMAIL_REGEX.
        if not EMAIL_REGEX.match(userInput['email']):
            errorList.append('Email is not a valid email! Try this format: something@example.com\n')

        # Checks if the password matches the PASSWORD_REGEX.
        if not PASSWORD_REGEX.match(userInput['password']):
            errorList.append('Password is not long enough.\n')

        # Checks to make sure the password inputs match.
        if userInput['password'] != userInput['confirm_password']:
            errorList.append('Password match not confirmed.\n')

        # Checks the database to see if the username already exists.
        if self.filter(username = userInput['username']):
            errorList.append('This username already exists in our database.\n')

        # Checks the database to see if the email already exists.
        if self.filter(email = userInput['email']):
            errorList.append('This email already exists in our database.\n')

        # If the list has no errors.
        if not errorList:
            hashed = bcrypt.hashpw(userInput['password'].encode(), bcrypt.gensalt())
            current_user = self.create(first_name = userInput['first_name'], last_name = userInput['last_name'], username=userInput['username'], date_of_birth=userInput['dob'], email = userInput['email'], password = hashed)
            return True, current_user
        return False, errorList

    # Call this function to check for validation of all field for login.
    # How to call: Table.userManager.login(request.POST)
    def login(self, userInput):
        # errorList - Keeps tracks of all errors with the validation.
        errorList = []

        # Checks if the username and password don't match.
        if not userInput['username'] and not userInput['password']:
            errorList.append('Unsuccessful login. Please fill in the username and password field!\n')
            return False, errorList

        # Checks if the username is in the database.
        if self.filter(username = userInput['username']):
            hashed = self.get(username = userInput['username']).password.encode()
            password = userInput['password'].encode()

            # Checks if the password is the correct one to the hashed one.
            if bcrypt.hashpw(password, hashed) == hashed:
                return True, self.get(username=userInput['username'])
            else:
                errorList.append('Unsuccessful login. Incorrect password!\n')
        else:
            errorList.append('Unsuccessful login. Your email is incorrect!\n')
        return False, errorList


class User(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    username = models.CharField(max_length=200)
    date_of_birth = models.CharField(max_length=200)
    email = models.EmailField()
    password = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    userManager = UserManager()
