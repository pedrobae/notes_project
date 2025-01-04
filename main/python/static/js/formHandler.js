function collectFormData() {
    const formData = {};

    // Collect node data
    formData.label = document.getElementById("label").value;
    formData.name = document.getElementById("name").value;

    // Collect properties
    formData.properties = [];
    document.querySelectorAll("input[id^='property_']").forEach((input) => {
        const id = input.id.split("_")[1]; // Extract property index
        const valueInput = document.getElementById(`property_${id}_value`);
        if (valueInput) {
            formData.properties.push({
                key: input.value,
                value: valueInput.value,
            });
        }
    });

    // Collect edges
    formData.edges = [];
    document.querySelectorAll("input[name='edgeNodeLabel']").forEach((labelInput, index) => {
        const nameInput = document.querySelectorAll("input[name='edgeNode']")[index];
        const edge = {
            label: labelInput.value,
            name: nameInput.value,
            properties: [],
        };

        // Collect edge properties
        document.querySelectorAll(`input[id^='edgeProperty_${index}_']`).forEach((propInput) => {
            const id = propInput.id.split("_")[2]; // Extract edge property index
            const propValueInput = document.getElementById(`edgeProperty_${index}_${id}_value`);
            if (propValueInput) {
                edge.properties.push({
                    key: propInput.value,
                    value: propValueInput.value,
                });
            }
        });

        // Collect edge type
        const edgeTypeInput = document.getElementById(`edgeType_${index}`)
        edge.properties.push({
            key: 'type',
            value: edgeTypeInput.value,
        })

        formData.edges.push(edge);
    });

    console.log("Collected Form Data:", formData);

    // Sending this data via AJAX to Flask
    fetch("/saveNode", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
    })
        .then((response) => response.json())
        .then((data) => {
            console.log("Response from server:", data);
            alert("Data saved successfully!");
        })
        .catch((error) => {
            console.error("Error saving data:", error);
            alert("Failed to save data.");
        });
}