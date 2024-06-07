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
    if len(corpus[page]) == 0:
        return equally_distribute(corpus)
    else:
        return weighted_distribute(corpus, page, damping_factor)


def equally_distribute(corpus):
    equally_distributed = 1 / len(corpus)
    return {page: equally_distributed for page in corpus}
    

def weighted_distribute(corpus, page, damping_factor):
    probability_distribution = dict()
    probability_of_page_in_current_page = damping_factor / len(corpus[page])
    probability_of_any_page = (1 - damping_factor) / len(corpus)
    
    for each_page in corpus:
        probability_distribution[each_page] = probability_of_any_page
        if each_page in corpus[page]:
            probability_distribution[each_page] += probability_of_page_in_current_page
    return probability_distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    pagerank = dict()
    start_page = random.choice(list(corpus))
    
    for _ in range(n):
        new_sample = transition_model(corpus, start_page if len(pagerank) == 0 else next_page, damping_factor)
        next_page = random.choices(list(new_sample.keys()), list(new_sample.values()))[0]
        for page, probability in new_sample.items():
            pagerank[page] = probability + pagerank.setdefault(page, 0)
            
    return probability_average(pagerank, n)


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
    
    total_number_of_pages = len(corpus)
    start_probability = 1 / total_number_of_pages
    random_probablity = (1 - damping_factor) / total_number_of_pages
    
    pagerank = {page: start_probability for page in corpus}
    previous_pagerank = {page: 0 for page in corpus}    
    value_converged = False
    
    while not value_converged:
        for page in corpus:
            pagerank[page] = random_probablity + damping_factor * sum_of_incoming_pages_probability(page, pagerank, corpus)   
        value_converged = is_value_converged(previous_pagerank, pagerank)
        previous_pagerank = {page: probability for page, probability in pagerank.items()}    
                
    return pagerank


def is_value_converged(previous_pagerank, pagerank):
    threshold = 0.0001
    converged = 0
    all_pages = len(pagerank)
    
    for page in pagerank:
        different = abs(pagerank[page] - previous_pagerank[page])
        if different < threshold:
            converged += 1
    return True if all_pages == converged else False
            
            
def sum_of_incoming_pages_probability(page, pagerank, corpus):
    sum = 0
    
    for link in corpus:
        probability_of_incoming_page = pagerank[link]
        number_of_links_in_incoming_page = len(corpus[link])
        
        if number_of_links_in_incoming_page == 0:
            sum += probability_of_incoming_page / len(pagerank)  
        elif page in corpus[link]:         
            sum += probability_of_incoming_page / number_of_links_in_incoming_page
    
    return sum


if __name__ == "__main__":
    main()
