import json
import requests
import syllables
import sys
import textblob
import nltk
nltk.download("punkt")
nltk.download('averaged_perceptron_tagger')


# This function has been used again from my old assignments.
def correct_spelling(word):
    """
    Function to the correct the spelling of the input word using TextBlob.correct()

    Parameters
    ------------
        word: str
            Input word that needs to be corrected

    Returns
    ------------
    blob.correct(): str
        Corrected word by spelling for the input word

    """
    blob = textblob.TextBlob(word)
    return blob.correct()


# This function has been used again from my old assignments.
def seek_response():
    """
    Function to Seek response from user whether to run any further analysis or not

    Parameters
    ----------------
        -

    Returns
    ----------------
    analyzer()
        If user response is yes

    None
        Ends program if user response is no

    seek_response()
        neither yes nor no, then seeks response from user again

    """
    # seeking response from user. validates case and whitespaces.
    get_response = input("\nWould you like to run any another analysis (yes/no)?\n"
                         "Your response will be spell corrected ").lower().strip()

    # Corrects input from user using textblob correct
    response_from_user = correct_spelling(get_response)

    # If user response is yes, executes analysis function
    if response_from_user == "yes":
        return analyzer()

    # If user response is no, ends the entire program
    elif response_from_user == "no":
        return

    # If user is response is not among yes or no, seeks user response again to proceed.
    else:
        print("\nInvalid Input. Enter only yes or no.")
        return seek_response()


def formality(tweets):
    """
    Function to calculate average formality index across all tweets in input tweet list

    Parameters
    ----------------
        tweets
            List of tweets

    Returns
    ----------------
    avg formal
        Average formality Index value

    """
    # Initiating formality index as 0
    formal = 0

    # for each tweet in the tweets list
    for tweet in tweets:
        blob = textblob.TextBlob(tweet)
        f = 0
        c = 0

        # List for f and c with tags
        f_lst = ["NN", "JJ", "IN", "DT"]
        c_lst = ["PR", "VB", "RB", "UH"]

        # for each tag, if it contains in f_lst, increments f by 1
        # if in c_lst, increments c by 1
        for word, tag in blob.tags:
            for i in f_lst:
                if i in tag:
                    f += 1
            for j in c_lst:
                if j in tag:
                    c += 1
        # Add formality index for each tweet to the previous sum
        formal += 50*(((f-c)/(f+c))+1)

    # Calculate average formality index
    avg_formal = formal/len(tweets)

    return avg_formal


def fkgl(tweets):
    """
    Function to calculate Flesch-Kincaid Grade Level (FKGL) across all tweets in input tweet list

    Parameters
    ----------------
        tweets
            List of tweets

    Returns
    ----------------
    avg fkgl
        Average Flesch-Kincaid Grade Level (FKGL)

    """
    fkgl_sum = 0
    sent = 0
    syl = 0
    nword = 0

    # for each tweet in the tweets list
    for tweet in tweets:
        blob = textblob.TextBlob(tweet)

        # Increment no of sentences
        sent += len(blob.sentences)

        # for every word in sentence
        for word in blob.words:
            # Increment nword by 1
            nword += 1

            # Increment syllables by no of syllables
            syl += syllables.estimate(word)

        # Calculate fkgl for each tweet and sum to previous sum
        fkgl_sum += ((0.39*(nword/sent) + 11.8*(syl/nword))-15.59)

    # Average fkgl for all tweets in the tweet list
    avg_fkgl = fkgl_sum/len(tweets)

    return avg_fkgl


def analyzer():

    # Get type of analysis
    get_type = input("\nWhich analysis would you like to perform\n"
                     "(polarity/subjectivity/formality/FKGL)? ").lower().strip()

    # Gets the response from the api
    response = requests.get("https://dgoldberg.sdsu.edu/515/customer_service_tweets_full.json")

    # If response, check connection status
    if response:
        data = json.loads(response.text)
        tweets_polarity = 0
        tweets_subjectivity = 0
        counts = 0
        tweets_lst = []
        company_lst = []

        # Get the twitter to analyze
        get_handle = input("\nWhich Twitter handle would you like to analyze? ").lower().strip()

        # for every line in the json data
        for line in data:
            company = line["Company"].lower()
            tweet = line["Text"]

            # Creates uniques list of Companies available in  data
            if company not in company_lst:
                company_lst.append(company)

            # Checks if company from each line in json data is equal to user input
            if company == get_handle:

                # Appends to the tweets list and increments the count by 1
                tweets_lst.append(tweet)
                counts += 1

                # Calculates the polarity and subjectivity
                tweets_polarity += textblob.TextBlob(tweet).polarity
                tweets_subjectivity += textblob.TextBlob(tweet).subjectivity

        # Handles company handle input if not available in the uniques from json data
        if get_handle in company_lst:

            # Prints polarity if type is polarity
            if get_type == "polarity":
                avg_polarity = tweets_polarity / counts
                print(f"{get_handle}: ", avg_polarity)

            # Prints subjectivity
            elif get_type == "subjectivity":
                avg_subjectivity = tweets_subjectivity / counts
                print(f"{get_handle}: ",avg_subjectivity)

            # Prints Formality Index
            elif get_type == "formality":
                print(f"{get_handle}: ", formality(tweets_lst))

            # prints fkgl
            elif get_type == "fkgl":
                print(f"{get_handle}: ", fkgl(tweets_lst))

            else:
                print("Incorrect Analysis Type Chosen")

        else:
            print(f"Twitter handle({get_handle}) data not available")

        return seek_response()

    else:
        print("Connection Error!")
        return


def main():
    print("Welcome to the customer service analyzer!")
    analyzer()

    return


if __name__ == "__main__":
    sys.exit(main())
