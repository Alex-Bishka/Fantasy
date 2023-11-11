// script.js

// on init load
document.addEventListener('DOMContentLoaded', function() {
    initializeDropdowns();
    loadSelectedData();
});

// enable enter for users typing in search input
function enterPressed(event) {
    // Check if the Enter key was pressed
    if (event.key === "Enter") {
        // Call the searchData function
        searchData();
    }
}

// debounce
// Set a variable to keep track of the timeout ID
let typingTimeout;

function userStoppedTyping() {
    // Clear any existing timeouts
    clearTimeout(typingTimeout);

    // Set a new timeout
    typingTimeout = setTimeout(() => {
        searchData();
    }, 1500); // Set the delay to 1.5 seconds
}

// Get the input element
const inputElement = document.getElementById('searchBox');

// Add an event listener for the input event
inputElement.addEventListener('input', userStoppedTyping);

// Add an event listener for the keydown event
inputElement.addEventListener('keydown', enterPressed);

// Initialize dropdowns with options (you should populate these with the actual years and positions you have)
function initializeDropdowns() {
    const years = ['2023', '2022', '2021']; // Add more years as needed
    const positions = ['QB', 'RB', 'WR', 'TE']; // Add more positions as needed

    const yearSelect = document.getElementById('yearSelect');
    const positionSelect = document.getElementById('positionSelect');

    years.forEach(year => {
        let option = document.createElement('option');
        option.value = year;
        option.textContent = year;
        yearSelect.appendChild(option);
    });

    positions.forEach(position => {
        let option = document.createElement('option');
        option.value = position;
        option.textContent = position;
        positionSelect.appendChild(option);
    });

    // Set defaults (you could also set these based on the current year or user's preferences)
    yearSelect.value = '2023';
    positionSelect.value = 'QB';
}

// Call this function whenever you need to load data for a specific year and position
function loadSelectedData() {
    const year = document.getElementById('yearSelect').value;
    const position = document.getElementById('positionSelect').value;
    loadData(year, position);
}

// Variable to keep track of the current CSV path
let currentCSVPath = '';
let globalCsvData;
let selectedColumns;

// Modify loadData function to take parameters for year and position
function loadData(year, position) {
    currentCSVPath = `/Fantasy/Analysis/FantasyData/advanced-stats/${position}/${year}.csv`;
    fetch(currentCSVPath)
        .then(response => response.text())
        .then(csv => {
            globalCsvData = csvToJson(csv); // Store parsed data in the global variable
            selectedColumns = Object.keys(globalCsvData[0])

            // After fetching and parsing CSV data
            populateColumnCheckboxes(selectedColumns);
            renderTable(globalCsvData, selectedColumns);
        })
        .catch(error => console.error('Error loading the CSV:', error));
}

// convert the csv to json format for our table
function csvToJson(csv) {
    const lines = csv.split('\n');
    const headers = lines[0].split(',');
    const result = lines.slice(1).map(line => {
        const obj = {};
        const currentline = line.split(',');

        headers.forEach((header, i) => {
            obj[header] = currentline[i];
        });

        return obj;
    });

    return result; // This is an array of objects
}

// render the json data into the table
function renderTable(data, selectedColumns) {
    const container = document.getElementById('dataContainer');
    let table = '<table>';
    
    // Render headers for selected columns
    table += '<tr>';
    Object.keys(data[0]).forEach(key => {
        if (selectedColumns.includes(key) && key.length) {
            table += `<th>${key} <span class="sort-arrow" onclick="sortTable('${key}')">↕️</span></th>`;
        }
    });
    table += '</tr>';

    // Render rows for selected columns
    data.forEach(row => {
        if (row.name) {
            table += '<tr>';
            Object.entries(row).forEach(([key, val]) => {
                if (selectedColumns.includes(key) && key.length) {
                    table += `<td>${val}</td>`;
                }
            });
            table += '</tr>';
        }
    });
    
    table += '</table>';
    container.innerHTML = table;
}

// search input
function searchData() {
    const input = document.getElementById('searchBox');
    const filter = input.value.toUpperCase();
    const table = document.querySelector('table');
    const tr = table.getElementsByTagName('tr');

    for (let i = 0; i < tr.length; i++) {
        let td = tr[i].getElementsByTagName('td')[1]; // Change the index if you want to search in another column
        if (td) {
            let txtValue = td.textContent || td.innerText;
            if (txtValue.toUpperCase().indexOf(filter) > -1) {
                tr[i].style.display = "";
            } else {
                tr[i].style.display = "none";
            }
        }       
    }
}

