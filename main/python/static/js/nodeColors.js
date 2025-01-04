const palette = [
    "#fff7cd", // Light yellow
    "#fff1a8", // Soft yellow
    "#ffeb99", // Pale gold
    "#ffe680", // Pastel yellow
    "#fef9c3", // Cream
    "#fef3a5", // Warm cream
    "#fff3c6", // Soft beige
    "#ffeca2", // Light honey
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
