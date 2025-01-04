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

window.onload = function() {
    fetch("/getGraphData")
        .then(response => response.json())
        .then(data => {
            const elements = [
                ...data.nodes.map(node => ({ 
                    data: { id: node.name, label: node.label, color: getColorForLabel(node.label) },
                })),
                ...data.edges.map(edge => ({
                    data: { source: edge.source, target: edge.target, type: edge.type }
                }))
            ];

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

            cy.on('click', 'node', function (evt) {
            const node = evt.target;
            console.log('Clicked on node:', node.data());

            const form = document.createElement('form');
            form.method = 'POST';
            form.action = "/expandGraph";

            const nodeData = node.data();
            for (let key in nodeData) {
                const input = document.createElement('input');
                input.type = 'hidden';
                input.name = key;
                input.value = nodeData[key];
                form.appendChild(input);
            }

            document.body.appendChild(form);
            form.submit();
        });
    })
    .catch(error => {
        console.error('Error fetching graph data:', error);
    });
};