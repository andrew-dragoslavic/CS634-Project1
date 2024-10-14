from itertools import combinations
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder

def get_valid_input(string, min, max):
    while True:
        try:
            value = int(input(string))
            if min <= value <= max:
                return value
            else:
                print(f"Please enter a number between {min} and {max}.")
        except ValueError:
            print("Invalid Input. Please enter a valid integer.")

def get_valid_choice():
    while True:
        choice = input('Please Choose a Number\n1. Amazon\n2. Shop Rite\n3. Apple\n4. Best Buy\n5. Nike\n')
        if choice in ('1', '2', '3', '4', '5'):
            return choice
        else:
            print("Invalid choice. Please enter a number 1 through 5.")

print('Welcome to Apriori 2.0!')
num = get_valid_choice()
support = get_valid_input('Please Enter and Number Between 1 and 100 for Support: ', 1, 100)
confidence = get_valid_input('Please Enter a Number Between 1 and 100 for Confidence: ', 1, 100)

transactions = pd.read_csv(f'{num}/Transactions.csv')
itemset = pd.read_csv(f'{num}/Items.csv')

itemsList = []
for index, row in transactions.iterrows():
    itemSet = [item.strip() for item in row['Transaction'].split(',')]
    itemsList.append(itemSet)

def convertToSet(transactions):
    return set(item.strip() for item in transactions.split(","))


transactions["Transaction"] = transactions["Transaction"].apply(convertToSet)
threshold = (support / 100) * len(transactions)

# Get a dictionary of all the items from the csv file
# Go through the transactions and get a count of how many of each item there is


def generateItemsets(prevItemsets, transactions, threshold, k):
    itemsets = {}
    itemList = list(prevItemsets.keys())

    for combo in combinations(itemList, k):
        combo = set(combo)
        count = sum(
            1
            for transaction in transactions["Transaction"]
            if combo.issubset(transaction)
        )
        if count >= threshold:
            itemsets[tuple(combo)] = count
    return itemsets


def generateRules(itemsets, transactions, min_support, min_confidence):
    count = 0
    # Go through the final dictionary and if the length is only one item ignore it
    # If the length is more than two generate all the possible combinations
    for itemset in itemsets.keys():
        k = len(itemset)
        if k < 2:
            continue
        for i in range(1, k):
            for combo in combinations(itemset, i):
                start = set(combo)
                itemset = set(itemset)
                res = itemset - start
                start_support = sum(
                    1
                    for transaction in transactions["Transaction"]
                    if start.issubset(transaction)
                )
                rule_support = sum(
                    1
                    for transaction in transactions["Transaction"]
                    if itemset.issubset(transaction)
                )
                confidence = rule_support / start_support
                if confidence >= min_confidence / 100:
                    count += 1
                    print(
                        f"\nRule {count}: {', '.join(start)} -> {', '.join(res)} \nConfidence: {round((confidence * 100),2)}% \nSupport: {round(((rule_support/len(transactions))*100),2)}%"
                    )


def generateFrequentItems(itemsets):
    freq = []
    freqString = """\nFrequent Items: """
    for itemset in itemsets:
        freq.append(itemset)
    for i in range(len(freq)):
        freqString += "{" + ", ".join(freq[i]) + "}"
        if i < len(freq) - 1:
            freqString += ", "
    return freqString


def aprioriBrute(transactions, min_support, min_confidence):
    itemsets = {}
    results = {}

    for index, row in transactions.iterrows():
        for item in row["Transaction"]:
            itemsets[item] = itemsets.get(item, 0) + 1

    threshold = (min_support / 100) * len(transactions)
    itemsets = {k: v for k, v in itemsets.items() if v >= threshold}

    k = 1

    while True:
        new = generateItemsets(itemsets, transactions, threshold, k)
        if not new:
            break
        results.update(new)
        k += 1
    generateRules(results, transactions, min_support, min_confidence)

    return results

results = aprioriBrute(transactions, support, confidence)
print(generateFrequentItems(results))

encoder = TransactionEncoder()
onehot = encoder.fit(itemsList).transform(itemsList)
df = pd.DataFrame(onehot, columns = encoder.columns_)

aprioriItemsets = apriori(df, min_support=support/100, use_colnames=True)
# Generate the association rules
if not aprioriItemsets.empty:
    aprioriRules = association_rules(aprioriItemsets, metric="confidence", min_threshold=confidence/100)
    for index, row in aprioriRules.iterrows():
        antecedent_str = row['antecedents']
        consequent_str = row['consequents']
        confidence_str = row['confidence']
        
        print(f"Rule {index + 1}: [{antecedent_str}, {consequent_str}, {confidence_str}]\n")
else:
    print("No frequent itemsets found.")



