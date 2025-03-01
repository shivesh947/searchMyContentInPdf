from flask import Flask, render_template_string, request
import os
import PyPDF2

app = Flask(__name__)

# Function to search PDF files for the given string in the folder and subfolders
def search_pdf_in_folder(folder_path, search_string):
    results = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith('.pdf'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'rb') as pdf_file:
                        pdf_reader = PyPDF2.PdfReader(pdf_file)
                        for page_num in range(len(pdf_reader.pages)):
                            page = pdf_reader.pages[page_num]
                            text = page.extract_text()
                            if text and search_string.lower() in text.lower():
                                for line in text.split('\n'):
                                    if search_string.lower() in line.lower():
                                        results.append((file_path, line.strip()))
                                        break
                except Exception as e:
                    print(f"Could not read {file_path}: {e}")
    return results

# HTML template with embedded CSS for a beautiful UI
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PDF Search Tool</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f7fc;
            margin: 0;
            padding: 0;
            color: #333;
        }

        header {
            background-color: #4CAF50;
            color: white;
            text-align: center;
            padding: 20px 0;
            margin-bottom: 30px;
        }

        h1 {
            margin: 0;
            font-size: 24px;
        }

        form {
            width: 50%;
            margin: 0 auto;
            background-color: #ffffff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
        }

        label {
            font-size: 16px;
            font-weight: bold;
            margin-bottom: 8px;
            display: block;
        }

        input[type="text"] {
            width: 100%;
            padding: 10px;
            font-size: 16px;
            border: 1px solid #ccc;
            border-radius: 4px;
            margin-bottom: 15px;
        }

        input[type="submit"] {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 12px 25px;
            font-size: 16px;
            border-radius: 4px;
            cursor: pointer;
        }

        input[type="submit"]:hover {
            background-color: #45a049;
        }

        table {
            width: 80%;
            margin: 30px auto;
            border-collapse: collapse;
            background-color: #fff;
            border-radius: 8px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
        }

        table th, table td {
            padding: 12px;
            text-align: left;
            border: 1px solid #ddd;
        }

        table th {
            background-color: #f4f4f4;
            color: #333;
        }

        table tr:nth-child(even) {
            background-color: #f9f9f9;
        }

        .message {
            text-align: center;
            font-size: 18px;
            color: #ff5722;
        }
    </style>
</head>
<body>
    <header>
        <h1>PDF Search Tool</h1>
    </header>

    <form method="POST">
        <label for="folder_path">Folder Path:</label>
        <input type="text" id="folder_path" name="folder_path" required placeholder="Enter folder path here...">
        
        <label for="search_string">Search String:</label>
        <input type="text" id="search_string" name="search_string" required placeholder="Enter search string here...">
        
        <input type="submit" value="Search">
    </form>

    {% if results %}
    <h2 style="text-align: center;">Search Results:</h2>
    <table>
        <tr>
            <th>File Path</th>
            <th>Matching Line</th>
        </tr>
        {% for result in results %}
        <tr>
            <td>{{ result[0] }}</td>
            <td>{{ result[1] }}</td>
        </tr>
        {% endfor %}
    </table>
    {% elif request.method == 'POST' %}
    <div class="message">No results found for your search.</div>
    {% endif %}
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    results = []
    if request.method == 'POST':
        folder_path = request.form['folder_path']
        search_string = request.form['search_string']
        results = search_pdf_in_folder(folder_path, search_string)

    return render_template_string(html_template, results=results)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))