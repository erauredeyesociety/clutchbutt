import os
import json
from datetime import datetime

# Define the function to generate markdown files from json data
def generate_markdown_from_json(json_dir, output_dir):
    # Get all json files from the directory
    json_files = [f for f in os.listdir(json_dir) if f.endswith('.json')]

    # Iterate over each JSON file
    for json_file in json_files:
        category = json_file.split('_')[1].replace('.json', '')  # Extract category from filename
        json_path = os.path.join(json_dir, json_file)

        # Read the json data
        with open(json_path, 'r') as file:
            data = json.load(file)

        # Get today's date
        today_date = datetime.today().strftime('%Y-%m-%d')

        # Initialize the markdown content
        markdown_content = f"+++ \n" \
                           f"author = \"cletus\"\n" \
                           f"title = \"{category} - {today_date}\"\n" \
                           f"date = \"{today_date}\"\n" \
                           f"description = \"{category} news for today\"\n" \
                           f"tags = [\n" \
                           f"    \"{category}\",\n" \
                           f"]\n" \
                           f"+++\n\n"

        # Access the 'daily_links' section in the data
        daily_links = data.get("daily_links", {})

        # Iterate through the websites and their respective articles in the 'daily_links' section
        for website, articles in daily_links.items():
            markdown_content += f"# {website}\n\n"
            markdown_content += f"<details>\n" \
                                f"<summary>View Articles</summary>\n" \
                                f"<br>\n"

            # Iterate through each article (which is a dictionary)
            for article in articles:
                headline = article.get('headline')
                link = article.get('link')

                if headline and link:
                    # Prepend the 12ft proxy URL
                    proxied_link = f"https://12ft.io/{link}"
                    markdown_content += f"\n[{headline}]({proxied_link})\n"  # Add a newline after each link

            markdown_content += f"\n</details>\n\n"

        # Ensure the output directory exists
        os.makedirs(output_dir, exist_ok=True)

        # Create the output markdown file with UTF-8 encoding
        output_file_path = os.path.join(output_dir, f"{category}.md")
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            output_file.write(markdown_content)

# Set the paths to your json directory and output markdown directory
json_directory = 'tmp_json'
output_directory = 'content/posts'

# Generate markdown files
# generate_markdown_from_json(json_directory, output_directory)