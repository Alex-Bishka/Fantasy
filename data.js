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

// Modify loadData function to take parameters for year and position
function loadData(year, position) {
    const filePath = `/Fantasy/Analysis/FantasyData/advanced-stats/${position}/${year}.csv`;
    fetch(filePath)
        .then(response => response.text())
        .then(csv => {
            const data = csvToJson(csv);
            renderTable(data);
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
function renderTable(data) {
    const container = document.getElementById('dataContainer');
    let table = '<table>';
    table += '<tr>';
    // Assuming all objects have the same keys, use the first one for column headers
    Object.keys(data[0]).forEach(key => {
        table += `<th>${key}</th>`;
    });
    table += '</tr>';
    
    data.forEach(row => {
        if (row.name) {
            table += '<tr>';
            Object.values(row).forEach(val => {
                table += `<td>${val}</td>`;
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
