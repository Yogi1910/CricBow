// player.js

// This function will render the Plotly graph using the provided graph HTML content
function renderPlotlyGraph(graphHtmlContent) {
    // Get the graph container element
    var graphContainer = document.getElementById("graph_container");
    
    // Set the graph HTML content
    graphContainer.innerHTML = graphHtmlContent;
}

// Fetch the graph HTML content from the server and render the graph
function fetchAndRenderGraph() {
    // Make an HTTP request to get the graph HTML content
    fetch('/get_graph_html')  // Replace with your Flask route for getting graph HTML
        .then(response => response.text())
        .then(graphHtmlContent => {
            // Call the function to render the Plotly graph
            renderPlotlyGraph(graphHtmlContent);
        })
        .catch(error => console.error('Error fetching graph HTML:', error));
}

// Call the function to fetch and render the graph when the page loads
window.addEventListener('load', fetchAndRenderGraph);


// This function will render the player name suggestions using the provided suggestions array
function renderSuggestions(suggestions) {
    var suggestionsContainer = document.getElementById("suggestions");
    suggestionsContainer.innerHTML = "";

    suggestions.forEach(suggestion => {
        var suggestionElement = document.createElement("div");
        suggestionElement.classList.add("suggestion");
        suggestionElement.textContent = suggestion;
        suggestionElement.addEventListener("click", function () {
            var playerSearchInput = document.getElementById("playerSearch");
            playerSearchInput.value = suggestion;
            suggestionsContainer.innerHTML = ""; // Clear suggestions after selecting
        });
        suggestionsContainer.appendChild(suggestionElement);
    });
}

// Fetch player name suggestions based on input text
function fetchPlayerNameSuggestions(inputText) {
    fetch(`/get_suggestions?input_text=${inputText}`)
        .then(response => response.json())
        .then(data => {
            renderSuggestions(data.suggestions);
        })
        .catch(error => console.error('Error fetching suggestions:', error));
}

// Call the function to fetch and render the graph when the page loads
window.addEventListener('load', fetchAndRenderGraph);

// Autocomplete suggestions as the user types
var playerSearchInput = document.getElementById("playerSearch");
playerSearchInput.addEventListener("input", function () {
    var inputText = this.value.trim();
    
    // Fetch and render player name suggestions
    if (inputText.length > 1) {
        fetchPlayerNameSuggestions(inputText);
    } else {
        var suggestionsContainer = document.getElementById("suggestions");
        suggestionsContainer.innerHTML = ""; // Clear suggestions
    }
});