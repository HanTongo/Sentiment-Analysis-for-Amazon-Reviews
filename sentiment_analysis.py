import spacy
import pandas as pd
import random 
from spacytextblob import spacytextblob

# Loads up simple nlp model
nlp = spacy.load("en_core_web_sm")
nlp.add_pipe("spacytextblob")

# Loads the Amazon csv into a DataFrame 
df = pd.read_csv("1429_1.csv", sep=',')

# Removes missing values from column "reviews.text"
na_reviews_data = df.dropna(subset=["reviews.text"])

# Grabs row length of the Amazon DataFrame.
length_df = len(df)
numbers = random.sample(range(0,length_df),5)

# Randomly selected reviews
rnd_selected_reviews_data = na_reviews_data["reviews.text"].iloc[numbers]

def to_clean(reviews):
    # Sets up list to return clean reviews
    clean_reviews_list = []
    for review in reviews:
        doc = nlp(review)

        # For each word in the review: keep if not a stopword, and make lowercase and remove whitespace
        filtered_tokens = [token.text.lower() for token in doc if not token.is_stop and token.text.strip()]

        # Combine all words into a sentence. Then put sentences in a list
        clean_words = ' '.join(filtered_tokens)
        clean_reviews_list.append(clean_words)
    return clean_reviews_list

def sentiment_analysis(reviews):
    # Sets up list to return sentiment scores reviews
    sentiment_list = []
    for review in reviews:
        doc = nlp(review)

        # Finds how positive or negative the comment is.
        polarity = doc._.blob.polarity
        sentiment_list.append(polarity)

    return sentiment_list

def menu_options_display():
    print("[1] Random")
    print("[2] Clean + Sentiment Analysis Random Amazon data.")
    print("[3] To Input User's Review")
    print("[4] Clean + Sentiment Analysis of User Review ")

print("Amazon review data loaded.")
menu_options_display() 

user_choice = input("Please enter your option [1-4, 0 to exit]: ")

# Loop to send the user to the desired service
# If there is an incorrect input, direct the user to retry.
while user_choice != "0":

    if user_choice == "1":
                
        # Grabs row length of the Amazon DataFrame.
        # Uses random to select 5 numbers from the number of reviews in the Amazon DataFrame
        length_df = len(df)
        numbers = random.sample(range(0,length_df),5)

        # Randomly selected reviews
        rnd_selected_reviews_data = na_reviews_data["reviews.text"].iloc[numbers]

    if user_choice == "2":

        # Cleans and analyses the Amazon reviews
        clean_amazon = to_clean(rnd_selected_reviews_data)
        sentiment_amazon = sentiment_analysis(clean_amazon)

        # Presents the reviews and their sentiment scores
        for x in range(0,5):
            print(f"\nReview {x+1}: {rnd_selected_reviews_data.iloc[x]}\nSentiment score: {sentiment_amazon[x]:.3f}")

    elif user_choice == "3": 

        user_input = input("\nPlease enter a review: ")
        
        # Puts user input into a dataframe structure to run through the clean and analysis functions.
        df = pd.DataFrame({"reviews.text": [user_input]})
        input("Review inputted. Please press [ENTER] to return to the menu.")
        
    elif user_choice == "4":

        # Puts the user dataframe through the cleaning and sentiment analysis functions.
        clean_amazon = to_clean(df["reviews.text"])
        sentiment_amazon = sentiment_analysis(clean_amazon)

        # Displays a formatted result of the functions
        print(f"\nUser Review: {user_input}\nSentiment score: {sentiment_amazon[0]:.3f}")
        
    else:
        print("Invalid option. Please try again.")

    print()
    menu_options_display()
    user_choice = input("Please enter your option [1-4, 0 to exit]: ")

print("\nThank you for using the program. Hope to see you again.")
input("[Press ENTER to exit]")


