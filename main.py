import requests
import json
import sys
import os

class DataFetcher:
    def __init__(self):
        self.base_url = "https://jsonplaceholder.typicode.com"
        self.cache_file = "cache.json"
        self.data = {"posts": [], "users": []}

    def fetch_data(self):
        """Fetches data from API endpoints with error handling."""
        print("Fetching data from API...")
        try:
            # Fetching from Endpoint 1: Posts
            posts_response = requests.get(f"{self.base_url}/posts", timeout=10)
            posts_response.raise_for_status()
            
            # Fetching from Endpoint 2: Users
            users_response = requests.get(f"{self.base_url}/users", timeout=10)
            users_response.raise_for_status()

            self.data["posts"] = posts_response.json()
            self.data["users"] = users_response.json()
            
            self.save_to_cache()
            print("Data fetched and cached successfully.\n")

        except requests.exceptions.Timeout:
            print("Error: The request timed out.")
        except requests.exceptions.ConnectionError:
            print("Error: Network failure. Check your internet connection.")
        except requests.exceptions.HTTPError as err:
            print(f"Error: Invalid response received. {err}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def save_to_cache(self):
        """Stores fetched data in a local file."""
        try:
            with open(self.cache_file, 'w') as f:
                json.dump(self.data, f, indent=4)
        except IOError as e:
            print(f"Error saving cache: {e}")

    def load_from_cache(self):
        """Loads data from local storage if available."""
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r') as f:
                    self.data = json.load(f)
                return True
            except json.JSONDecodeError:
                print("Error: Cache file is malformed.")
        return False

    def list_posts(self, user_id=None):
        """Lists items with filtering options."""
        print(f"{'ID':<5} | {'Title':<50} | {'User ID'}")
        print("-" * 70)
        
        count = 0
        for post in self.data["posts"]:
            # Filtering Logic
            if user_id and str(post['userId']) != str(user_id):
                continue
                
            # Truncate title for clean CLI output
            title = (post['title'][:47] + '..') if len(post['title']) > 47 else post['title']
            print(f"{post['id']:<5} | {title:<50} | {post['userId']}")
            count += 1
            
        if count == 0:
            print("No posts found matching criteria.")
        print("\n")

    def get_post_details(self, post_id):
        """Show detailed view for a single item by ID."""
        post = next((p for p in self.data["posts"] if str(p['id']) == str(post_id)), None)
        
        if post:
            # Enrich data by finding the author (User)
            author = next((u for u in self.data["users"] if u['id'] == post['userId']), None)
            author_name = author['name'] if author else "Unknown"

            print("\n=== POST DETAILS ===")
            print(f"ID: {post['id']}")
            print(f"Title: {post['title']}")
            print(f"Author: {author_name} (User ID: {post['userId']})")
            print("Body:")
            print(post['body'])
            print("====================\n")
        else:
            print(f"Error: Post with ID {post_id} not found.")

def main():
    app = DataFetcher()
    
    # Check if we have cached data, otherwise fetch fresh
    if not app.load_from_cache():
        app.fetch_data()

    while True:
        print("1. Refresh Data (API Call)")
        print("2. List All Posts")
        print("3. Filter Posts by User ID")
        print("4. View Post Details")
        print("5. Exit")
        
        choice = input("Enter choice: ")

        if choice == '1':
            app.fetch_data()
        elif choice == '2':
            app.list_posts()
        elif choice == '3':
            uid = input("Enter User ID to filter by: ")
            app.list_posts(user_id=uid)
        elif choice == '4':
            pid = input("Enter Post ID to view: ")
            app.get_post_details(post_id=pid)
        elif choice == '5':
            sys.exit()
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()