// Function to download the current CSV
function downloadCSV() {
    if (!currentCSVPath) {
        alert('No CSV file is available for download.');
        return;
    }

    // Create a temporary link to trigger the download
    const tempLink = document.createElement('a');
    tempLink.href = currentCSVPath;
    tempLink.setAttribute('download', '');
    document.body.appendChild(tempLink);
    tempLink.click();
    document.body.removeChild(tempLink);
}

// Get the modal
let modal = document.getElementById("columnSelectModal");

// Get the button that opens the modal
let openModalBtn = document.getElementById("selectColumnsBtn");

// Get the <span> element that closes the modal
let span = document.getElementsByClassName("close")[0];

// When the user clicks the button, open the modal 
openModalBtn.onclick = function() {
    modal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
    modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}

function populateColumnCheckboxes(headers) {
    const container = document.getElementById('checkboxContainer');
    container.innerHTML = ''; // Clear previous checkboxes

    headers.forEach(header => {
        if (header.length) {
            // Create checkbox for each header
            const checkbox = document.createElement('input');
            checkbox.type = 'checkbox';
            checkbox.id = header;
            checkbox.name = header;
            checkbox.value = header;
            checkbox.checked = true; // Default to checked

            const label = document.createElement('label');
            label.htmlFor = header;
            label.appendChild(document.createTextNode(header));

            container.appendChild(checkbox);
            container.appendChild(label);
            container.appendChild(document.createElement('br'));
        }
    });
}

document.getElementById('selectAllBtn').addEventListener('click', () => {
    document.querySelectorAll('#checkboxContainer input[type="checkbox"]').forEach(checkbox => {
        checkbox.checked = true;
    });
});

document.getElementById('deselectAllBtn').addEventListener('click', () => {
    document.querySelectorAll('#checkboxContainer input[type="checkbox"]').forEach(checkbox => {
        checkbox.checked = false;
    });
});

document.getElementById('applyColumnsBtn').addEventListener('click', () => {
    modal.style.display = "none";
    renderTableBasedOnSelection();
});

function renderTableBasedOnSelection() {
    selectedColumns = Array.from(document.querySelectorAll('#checkboxContainer input[type="checkbox"]:checked')).map(cb => cb.value);

    // Call renderTable with selected columns
    renderTable(globalCsvData, selectedColumns);
}

let sortDirection = {}; // Object to keep track of the sort direction for each column
let currentSortedColumn = null;

function sortTable(column) {
    // Determine if the first non-null/undefined value is numeric
    let firstNonNullValue = globalCsvData.find(row => row[column] != null && row[column] !== '');
    let isNumeric = firstNonNullValue && !isNaN(firstNonNullValue[column]);

    // Toggle sort direction
    if (currentSortedColumn !== column) {
        sortDirection[column] = true; // Default to ascending when first clicked
        currentSortedColumn = column;
    } else {
        sortDirection[column] = !sortDirection[column];
    }

    // Update arrow direction for all headers
    // const headers = document.querySelectorAll('#dataContainer th');
    // headers.forEach(header => {
    //     if (header.textContent.includes(column)) {
    //         // Found the right header, update its arrow
    //         const arrowSpan = header.querySelector('.sort-arrow');
    //         arrowSpan.textContent = sortDirection[column] ? '▲' : '▼';
    //     } else {
    //         // Reset other arrows to default
    //         const arrowSpan = header.querySelector('.sort-arrow');
    //         if (arrowSpan) arrowSpan.textContent = '↕️';
    //     }
    // });

    // Sort data
    globalCsvData.sort((a, b) => {
        let valA = a[column];
        let valB = b[column];

        if (isNumeric) {
            // Convert strings to numbers for comparison
            valA = parseFloat(valA);
            valB = parseFloat(valB);
        }

        if (valA < valB) {
            return sortDirection[column] ? -1 : 1;
        }
        if (valA > valB) {
            return sortDirection[column] ? 1 : -1;
        }
        return 0;
    });

    // Re-render the table with sorted data
    renderTable(globalCsvData, selectedColumns);
}
