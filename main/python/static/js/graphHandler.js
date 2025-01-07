const palette = [
    "#fff7cd", // Light yellow
    "#ffd95a", // Golden yellow 
    "#ffc83f", // Rich gold 
    "#ffb347", // Deep honey 
    "#d4a017", // Mustard yellow 
];


const labelColorMap = {};
let colorIndex = 0;

// Function to get or assign a color for a label
function getColorForLabel(label) {
    if (!labelColorMap[label]) {
        labelColorMap[label] = palette[colorIndex];
        colorIndex = (colorIndex + 1) % palette.length; // Loop through the palette
    }
    console.log(labelColorMap)
    return labelColorMap[label];
}


let cy;

const graphData = {
    nodes: [{
        name: '',
        label: ''
    }],
    edges: [{
        source: '',
        target: '',
        type: ''
    }]

}

function getGraphData() {
    fetch('/getGraphData', {
        method: 'GET'
    })
        .then((response) =>response.json())
        .then((data) => {
            console.log('Response from getGraphData:', data);
            if (data.success) {
                graphData.nodes = data.graphData.nodes
                graphData.edges = data.graphData.edges
                populateGraph();
            } else {
                alert("Failed to get Graph Data.");
            }
        });
};

function populateGraph() {
    console.log('Populating Graph:', graphData);

    const elements = [
        ...graphData.nodes.map(node => ({ 
            data: { id: node.name, label: node.label, color: getColorForLabel(node.label) },
        })),
        ...graphData.edges.map(edge => ({
            data: { source: edge.source, target: edge.target, type: edge.type }
        }))
    ];

    console.log('Mapped Graph Elements: ', elements)

    cy = cytoscape({
        container: document.getElementById('cy'),
        elements: elements,
        style: [
            {
                selector: 'node',
                style: {
                    'content': 'data(id)',
                    'background-color': 'data(color)', 
                    'border-width': '2px',
                    'border-color': '#e2c79d', 
                    'font-size': '14px',
                    'font-family': 'Georgia, serif', 
                }
            },
            {
                selector: 'edge',
                style: {
                    'content': 'data(type)',
                    'line-color': '#ccc', 
                    'width': 2,
                    'line-style': 'dashed', 
                    'line-dash-pattern': '5 5',
                    'font-size': '12px',
                    'font-family': 'Courier New, Courier, monospace', 
                    'color': '#4e4b3e'
                }
            }
        ],
        layout: {
            name: 'cose',
            animate: true,
            animationDuration: 800
        }
    });

    cy.on('click', 'node', function (event) {
        const node = event.target;
        console.log('Clicked on node:', node.data());

        fetch('/expandGraph', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(node.data())
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                graphData.nodes = data.graphData.nodes
                graphData.edges = data.graphData.edges
                populateGraph();
            } else {
                alert("Failed to get Graph Data.");
            }
        })
    });
};