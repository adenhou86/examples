import agno

def perform_web_search(query: str):
    """
    Uses the agno web tool to perform a search based on the provided query.
    Returns a list of results with each result containing a title, URL, and snippet.
    """
    try:
        # Call the web search tool; the expected payload is a dictionary with the 'query' key.
        results = agno.web.search({"query": query})
        return results
    except Exception as e:
        print(f"An error occurred while searching: {e}")
        return []

def main():
    # Prompt the user to enter a search query
    query = input("Enter your search query: ")
    print(f"\nSearching for: {query}\n")

    # Perform the web search
    results = perform_web_search(query)
    
    if results:
        print("Search Results:")
        for idx, result in enumerate(results, start=1):
            print("-" * 40)
            print(f"Result {idx}:")
            print("Title: ", result.get("title", "No title available"))
            print("URL: ", result.get("url", "No URL available"))
            print("Snippet: ", result.get("snippet", "No snippet available"))
            print("-" * 40)
    else:
        print("No search results found.")

if __name__ == "__main__":
    main()
