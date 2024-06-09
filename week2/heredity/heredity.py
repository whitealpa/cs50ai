import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }
    
    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    no_gene = set(people) - one_gene - two_genes
    genes = [no_gene, one_gene, two_genes]
    total_probability = 1
    
    for number_of_genes in range(len(genes)):
        for person in genes[number_of_genes]:
            has_parent = people[person]["mother"]
        
            if has_parent:         
                not_from_mother = probability_not_from("mother", people, person, genes)
                not_from_father = probability_not_from("father", people, person, genes)
                from_mother = probability_from("mother", people, person, genes)
                from_father = probability_from("father", people, person, genes)
                
                if number_of_genes == 0:
                    probability = not_from_mother * not_from_father
                elif number_of_genes == 1:
                    probability = (not_from_mother * from_father) + (from_mother * not_from_father)
                elif number_of_genes == 2:
                    probability = from_mother * from_father
                    
            elif not has_parent:
                probability = PROBS["gene"][number_of_genes]
        
            probability *= PROBS["trait"][number_of_genes][person in have_trait]
            total_probability *= probability

    return total_probability


def probability_not_from(parent, people, person, genes):
    this_parent = people[person][parent]
    if this_parent in genes[0]:
        probability = 1 - PROBS["mutation"]
    elif this_parent in genes[1]:
        probability = 0.5
    elif this_parent in genes[2]:
        probability = PROBS["mutation"]
    return probability


def probability_from(parent, people, person, genes):
    this_parent = people[person][parent]
    if this_parent in genes[0]:
        probability = PROBS["mutation"]
    elif this_parent in genes[1]:
        probability = 0.5
    elif this_parent in genes[2]:
        probability = 1 - PROBS["mutation"]
    return probability


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person in probabilities:
        gene_index = 1 if person in one_gene else 2 if person in two_genes else 0
        trait_index = True if person in have_trait else False
        
        probabilities[person]["gene"][gene_index] += p
        probabilities[person]["trait"][trait_index] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """    
    for person in probabilities:
        normalize_distribution(probabilities, person, "gene")
        normalize_distribution(probabilities, person, "trait")
   

def normalize_distribution(probabilities, person, distribution):
        person_distribution = probabilities[person][distribution]
        sum_total = 0
        values = []
        normalized_values = []
        
        for i in range(len(person_distribution)):
            sum_total += (person_distribution[i])
            values.append(person_distribution[i])
        
        normalized_values = [value / sum_total for value in values]
        
        for i in range(len(person_distribution)):
            person_distribution[i] = normalized_values[i]


if __name__ == "__main__":
    main()
