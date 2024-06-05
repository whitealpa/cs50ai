import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    
    probability_distribution = dict()
    number_of_pages_in_current_page = len(corpus[page])
    
    if number_of_pages_in_current_page == 0:
        probability_distribution = equally_distribute(corpus)
    else:
        probability_distribution = weighted_distribute(corpus, page, damping_factor)

    return probability_distribution


def equally_distribute(corpus):
    probability_distribution = dict()
    equally_distributed = 1 / len(corpus)
    
    for each_page in corpus:
        probability_distribution[each_page] = equally_distributed
        
    return probability_distribution
    

def weighted_distribute(corpus, page, damping_factor):
    probability_distribution = dict()
    probability_of_page_in_current_page = damping_factor / len(corpus[page])
    probability_of_any_page = (1 - damping_factor) / len(corpus)
    
    for each_page in corpus:
        if each_page in corpus[page]:
            probability_distribution[each_page] = probability_of_any_page + probability_of_page_in_current_page
        else:
            probability_distribution[each_page] = probability_of_any_page
            
    return probability_distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    
    probability_distribution = dict()
    next_page = None
    
    for _ in range(n):
        if len(probability_distribution) == 0:
            start_page = random.choice(list(corpus))
            new_sample = transition_model(corpus, start_page, damping_factor)
            next_page = random.choices(list(new_sample.keys()), list(new_sample.values()))   
            for page, probability in new_sample.items():
                probability_distribution[page] = probability       
        else:
            new_sample = transition_model(corpus, next_page[0], damping_factor)
            next_page = random.choices(list(new_sample.keys()), list(new_sample.values())) 
        
        for page, probability in new_sample.items():
            probability_distribution[page] += probability
    
    probability_distribution = probability_average(probability_distribution, n)
    
    return probability_distribution


def probability_average(distribution, n):
    for page, probability in distribution.items():
        distribution[page] = probability / n
        
    return distribution
    

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    raise NotImplementedError


if __name__ == "__main__":
    main()
