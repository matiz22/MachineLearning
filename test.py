# ID3 Decision Tree Tutorial
# This notebook walks you through implementing an ID3 decision tree from scratch in Python.
# We'll cover:
# 1. Calculating Entropy
# 2. Information Gain
# 3. Split Information and Gain Ratio
# 4. Building the ID3 Tree
# 5. Displaying the Tree

# ## 1. Import Necessary Libraries
import math
import pandas as pd

# ## 2. Entropy Calculation
# Entropy measures the amount of uncertainty in a dataset.
# The formula: H(S) = - \sum_{i=1}^c p_i \log_2(p_i)
# where p_i is the proportion of label i in the set.


def entropy(labels):
    """
    Calculate the entropy of a list/Series of class labels.
    labels: iterable of class labels
    Returns: entropy value
    """
    counts = labels.value_counts()
    total = len(labels)
    ent = 0.0
    for count in counts:
        p = count / total
        ent -= p * math.log2(p)
    return ent


# Example usage:
# data = pd.Series(['yes', 'no', 'yes', 'yes', 'no'])\#
# print("Entropy:", entropy(data))

# ## 3. Information Gain
# Gain(S, A) = Entropy(S) - \sum_{v \in values(A)} \frac{|S_v|}{|S|} Entropy(S_v)


def information_gain(df, attribute, target_name="target"):
    """
    Compute the information gain of splitting df on attribute.
    df: pandas DataFrame
    attribute: column name to split on
    target_name: name of the target/class column
    Returns: information gain value
    """
    # Base entropy
    base_entropy = entropy(df[target_name])
    # Values and weighted entropy
    values = df[attribute].unique()
    weighted_ent = 0.0
    for val in values:
        subset = df[df[attribute] == val]
        weight = len(subset) / len(df)
        weighted_ent += weight * entropy(subset[target_name])
    return base_entropy - weighted_ent


# ## 4. Split Information and Gain Ratio
# SplitInfo(A) = - \sum_{v \in values(A)} \frac{|S_v|}{|S|} \log_2(\frac{|S_v|}{|S|})
# GainRatio(A) = Gain(S, A) / SplitInfo(A)


def split_info(df, attribute):
    """
    Compute the split information for attribute in df.
    """
    total = len(df)
    values = df[attribute].unique()
    split_info_val = 0.0
    for val in values:
        subset = df[df[attribute] == val]
        p = len(subset) / total
        split_info_val -= p * math.log2(p) if p > 0 else 0
    return split_info_val


def gain_ratio(df, attribute, target_name="target"):
    """
    Compute the gain ratio of splitting df on attribute.
    """
    gain = information_gain(df, attribute, target_name)
    si = split_info(df, attribute)
    return gain / si if si != 0 else 0


# ## 5. Building the ID3 Tree
# The ID3 algorithm recursively selects the attribute with highest gain (or gain ratio) to split on.


class DecisionNode:
    def __init__(self, attribute=None, label=None, branches=None):
        self.attribute = attribute  # attribute to split on
        self.label = label  # class label if leaf
        self.branches = branches or {}  # dict: attribute value -> child node


def id3(df, attributes, target_name="target", use_gain_ratio=False):
    """
    Build an ID3 decision tree.
    df: pandas DataFrame
    attributes: list of attribute names to consider
    target_name: name of target column
    use_gain_ratio: whether to use gain ratio instead of gain
    Returns: root DecisionNode
    """
    # If all examples have same label, return leaf
    labels = df[target_name]
    if len(labels.unique()) == 1:
        return DecisionNode(label=labels.iloc[0])
    # If no attributes left, return majority label
    if not attributes:
        majority = labels.mode()[0]
        return DecisionNode(label=majority)
    # Select best attribute
    best_attr = None
    best_score = -float("inf")
    for attr in attributes:
        score = (
            gain_ratio(df, attr, target_name)
            if use_gain_ratio
            else information_gain(df, attr, target_name)
        )
        if score > best_score:
            best_score = score
            best_attr = attr
    # Create tree node
    tree = DecisionNode(attribute=best_attr)
    # For each value of best_attr, create branch
    for val in df[best_attr].unique():
        subset = df[df[best_attr] == val]
        if subset.empty:
            # Add leaf with majority label
            majority = labels.mode()[0]
            tree.branches[val] = DecisionNode(label=majority)
        else:
            # Recurse on subset without best_attr
            remaining_attrs = [a for a in attributes if a != best_attr]
            tree.branches[val] = id3(
                subset, remaining_attrs, target_name, use_gain_ratio
            )
    return tree


# ## 6. Displaying the Tree
# We'll write a helper function to print the tree structure.


def print_tree(node, depth=0):
    indent = "  " * depth
    if node.label is not None:
        print(f"{indent}Leaf: {node.label}")
    else:
        print(f"{indent}Attribute: {node.attribute}")
        for val, child in node.branches.items():
            print(f"{indent}|-- Value = {val}")
            print_tree(child, depth + 1)


# ## 7. Example Usage
if __name__ == "__main__":
    # Sample dataset: Play Tennis
    data = {
        "Outlook": [
            "Sunny",
            "Sunny",
            "Overcast",
            "Rain",
            "Rain",
            "Rain",
            "Overcast",
            "Sunny",
            "Sunny",
            "Rain",
            "Sunny",
            "Overcast",
            "Overcast",
            "Rain",
        ],
        "Temperature": [
            "Hot",
            "Hot",
            "Hot",
            "Mild",
            "Cool",
            "Cool",
            "Cool",
            "Mild",
            "Cool",
            "Mild",
            "Mild",
            "Mild",
            "Hot",
            "Mild",
        ],
        "Humidity": [
            "High",
            "High",
            "High",
            "High",
            "Normal",
            "Normal",
            "Normal",
            "High",
            "Normal",
            "Normal",
            "Normal",
            "High",
            "Normal",
            "High",
        ],
        "Wind": [
            "Weak",
            "Strong",
            "Weak",
            "Weak",
            "Weak",
            "Strong",
            "Strong",
            "Weak",
            "Weak",
            "Weak",
            "Strong",
            "Strong",
            "Weak",
            "Strong",
        ],
        "target": [
            "No",
            "No",
            "Yes",
            "Yes",
            "Yes",
            "No",
            "Yes",
            "No",
            "Yes",
            "Yes",
            "Yes",
            "Yes",
            "Yes",
            "No",
        ],
    }
    df = pd.read_csv("data/gielda.txt")
    attrs = ["up", "down"]

    # Build tree (using Gain Ratio)
    tree = id3(df, attrs, target_name="target", use_gain_ratio=True)
    print("Decision Tree:\n")
    print_tree(tree)
