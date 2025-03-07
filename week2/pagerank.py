import os
import random
import re
import sys
import copy

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
    pd = {}
    dict_len = len(corpus.keys())
    page_links = len(corpus[page])

    if page_links < 1:
        for key in corpus:
            pd[key] = 1/dict_len

    else:    
        random_factor = (1-damping_factor)/len(corpus)
        even_factor = damping_factor/len(corpus[page])
        for key in corpus:
            if key not in corpus[page]:
                pd[key] = random_factor
            else:
                pd[key] = random_factor + even_factor
    return pd
    


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    curr_page = random.choice(list(corpus.keys()))
    pagerank = {}

    for key in corpus:
        pagerank[key] = 0

    for i in range(n):
        pagerank[curr_page] += 1

        next_page_prob = transition_model(corpus, curr_page, damping_factor)

        next_pages_weight = []
        next_pages = []
        for key in corpus:
            next_pages.append(key)
            next_pages_weight.append(next_page_prob[key])

        curr_page = random.choices(next_pages, weights=next_pages_weight, k=1)[0]

    for key in pagerank:
        pagerank[key] = pagerank[key]/n

    return pagerank
import copy

def iterate_pagerank(corpus: dict, damping_factor: float):
    d = damping_factor
    pages = list(corpus.keys())
    len_pages = len(pages)

    pagerank = {page: 1 / len_pages for page in pages}

    while True:
        prev_pagerank = copy.deepcopy(pagerank)

        # Compute total contribution from dangling pages (pages with no outgoing links)
        dangling_contribution = sum(pagerank[page] for page in pages if len(corpus[page]) == 0) / len_pages

        for curr_page in pages:
            random_factor = (1 - d) / len_pages
            links_factor = dangling_contribution  # Start with dangling contribution

            for page in pages:
                if curr_page in corpus[page] and len(corpus[page]) > 0:
                    links_factor += pagerank[page] / len(corpus[page])

            pagerank[curr_page] = random_factor + d * links_factor

        # Check for convergence
        if max(abs(prev_pagerank[page] - pagerank[page]) for page in pages) < 0.001:
            break

    return pagerank




if __name__ == "__main__":
    main()