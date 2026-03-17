'''
This program is designed to evaluate and improve password security. It analyzes any user-given password based 
length and character diversity, assigns a strength score, and provides suggestions on how the password can be improved.
The program also includes a password generator that creates secure random passwords and allows the user to save them to a 
file. Additionally, it features a mode for checking previously saved passwords by reading them from a text file 
and analyzing them automatically.
'''

import random, string

#main Menu loop
def main_loop():
    
    #Displays the main menu and repeatedly prompt user until a valid option is selected.
    #This function returns the chosen option.
    
    while True:
        #OPT for user input
        print("Enter 1  for Password Analyzer\n")
        print("Enter 2 for New Password Generator\n")
        print("Enter 3 for Old Password Checker\n")
    
        try: 
            user_selection = int(input("Please Enter a Number between 1-3: "))
            print()
            if user_selection in [1,2,3]:
                return user_selection
            else:
                print("Please Enter a Number between 1-3\n")
        except ValueError:
            print("Please enter a valid number between 1-3\n")
            

def pts(pwd):
    
    #Calculate the password strength score based on several criterias 
    #Each criteria contributes a fixed number of points, and the total points determine the strength
    #Scoring factors
    # - Length of password (10-15 points)
    # - Uppercase letters (10 points)
    # - Lowercase letters (10 points)
    # - Digits (10 points)
    # - Special characters (10 points)
    #This function returns the total points as an integer
    
    
    len_score = 0 
    upper_case_score = 0
    lower_case_score = 0
    digit_score = 0
    symbol_score = 0 
    
    
    length = len(pwd)
    
    #Determine length score: longer passwords score more points
    
    if length >= 10:
        len_score += 15
        
    elif length >= 8:
        len_score += 10
        
    elif length < 8: #Length shorter thann 8 characters immediately score 0
        len_score = 0
    
    # any() is used to detect if the password contains at least one character
    if any(ch.isupper() for ch in pwd):
        upper_case_score += 10
    if any(ch.islower() for ch in pwd):
        lower_case_score += 10
    if any(ch.isdigit() for ch in pwd):
        digit_score += 10
    if any(ch in "!@#$%^&*?" for ch in pwd):
        symbol_score += 10
   
    #total score
    final_score = len_score + upper_case_score + lower_case_score + digit_score + symbol_score
    
    return final_score



def analyzer(score):
    #Convert the numeric score into a strength message
    #Thressholds:
    # - 55 or above = strong 
    # - 36 to 54 = moderate 
    # - 35 or below = weak 
    #This function returns the corresponding message string
    
    
    if score >= 55:
        return "You have a strong password"
    elif score > 35 and score < 55:
        return "You have moderate strength password"
    else:
        return "You have weak password"
    
def suggestions(pwd):
    
    #Generate suggestions based on which password requirements are missing.
    #Each missing requirement adds one suggestion to a list
    #This function is only used for user feedback
    
    suggestions_list = []
    
    # length check
    if len(pwd) < 8:
        suggestions_list.append("Use at least 8 characters.")
    
    # uppercase check
    if not any(ch.isupper() for ch in pwd):
        suggestions_list.append("Add at least one uppercase letter.")
    
    # lowercase check
    if not any(ch.islower() for ch in pwd):
        suggestions_list.append("Add at least one lowercase letter.")
    
    # digit check
    if not any(ch.isdigit() for ch in pwd):
        suggestions_list.append("Add at least one digit.")
    
    # symbol check
    if not any(ch in '!@#$%^&*?' for ch in pwd):
        suggestions_list.append("Add at least one special symbol (!@#$%^&*?).")

    return suggestions_list

def gen(length):
    #Generate a random password of user defineed length 
    #Gen password includes uppercase, lowercase, digits and special characters
    #random.choice() selects one character at a time from the character pool
    #The resulting string is returned
    
    characters = string.ascii_letters + string.digits + '!@#$%^&*?' #character pool
    
    while True: 
        gen_pass = ''
        
        #loop through pool and pick one character at random
        for i in range(length):
            gen_pass += random.choice(characters)
        
        #check if it hits all requirements
        if (any(ch.isupper() for ch in gen_pass) and 
            any(ch.isupper() for ch in gen_pass) and 
             any(ch.isdigit() for ch in gen_pass) and 
             any(ch in '!@#$%^&*?' for ch in gen_pass)):
            
            #only return if it statisfies all conditions
             
            return gen_pass
        
        #otherwise, loop again 

    
def main():
    #The main program loop controls overall program files
    #It repeatedly displays the menu, executes the selected mode
    #Exits when the user chooses to
    
    
    print("Welcome user to PassWord\n")

    while True:  # MAIN PROGRAM LOOP
        choice = main_loop()
        
        #Analyze the password: compute score, determine strength, and display suggestions
        #Does not write to file
        
        if choice == 1:
            if choice == 1: 
                print("Howdy user, youre in password analyzer mode\n")
                
                pwd = input("Enter your password: ")
                

                #score gets saved 
                score = pts(pwd)
                #analyzer returns a msg 
                message = analyzer(score)
                print(f"\nPassword score: {score}")
                print(message)
                suggestions_list = suggestions(pwd)

                if suggestions_list:
                    print("\nSuggestions to improve your password:")
                    for s in suggestions_list:
                        print("- " + s)
                else:
                    print("Your password meets all recommended requirements!")
                    
       #Ask the user for length. Enforce a minimum length of 8
       #After generating the password, allow the user to save it to a text file for later use.
       
        elif choice == 2:
            print("Howdy user, youre in genrator mode\n")
            while True:
                try: 
                    length = int(input("Please enter the length you want your password to be: "))
                    if length < 8: 
                        print("Password length must be at least 8 characters long.")
                        continue #ask again
                    break # valid length, exist loop
                except ValueError:
                    print("Enter only numbers")
                    
            message_gen_pass = gen(length)
            print(f'Your generated password is: {message_gen_pass}')
            
            while True:
                option = input("Do you want to save the password? (y/n): ")
                if option.lower() == "y":
                    with open("password_saved.txt", "a") as f:
                        f.write(f"{message_gen_pass}\n")
                        print("\nYour password has been saved")
                        break
                    
                elif option.lower() == "n":
                    break
                else:
                    print("Please enter y/n only")
                    continue
        
        #Read previously stroed passwords line by line from a text file
        #For each passwprd, compute its score and display the corresponding strength category

        else:
            print("Howdy user, youre in old password checker mode")
            
            with open("password_list.txt", "r") as f :
                for line in f:
                    old_pass = line.strip()
                    score = pts(old_pass)
                    result = analyzer(score)
                    print(f" {old_pass} : {result}")
                    
                    suggestions_list = suggestions(old_pass)

                    if suggestions_list:
                        print("\nSuggestions to improve your password:")
                        for s in suggestions_list:
                            print("- " + s)
                    else:
                        print("Your password meets all recommended requirements!")

        # ask user if they want to repeat menu
        while True:
           
            again = input("\nReturn to main menu? (y/n): ").lower()
            if again in ("y", "n"):
                break
            else: 
                print("Only (y/n)")
                
        if again == "n":
            print("Goodbye")
            break

main()    