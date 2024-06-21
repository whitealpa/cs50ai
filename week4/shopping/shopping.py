import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """

    with open(filename, newline='') as f:
        shopping_data = csv.reader(f) 
        shopping_data = list(shopping_data)
    
    labels = get_labels_list(shopping_data)
    evidence = clean_evidence_data(shopping_data)
    
    print()
    print("clean up data")
    print("evidence:")
    print(evidence)
    print("labels:")
    print(labels)
    
    return (evidence, labels)

def get_labels_list(shopping_data):
    exclude_header = slice(1, None)
    label_index = -1
    return [1 if data[label_index] == 'TRUE'
              else 0 for data in shopping_data[exclude_header]]

def clean_evidence_data(shopping_data):
    evidence_data = exclude_label_and_header(shopping_data)
    data_types = get_data_types(shopping_data)
    int_types = get_int_types()
    float_types = get_float_types()

    for data in evidence_data:
        for i in range(len(data_types)):
            if data_types[i] in int_types:
                data[i] = int(data[i])
            elif data_types[i] in float_types:
                data[i] = float(data[i])
            elif data_types[i] == 'VisitorType':
                data[i] = 1 if data[i] == 'Returning_Visitor' else 0
            elif data_types[i] == 'Weekend':
                data[i] = 1 if data[i] == 'TRUE' else 0
            elif data_types[i] == 'Month':
                data[i] = convert_month_to_int(data[i])
    return evidence_data           

def exclude_label_and_header(shopping_data):
    exclude_header = slice(1, None)
    exclude_label = slice(None, -1)
    return [data[exclude_label] for data in shopping_data[exclude_header]]

def get_data_types(shopping_data):
    header = 0
    exclude_label = slice(None, -1)
    return shopping_data[header][exclude_label]

def get_int_types():
    return {
        "Administrative", 
        "Informational", 
        "ProductRelated", 
        "OperatingSystems", 
        "Browser", 
        "Region", 
        "TrafficType"
        }
    
def get_float_types():
    return {
        "Administrative_Duration", 
        "Informational_Duration", 
        "ProductRelated_Duration", 
        "BounceRates", 
        "ExitRates", 
        "PageValues", 
        "SpecialDay"
        }
    
def convert_month_to_int(month):
    month_int_map = {
        'jan': 0,
        'feb': 1,
        'mar': 2,
        'apr': 3,
        'may': 4,
        'jun': 5,
        'jul': 6,
        'aug': 7,
        'sep': 8,
        'oct': 9,
        'nov': 10,
        'dec': 11
    }
    first_three_letters = slice(None, 3)
    month = month[first_three_letters].lower()
    return month_int_map[month]

def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    raise NotImplementedError


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    raise NotImplementedError


if __name__ == "__main__":
    main()
