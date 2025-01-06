document.addEventListener("DOMContentLoaded", () => {
    const propertiesBody = document.getElementById("propertiesBody");
    const edgesContainer = document.getElementById("edgesContainer");
    const addPropertyBtn = document.getElementById("addPropertyBtn");
    const addEdgeBtn = document.getElementById("addEdgeBtn");

    // Mock data
    const activeNode = {
        label: "",
        name: "",
        properties: [],
        edges: []
    };

    // Populate form with node data
    function populateForm() {
        console.log("Active Node Data:\n", activeNode);
        document.getElementById("label").value = activeNode.label;
        document.getElementById("name").value = activeNode.name;

        // Populate properties
        propertiesBody.innerHTML = "";
        activeNode.properties.forEach((propTuple, propIndex) => {
            propertiesBody.innerHTML += `
                <tr>
                    <td><input type="text" class="form-control" placeholder="Property"
                               value="${propTuple[0]}" /></td>
                    <td><textarea class="form-control" 
                                  placeholder="Value">${propTuple[1]}</textarea></td>
                    <td><button class="btn btn-danger btn-sm" onclick="deleteProperty(${propIndex})">
                        <i class="fa fa-trash"></i>
                    </button></td>
                </tr>
            `;
        });

        // Populate edges
        edgesContainer.innerHTML = "";
        activeNode.edges.forEach((edgeData, edgeIndex) => {
            edgesContainer.innerHTML += `
                <div class="card my-3" id="edgeCard(${edgeIndex})" index="${edgeIndex}">
                    <div class="card-header d-flex justify-content-between align-items-center">
                        <input type="text" class="form-control me-3" id=edgeType(${edgeIndex})
                               value="${edgeData.type}" placeholder="Type" />
                        <button class="btn btn-danger btn-sm" onclick="deleteEdge(${edgeIndex})">
                            <i class="fa fa-trash"></i>
                        </button>
                    </div>
                    <div class="card-body">
                        <div class="row g-2">
                            <div class="col-md-6">
                                <input type="text" class="form-control" id=edgeLabel(${edgeIndex})
                                       value="${edgeData.label}" placeholder="Edge Label" />
                            </div>
                            <div class="col-md-6">
                                <input type="text" class="form-control" id=edgeName(${edgeIndex})
                                       value="${edgeData.name}" placeholder="Edge Name" />
                            </div>
                        </div>
                        <div class="d-flex justify-content-between align-items-center">
                            <h6 class="mb-0">Edge Properties</h6>
                            <button class="btn btn-primary btn-sm" 
                                    onclick="addEdgeProperty(${edgeIndex})">Add Edge Property</button>
                        </div>
                        
                        <table class="table table-bordered table-sm mt-3" id="edgePropertiesTable(${edgeIndex})">
                            <tbody id="edgeProperties_${edgeIndex}">
                                ${edgeData.properties
                                    .map((edgePropTuple, edgePropIndex) => `
                                        <tr>
                                            <td><input type="text" class="form-control" 
                                                       value="${edgePropTuple[0]}" placeholder="Edge Property"/></td>
                                            <td><textarea class="form-control" 
                                                          placeholder="Edge Property Value">${edgePropTuple[1]}</textarea></td>
                                            <td><button class="btn btn-danger btn-sm" onclick="deleteEdgeProperty(${edgeIndex}, ${edgePropIndex})">
                                                <i class="fa fa-trash"></i>
                                            </button></td>
                                        </tr>
                                    `).join("")}
                            </tbody>
                        </table>
                    </div>
                </div>
            `;
        });

        const textareas = document.querySelectorAll('textarea');
        textareas.forEach((textarea) => {
            // Adjust height on page load for pre-filled content
            autoResizeTextArea(textarea);

            // Add event listener to resize as user types
            textarea.addEventListener('input', () => autoResizeTextArea(textarea));
        });
    }

    // Collect form data and update active node
    function collectData() {
        const edges = collectEdgeData();

        activeNode.name = document.getElementById("name").value;
        activeNode.label = document.getElementById("label").value;
        activeNode.properties = collectTableData("propertiesTable");
        activeNode.edges = edges
    };

    // Add property
    addPropertyBtn.addEventListener("click", () => {
        collectData();
        activeNode.properties.push(["", ""]);
        populateForm();
    });

    // Add edge
    addEdgeBtn.addEventListener("click", () => {
        collectData();
        activeNode.edges.push({ type: "", label: "", name: "", properties: [] });
        populateForm();
    });

    // Add edge property
    window.addEdgeProperty = function (edgeIndex) {
        collectData();
        activeNode.edges[edgeIndex].properties.push(["", ""]);
        populateForm();
    };

    // Delete property
    window.deleteProperty = function (index) {
        collectData();
        activeNode.properties.splice(index, 1);
        populateForm();
    };

    // Delete edge
    window.deleteEdge = function (index) {
        collectData();
        activeNode.edges.splice(index, 1);
        populateForm();
    };

    // Delete edge property
    window.deleteEdgeProperty = function (edgeIndex, propIndex) {
        collectData();
        activeNode.edges[edgeIndex].properties.splice(propIndex, 1);
        populateForm();
    };

    // Initial population
    populateForm();
});

function sendData() {
    const formData = collectData()
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