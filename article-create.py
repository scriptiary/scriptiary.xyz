import os
from datetime import datetime
from jinja2 import Template

def create_article(title, short_description, long_description):
    # Format the current date and time
    current_date = datetime.now().strftime("%m%d%y")

    # Create the file name using the provided title and current date
    file_name = f"articles/{title.lower().replace(' ', '-')}-{current_date}.html"

    # HTML template
    html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }} - Scriptiary</title>
    <link rel="stylesheet" href="/CSS/main.css">
    <link rel="icon" type="image/x-icon" href="/images/favicon.ico">
    <style>.short-description{ color: #000000; display: none;}</style>
</head>
<body>
    <div class="header">
        <div class="container"><h1><img src="/images/favicon.ico" class="logo">Scriptiary</h1></div>
        <p class="tagline">Unlocking Roblox - One line of code at a time</p>
    </div>
    <h1 class=title>{{ title }}</h1>
    <p class=short-description>{{ short_description }}</p>
    <p class=description>{{ long_description }}</p>
    <footer>
        <p>© Scriptiary 2023</p>
        <a href="/legal/privacy-policy.html" style="text-decoration: underline; cursor: pointer;"><p>Privacy Policy</p></a>
        <a href="/legal/disclaimer.html" style="text-decoration: underline; cursor: pointer;"><p>Disclaimers</p></a>
    </footer>
</body>
</html>
"""

    # Create the file and write the HTML template
    with open(file_name, "w") as file:
        file.write(Template(html_template).render(title=title, short_description=short_description, long_description=long_description))

    print(f"Article created successfully: {file_name}")

def generate_index_page():
    # Get the current date
    current_date = datetime.now().strftime("%d %B %Y")

    # Get a list of all articles in the "articles" directory
    articles = []
    for file_name in os.listdir("articles"):
        if file_name.endswith(".html"):
            with open(os.path.join("articles", file_name), "r") as article_file:
                article_content = article_file.read()
                
                # Extract title, short description, and description
                title = article_content.split('<h1 class=title>')[1].split('</h1>')[0]
                short_description = article_content.split('<p class=short-description>')[1].split('</p>')[0]
                description = article_content.split('<p class=description>')[1].split('</p>')[0]

                # Try to extract date, use current date if the string is not found
                try:
                    date = article_content.split('<p class="caption">')[1].split('</p>')[0]
                except IndexError:
                    date = current_date

                articles.append({
                    "title": title,
                    "short_description": short_description,
                    "date": date,
                    "url": f"/articles/{file_name}",
                    "image": "/images/example.png"  # Replace with the actual image path
                })

    # Load the index template and render it with the article data
    index_template = Template(open("index_template.html", "r").read())
    index_content = index_template.render(articles=articles)

    # Write the generated index content to the actual index.html file
    with open("index.html", "w") as index_file:
        index_file.write(index_content)

if __name__ == "__main__":
    article_title = input("Enter the title for the article: ")
    short_description = input("Enter the short description for the article (visible on index): ")
    long_description = input("Enter the long description for the article (visible on article page): ")
    create_article(article_title, short_description, long_description)
    generate_index_page()
