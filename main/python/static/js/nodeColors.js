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
