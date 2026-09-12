// Function to redirect to the team.html page with the selected team's name
function redirectToTeam(teamName) {
    window.location.href = '/team?team_name=' + encodeURIComponent(teamName);
}

document.addEventListener('DOMContentLoaded', function () {
    const teamButtons = document.querySelectorAll('.team-button');

    // Retrieve the selected team from localStorage if available
    const selectedTeam = localStorage.getItem('selectedTeam');

    // Apply the "selected" class based on the stored value
    if (selectedTeam) {
        teamButtons.forEach(button => {
            if (button.textContent === selectedTeam) {
                button.classList.add('selected');
            }
        });
    }

    teamButtons.forEach(button => {
        button.addEventListener('click', function () {
            const teamName = button.textContent;

            // Remove the "selected" class from all buttons
            teamButtons.forEach(btn => {
                btn.classList.remove('selected');
            });

            // Add the "selected" class to the clicked button
            button.classList.add('selected');

            // Store the selected team in localStorage
            localStorage.setItem('selectedTeam', teamName);

            redirectToTeam(teamName);
        });
    });
});
