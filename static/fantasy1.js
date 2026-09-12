// stadium analyze

document.addEventListener("DOMContentLoaded", function () {
  const buttons = document.querySelectorAll(".stadium-button");
  const summaryContainer = document.getElementById("summary-container");

  buttons.forEach(button => {
      button.addEventListener("click", function () {
          const stadiumName = button.getAttribute("data-stadium");
          
          // Make an AJAX request to update the summary
          fetch(`/update-summary?stadium=${encodeURIComponent(stadiumName)}`)
              .then(response => response.text())
              .then(updatedSummary => {
                  // Update the summary container with the new content
                  summaryContainer.innerHTML = updatedSummary;
              })
              .catch(error => {
                  console.error('Error fetching updated summary:', error);
              });
      });
  });
});
