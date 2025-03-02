document.getElementById('searchForm').addEventListener('submit', function (event) {
    event.preventDefault();

    const folderInput = document.getElementById('folderInput');
    const searchString = document.getElementById('searchString').value;
    const files = folderInput.files;

    if (files.length === 0 || !searchString) return;

    // Prepare the results table and hide the no results message
    document.getElementById('resultsTable').style.display = 'none';
    document.getElementById('resultHeader').style.display = 'none';
    document.getElementById('noResultsMessage').style.display = 'none';
    const resultsTable = document.getElementById('resultsTable');
    resultsTable.innerHTML = `
        <tr>
            <th>File Name</th>
            <th>Matching Line</th>
        </tr>
    `;

    let resultFound = false;

    // Highlighting style
    const highlightStyle = (text, searchStr) => {
        const regex = new RegExp(`(${searchStr})`, 'gi'); // Case insensitive matching
        return text.replace(regex, '<span class="highlight">$1</span>');
    };

    // Loop through each selected file
    Array.from(files).forEach(file => {
        if (!file.name.toLowerCase().endsWith('.pdf')) return; // Skip non-PDF files

        const reader = new FileReader();
        reader.onload = function (event) {
            const pdfData = new Uint8Array(event.target.result);

            pdfjsLib.getDocument(pdfData).promise.then(function (pdf) {
                let matches = [];
                const numPages = pdf.numPages;

                const searchTextInPage = (pageNum) => {
                    pdf.getPage(pageNum).then(function (page) {
                        page.getTextContent().then(function (textContent) {
                            const text = textContent.items.map(item => item.str).join(' ');
                            const regex = new RegExp(searchString, 'i');
                            if (regex.test(text)) {
                                text.split('\n').forEach(line => {
                                    if (line.toLowerCase().includes(searchString.toLowerCase())) {
                                        // Highlight the search string in the matching line
                                        const highlightedLine = highlightStyle(line.trim(), searchString);
                                        matches.push([file.webkitRelativePath, highlightedLine]);
                                    }
                                });
                            }
                        }).then(() => {
                            if (pageNum < numPages) {
                                searchTextInPage(pageNum + 1);
                            } else {
                                // All pages processed
                                if (matches.length > 0) {
                                    resultFound = true;
                                    matches.forEach(match => {
                                        const row = document.createElement('tr');
                                        row.innerHTML = `<td>${match[0]}</td><td>${match[1]}</td>`;
                                        resultsTable.appendChild(row);
                                    });
                                    document.getElementById('resultsTable').style.display = 'block';
                                    document.getElementById('resultHeader').style.display = 'block';
                                }
                                else {
                                    if (!resultFound) {
                                        document.getElementById('noResultsMessage').style.display = 'block';
                                    }
                                }
                            }
                        });
                    });
                };

                searchTextInPage(1);
            });
        };
        reader.readAsArrayBuffer(file);


    });

});