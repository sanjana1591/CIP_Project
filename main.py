import json
import time
import constants

def main():
    """
    Start by displaying a welcome message. Ask for the username, display questions to get answers, compute the score and 
    display analysis. Display a thank you message at the end and add the user data to a json file.
    """
    welcome_message()
    username = ask_user_name()
    answers = get_answers(username)
    category_scores, analysis_codes = compute_score(answers)
    display_analysis(username, analysis_codes)
    thank_you_message()
    add_data_to_file(username, category_scores) 

def welcome_message():
    """
    Display a welcome message introducing the OCEAN personality test. Informing user of the number of questions and how to
    answer them. 
    """
    print("******* OCEAN PERSONALITY TEST *******")
    print("This is a personality test based on the widely used OCEAN model")
    print("We will ask you 10 questions")
    print("Each question can be answered from 1 (Strongly Disagree) to 5 (Strongly Agree)")
    print("********************************************************************************")

def ask_user_name():
    """
    Ask user to enter their name. Return the input value.
    """
    print("")
    username = input("Please enter your name: ")
    print("")
    return username

def get_answers(username):
    """
    Questions are displayed one by one and the answers recorded in a list which is then returned.
    """
    answers = []
    print(username + " the questions will now begin...")
    time.sleep(2)
    for i in range(len(constants.questions)):
        print("")
        print("Question", i+1)
        answers.append(ask_question(constants.questions[i]))
    return answers

def ask_question(question):
    """
    Answer is returned after getting a valid answer for the question.
    """
    answer = get_valid_answer(question)
    return answer

def get_valid_answer(question):
    """
    User is prompted to enter an answer after displaying the question. A check is performed against the user input if its a
    valid number between 1 and 5. If the input is not valid, user is asked to enter the answer again. The valid answer is returned.
    """
    answer = input(question)
    while True:
        if not answer.isnumeric():
            answer = input("Please enter a number: ")
        else:
            answer = int(answer)
            if answer < 1 or answer > 5:
                answer =  input("Please enter a number between 1 and 5: ")
            else:
                return answer

def compute_score(answers):
    """
    Start by calculating category scores with the answers and get the analysis codes with the calculated category 
    scores. Both category scores and analysis codes are returned back.
    """
    category_scores = get_category_scores(answers)
    analysis_codes = get_analysis_codes(category_scores) 
    return category_scores, analysis_codes  

def get_category_scores(answers):
    """
    Some scores are taken as is and some need to be reversed. This information is stored in a reverse list. Start by 
    reversing scores for answers that need to be reversed, according to the reverse list and then categorise scores 
    to the five personality categories. Return the category scores.
    """
    scores = reverse_scores(answers)
    category_scores = categorise_scores(scores)
    return category_scores

def reverse_scores(answers):
    """
    For each answer, a check is performed whether its score needs to be reversed or not. If yes, the score is reversed,
    if not, the score remains the same as the answer. Scores is returned from here.
    """
    scores = []
    for i in range(len(answers)):
        if constants.reverse_answers[i] == 'Y':
            scores.append(-(answers[i]-6))
        else:
            scores.append(answers[i])
    return scores

def categorise_scores(scores):
    """
    Category score is calculated from the scores list. Against each category in the category list, the score is summed up and
    stored in the category scores dict, which is returned.
    """
    category_scores = {}
    for i in range(len(scores)):
        if constants.category_code[i] in category_scores:
            category_scores[constants.category_code[i]] += scores[i]
        else:
            category_scores[constants.category_code[i]] = scores[i]
    return category_scores

            
def get_analysis_codes(category_scores):
    """
    Analysis is a dictionary with mapping of analysis codes to analysis that will be displayed to the user. Analysis codes are
    calculated based on the category scores. If, for a particular category, the score is < 2.5, 'L', signifying low, is appended 
    to the category code. Similarly, 'M' for medium and 'H' for high is appended to get the analysis code. For eg, if for the 
    category 'E' (extraversion), the score is > 3.5, 'H' will be added to the category code. So the analysis code will be 'EH'.
    """
    analysis_codes = []
    for key in category_scores:
        if category_scores[key] < 2.5:
            analysis_codes.append(key + 'L')
        elif category_scores[key] < 3.5:
            analysis_codes.append(key + 'M')
        else: 
            analysis_codes.append(key + 'H')
    return analysis_codes

def display_analysis(username, analysis_codes):
    """
    Congratulate the user on completing the questionnnare, added a sleep duration to give a feeling of analysis being generated. 
    The personality analysis is then printed as per the analysis code.
    """
    print("")
    print("***************************************")
    print("Awesome! You answered all questions " + ("\U0001f600"))
    print("Analysing personality according to the OCEAN model...")
    time.sleep(2)
    print("")
    print("\033[1m" + username + "'s Personality Analysis:"+ "\033[0m")
    print("")
    print_analysis(analysis_codes)

def print_analysis(analysis_codes):
    """
    For each code, in analysis codes list, the corresponding analysis is pulled from the analysis dictionary and printed out.
    """
    analysis = constants.analysis
    for code in analysis_codes:
        print("\033[4m" + constants.category_descriptions[(code[0])] + "\033[0m" + ": ")
        print(analysis[code])

def thank_you_message():
    """
    A lag is added for the user to be able to read the results of the analysis. And a thank you message is then printed.
    """
    print("")
    time.sleep(4)
    print("Thank you for taking this test " + ("\U0001F642"))
    print("***************************************")
    
def add_data_to_file(username, category_scores):
    """
    Add the username with category scores to a json file.
    """
    data_to_add = {
        'username': username, 
        'scores': category_scores
        }
    try:
        with open("data.json", 'r') as f:
            existing_data = json.load(f)
    except FileNotFoundError:
        existing_data = []

    existing_data.append(data_to_add)

    with open("data.json", "w") as f:
        json.dump(existing_data, f, indent=4)

if __name__ == "__main__":
    main()