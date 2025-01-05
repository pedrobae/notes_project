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
        document.getElementById("label").value = activeNode.label;
        document.getElementById("name").value = activeNode.name;

        // Populate properties
        propertiesBody.innerHTML = "";
        activeNode.properties.forEach((propTuple, propIndex) => {
            propertiesBody.innerHTML += `
                <tr>
                    <td><input type="text" class="form-control" 
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
                <div class="card my-3" id="edge_${edgeIndex}">
                    <div class="card-header d-flex justify-content-between align-items-center">
                        <input type="text" class="form-control me-3" 
                               value="${edgeData.type}" placeholder="Type" />
                        <button class="btn btn-danger btn-sm" onclick="deleteEdge(${edgeIndex})">
                            <i class="fa fa-trash"></i>
                        </button>
                    </div>
                    <div class="card-body">
                        <div class="row g-2">
                            <div class="col-md-6">
                                <input type="text" class="form-control" 
                                       value="${edgeData.label}" placeholder="Edge Label" />
                            </div>
                            <div class="col-md-6">
                                <input type="text" class="form-control" 
                                       value="${edgeData.name}" placeholder="Edge Name" />
                            </div>
                        </div>
                        <div class="d-flex justify-content-between align-items-center">
                            <h6 class="mb-0">Edge Properties</h6>
                            <button class="btn btn-primary btn-sm" 
                                    onclick="addEdgeProperty(${edgeIndex})">Add Edge Property</button>
                        </div>
                        
                        <table class="table table-bordered table-sm mt-3">
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

    // Add property
    addPropertyBtn.addEventListener("click", () => {
        activeNode.properties.push(["", ""]);
        populateForm();
    });

    // Add edge
    addEdgeBtn.addEventListener("click", () => {
        activeNode.edges.push({ type: "", label: "", name: "", properties: [] });
        populateForm();
    });

    // Add edge property
    window.addEdgeProperty = function (edgeIndex) {
        activeNode.edges[edgeIndex].properties.push(["", ""]);
        populateForm();
    };

    // Delete property
    window.deleteProperty = function (index) {
        activeNode.properties.splice(index, 1);
        populateForm();
    };

    // Delete edge
    window.deleteEdge = function (index) {
        activeNode.edges.splice(index, 1);
        populateForm();
    };

    // Delete edge property
    window.deleteEdgeProperty = function (edgeIndex, propIndex) {
        activeNode.edges[edgeIndex].properties.splice(propIndex, 1);
        populateForm();
    };

    // Initial population
    populateForm();
});