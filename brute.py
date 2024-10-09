from itertools import combinations
import pandas as pd


transactions = pd.read_csv("Amazon Transactions.csv")
def convertToSet(transactions):
    return set(transactions.split(", "))
transactions['Transaction'] = transactions['Transaction'].apply(convertToSet)
itemset = pd.read_csv("Amazon Items.csv")
support = 45
confidence = 70
threshold = (support / 100) * len(transactions)

# Get a dictionary of all the items from the csv file
# Go through the transactions and get a count of how many of each item there is

def generateItemsets(prevItemsets, transactions, threshold, k):
    itemsets = {}
    itemList = list(prevItemsets.keys())

    for combo in combinations(itemList, k):
        combo = set(combo)
        count = sum(1 for transaction in transactions['Transaction'] if combo.issubset(transaction))
        if count >= threshold:
            itemsets[tuple(combo)] = count
    return itemsets

def generateRules(itemsets, transactions, min_support, min_confidence):
    # Go through the final dictionary and if the length is only one item ignore it
    # If the length is more than two generate all the possible combinations
    for itemset in itemsets.keys():
        k = len(itemset)
        if k < 2:
            continue
        for i in range(1,k):
            for combo in combinations(itemset, i):
                start = set(combo)
                itemset = set(itemset)
                res = itemset - start
                start_support = sum(1 for transaction in transactions['Transaction'] if start.issubset(transaction))
                rule_support = sum(1 for transaction in transactions['Transaction'] if itemset.issubset(transaction))
                confidence = rule_support / start_support
                if confidence >= min_confidence/100:
                    print(f"\nRule: {', '.join(start)} -> {', '.join(res)}, Confidence: {confidence}")

def generateFrequentItems(itemsets):
    freq = []
    freqString = '''\nFrequent Items: '''
    for itemset in itemsets:
        freq.append(itemset)
    for i in range(len(freq)):
        freqString += "{" + ", ".join(freq[i]) + "}"
        if i < len(freq) - 1:
            freqString += ", "
    return freqString

def apriori(transactions, min_support, min_confidence):
    itemsets = {}
    results = {}

    for index, row in transactions.iterrows():
        for item in row['Transaction']:
            itemsets[item] = itemsets.get(item, 0) + 1

    threshold = (min_support / 100) * len(transactions)
    itemsets = {k:v for k, v in itemsets.items() if v >= threshold}
    # results.update(itemsets)
    k = 1
    
    while True:
        new  = generateItemsets(itemsets, transactions, threshold, k)
        if not new:
            break
        results.update(new)
        k += 1
    generateRules(results, transactions, min_support, min_confidence)

    return results


results = apriori(transactions, 45, 90)
# print(results)
print(generateFrequentItems(results))







# def generateFreqItems(dict):
#     freqItems = []
#     result = """\nFrequent Itemset: """
#     for k, v in dict.items():
#         items = k.strip("()").split(", ")
#         if len(items) > 1:
#             items = [item.strip("'") for item in items]
#             freqItems.append(items)
#         else:
#             freqItems.append(items)
#     for i in range(len(freqItems)):
#         result += "{" + ", ".join(freqItems[i]) + "}"
#         if i < len(freqItems) - 1:
#             result += ", "
#     print(result)