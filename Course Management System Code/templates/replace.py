# Open the HTML file for reading
with open("register.html", "r") as f:
    # Read the contents of the file into a string
    html = f.read()

# Replace "asset" with "static" using the string replace method
html = html.replace("asset", "static")

# Replace "scripts" with "static"
html = html.replace("statics", "static")

# Open the same file for writing, overwriting the original contents
with open("register.html", "w") as f:
    # Write the modified HTML back to the file
    f.write(html)