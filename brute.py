from itertools import combinations
import pandas as pd


transactions = pd.read_csv("Amazon Transactions.csv")
itemset = pd.read_csv("Amazon Items.csv")
support = 45
confidence = 70
threshold = (support / 100) * len(transactions)

# Get a dictionary of all the items from the csv file
# Go through the transactions and get a count of how many of each item there is


def generateDict(itemset):
    k, itemDict = 1, {}
    while k <= 2:
        itemList = []
        for index, row in itemset.iterrows():
            itemList.append(row["Item Name"])
        if k == 1:
            for item in itemList:
                itemDict[item] = 0
        else:
            for combo in combinations(itemList, k):
                itemDict[str(combo)] = 0
        k += 1
    return itemDict


itemsetDict = generateDict(itemset)

for index, row in transactions.iterrows():
    k = 1
    while k <= 2:
        items = row["Transaction"].split(",")
        items = [item.strip() for item in items]
        if k > 1:
            items = [str(combo).strip() for combo in combinations(items, k)]
        for item in items:
            if item in itemsetDict:
                itemsetDict[item] += 1
        k += 1

itemsetDict = {k: v for k, v in itemsetDict.items() if v >= threshold}


def generateFreqItems(dict):
    freqItems = []
    result = """\nFrequent Itemset: """
    for k, v in dict.items():
        items = k.strip("()").split(", ")
        if len(items) > 1:
            items = [item.strip("'") for item in items]
            freqItems.append(items)
        else:
            freqItems.append(items)
    for i in range(len(freqItems)):
        result += "{" + ", ".join(freqItems[i]) + "}"
        if i < len(freqItems) - 1:
            result += ", "
    print(result)


def generateRules(dict):
    count = 0
    for k, v in dict.items():
        items = k.strip("()").split(", ")
        if len(items) > 1:
            items = [item.strip("'") for item in items]
            confCalcA = dict[k] / dict[items[0]]
            confCalcB = dict[k] / dict[items[1]]
            if confCalcA >= confidence / 100:
                count += 1
                print(
                    f"\nRule {str(count)}: {items[0]} -> {items[1]} \nConfidence: {round((confCalcA*100), 2)}% \nSupport: {round(((v/len(transactions) * 100)), 2)}%"
                )
            if confCalcB >= confidence / 100:
                count += 1
                print(
                    f"\nRule {str(count)}: {items[1]} -> {items[0]} \nConfidence: {round((confCalcB*100), 2)}% \nSupport: {round(((v/len(transactions) * 100)), 2)}%"
                )
    print("\n")


generateFreqItems(itemsetDict)
generateRules(itemsetDict)
