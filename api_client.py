import requests
import json

def fetch_data():
    base_url = "https://newsdata.io/api/1/latest"
    api_key = "pub_b993b1572ec14b6b876078d0e0bf64e8"
    
    params = {
        "apikey": api_key,
        "country": "in,us",
        "language": "en",
        "category": "top", 
        "prioritydomain": "top",
        "image": "1",
        "removeduplicate": "1"
    }

    try:
        print(f"Fetching data from {base_url}...")
        response = requests.get(base_url, params=params)
        
        # Check if the request was successful
        response.raise_for_status()
        
        # Parse JSON
        data = response.json()
        
        print("\n--- API Response ---")
        # Print a summarized version or the full thing
        print(f"Status: {data.get('status')}")
        print(f"Total Results: {data.get('totalResults')}")
        
        results = data.get('results', [])
        
        if results:
            print(f"\n--- Top 5 Unique Breaking News ---\n")
            
            unique_articles = []
            seen_titles = set()
            
            for article in results:
                title = article.get('title')
                # Check for duplicate titles to ensure uniqueness
                if title and title not in seen_titles:
                    unique_articles.append(article)
                    seen_titles.add(title)
                
                # Stop once we have 5 unique articles
                if len(unique_articles) >= 5:
                    break
            
            if unique_articles:
                for i, article in enumerate(unique_articles, 1):
                    print(f"{i}. {article.get('title')}")
                    print(f"   Source: {article.get('source_id')}")
                    print(f"   Link: {article.get('link')}")
                    print("-" * 40)
            else:
                 print("No unique articles found.")

        else:
            print("No results found.")
        
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        if 'response' in locals() and response.status_code == 401:
             print("Authentication failed. Please check your API key.")

if __name__ == "__main__":
    fetch_data()
