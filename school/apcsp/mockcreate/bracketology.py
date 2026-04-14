import os
os.system('clear')
# Data for the program
set1 = ["Noun", "Adjective", "Verb", "Place", "Exclamation"]
set2 = ["Adjective", "Noun", "Verb", "Adverb", "Food", "Color", "Animal", "Noun", "Adjective", "Noun"]
set3 = ["Noun", "Food", "Plural Noun", "Plural Noun", "Plural Noun", "Adjective", "Nonsense Word", "Adjective", "Noun", "Plural Noun", "Part Of Body", "Person", "Animal", "Plural Noun", "Body Part", "Plural Noun", "Adverb", "Plural Noun", "Noun", "Verb", "Adjective", "Place", "Color", "Noun", "Adjective", "Animal", "Verb", "Number", "Noun", "Noun"]

phrases = [
    "The #1 was #2. #3 at #4? #5!",
    "A #1 #2 decided to #3 #4. It ate #5 and saw a #6 #7. What a #8 #9 #10!",
    "During the #1, people threw #2. The #3 hit #4 and #5. It was #6! I shouted #7. A #8 #9 saw #10. My #11 felt #12. The #13 escaped #14. My #15 had #16. We ran #17 toward #18. The #19 began to #20. It was #21 at #22. A #23 #24 looked #25. That #26 started to #27. We saw #28 #29 by the #30."
]

sets = [set1, set2, set3]

# Finds out how long of a phrase the user wants
print("Welcome to Mad Libs!")
choice = int(input(f"""
Pick a set:
1 - Short | {len(set1)} Words
2 - Medium | {len(set2)} Words
3 - Long | {len(set3)} Words
Selected Set: """))

# Makes sure the user picks a valid option
if not 1 <= choice <= 3:
    os.system('clear')
    print("Invalid choice!\n")
    exit()

# Passes through the user-selected list and loops through each word to ask the user
def fill_words(selected_list):
    user_set = []
    for word_type in selected_list:
        user_word = input(f"Enter a {word_type}: ")
        
        if len(user_word) < 1:
            print("You did not enter a word. Defaulting to empty_space.")
            user_word = "empty_space"
            
        user_set.append(user_word)
    return user_set

# Configures the correct set of words
selected_index = choice - 1
new_words = fill_words(sets[selected_index])
story = phrases[selected_index]

# Inserts each word into the phrase. 
# This must go backwards as to avoid double digit numbers to be identified as single digit.
# Example: #13 being identified as #1 + 3
for i in range(len(new_words), 0, -1):
    placeholder = f"#{i}"
    story = story.replace(placeholder, new_words[i-1])

os.system('clear')
print("FINAL STORY:")
print(f"{story}\n")