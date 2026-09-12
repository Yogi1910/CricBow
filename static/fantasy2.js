// $(function () {
//     // Event listener for batsman selection
//     $("#batsman-dropdown").change(function () {
//         updatePlayerImageAndStats();
//     });

//     // Event listener for bowler selection
//     $("#bowler-dropdown").change(function () {
//         updatePlayerImageAndStats();
//     });

//     // Event listener for team selection
//     $("#team-dropdown").change(function () {
//         // When the team is changed, update the batsman and bowler dropdowns
//         updateBatsmenAndBowlers();
//     });

//     // Event listener for "Generate Statistics" button
//     $("#generate-button").click(function () {
//         // Get the selected batsman and bowler values
//         var selectedBatsman = $("#batsman-dropdown").val();
//         var selectedBowler = $("#bowler-dropdown").val();
//         var selectedTeam = $("#team-dropdown").val();  // Add this line to get the selected team

//         console.log("Selected Batsman:", selectedBatsman);
//         console.log("Selected Bowler:", selectedBowler);
//         console.log("Selected Team:", selectedTeam);  // Log the selected team

//         // Send an AJAX request to the server to generate player statistics
//         $.ajax({
//             type: "POST",  // Use the appropriate HTTP method (POST or GET)
//             url: "/generate_player_stats",  // Replace with the correct server route
//             data: {
//                 batsman: selectedBatsman,
//                 bowler: selectedBowler,
//                 team: selectedTeam  // Pass the selected team to the server
//             },
//             success: function (data) {
//                 // Update the "player-stats" div with the received HTML
//                 $("#player-stats").html(data);
//             },
//             error: function () {
//                 // Handle errors if needed
//                 console.error("Error occurred during AJAX request.");
//             }
//         });
//     });

//     // Function to update batsmen and bowlers based on the selected team
//     function updateBatsmenAndBowlers() {
//         var selectedTeam = $("#team-dropdown").val();
        
//         // Send an AJAX request to the server to get updated batsmen and bowlers for the selected team
//         $.ajax({
//             type: "POST",  // Use the appropriate HTTP method (POST or GET)
//             url: "/get_batsmen_and_bowlers",  // Replace with the correct server route
//             data: { team: selectedTeam },
//             success: function (data) {
//                 // Update the batsman and bowler dropdowns with the received data
//                 updateDropdownOptions($("#batsman-dropdown"), data.batsmen);
//                 updateDropdownOptions($("#bowler-dropdown"), data.bowlers);
//             },
//             error: function () {
//                 // Handle errors if needed
//                 console.error("Error occurred during AJAX request.");
//             }
//         });
//     }

//     // Function to update dropdown options
//     function updateDropdownOptions($dropdown, options) {
//         $dropdown.empty();
//         $.each(options, function (key, value) {
//             $dropdown.append($("<option></option>")
//                 .attr("value", value)
//                 .text(value));
//         });
//     }

//     // Function to update player image and stats
//     function updatePlayerImageAndStats() {
//         var selectedBatsman = $("#batsman-dropdown").val();
//         var selectedBowler = $("#bowler-dropdown").val();

//         // Update player images
//         $("#batsman-image").attr("src", "/static/player_images/" + selectedBatsman.replace(' ', '_') + ".jpeg");
//         $("#batsman-image").attr("alt", selectedBatsman);
//         $("#bowler-image").attr("src", "/static/player_images/" + selectedBowler.replace(' ', '_') + ".jpeg");
//         $("#bowler-image").attr("alt", selectedBowler);
//     }

//     // Initial load of batsmen and bowlers
//     updateBatsmenAndBowlers();
// });
