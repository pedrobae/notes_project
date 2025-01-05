// AUTOCOMPLETE ON SEARCH NODE
$(function() {
    $("#searchNode").autocomplete({
        source:function(request, response) {
            $.getJSON("/autocomplete", {
                q: request.term,
            }, function(data) {
                response(data.matching_results);
            });
        },
        minLength: 2,
        select: function(event, ui) {
            console.log(ui.item.value); 
        }
    });
});

// RESIZING TEXT AREAS DYNAMICALLY
function autoResizeTextArea(textarea) {
    textarea.style.height = 'auto'; // Reset height to auto to calculate correct scrollHeight
    textarea.style.height = `${textarea.scrollHeight}px`; // Set the height based on scrollHeight
}

// Function to iterate through a tables body and collect its data, used when collecting property data and edge property data
function collectTableData(tableId) {
    const table = document.getElementById(tableId);
    const data = []; // Initialize an array to hold the collected data array format data = [[property_1, value_1], [property_2, value_2]]

    if (!table) {
        console.error(`Table with ID "${tableId}" not found.`);
        return data;
    }

    const tbody = table.querySelector("tbody");

    // Iterate through each row in the tbody (Array.from creates an intermediate array from the HTMLCollection)
    Array.from(tbody.rows).forEach((row) => {
        const rowData = []; // Array to hold data for the current row

        // Iterate through each cell in the row
        Array.from(row.cells).forEach((cell) => {
            const inputElement = cell.querySelector("input, textarea"); // Find input/textarea and returns null on the delete button
            if (inputElement) {
                rowData.push(inputElement.value); // Collect the value of the input/textarea
            }
        });

        data.push(rowData); // Add row data to the main data array
    });

    return data; // Return the collected data
}

function collectEdgeData() {
    // Select all edge cards by ID
    const edgeCards = document.querySelectorAll("[id^='edgeCard']");
    // Initialize an array for resetting the activeNode.edges the expected edge data format is {label: "", name: "", type: "", properties: [["property", "value"]]}
    const edges = [];
    // Iterate through each card
    edgeCards.forEach((card) => {
        const cardData = {};
        const index = card.getAttribute('index');
        
        cardData.label = document.getElementById(`edgeLabel(${index})`).value;
        cardData.name = document.getElementById(`edgeName(${index})`).value;
        cardData.type = document.getElementById(`edgeType(${index})`).value;
        cardData.properties = collectTableData(`edgePropertiesTable(${index})`);

        edges.push(cardData);
    });
    return edges;
}
