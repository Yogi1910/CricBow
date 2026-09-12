$(document).ready(function() {
  
    // Function to update player image based on the selection in the dropdown
    function updatePlayerImage(playerType) {
        var playerName = $('#' + playerType).find('option:selected').text();
        var playerNameFormatted = playerName.toLowerCase().replace(' ', '_');
        $('#' + playerType + '-image').attr('src', '/static/player_images/' + playerNameFormatted + '.jpeg');
        $('#' + playerType + '-image').attr('alt', playerName);
    }

    // Event listeners for the dropdowns to update player images dynamically
    $('#bowler').on('change', function() {
        updatePlayerImage('bowler');
    });

    $('#striker').on('change', function() {
        updatePlayerImage('striker');
    });

    // AJAX call to fetch player statistics on form submission
    $('#player-form').on('submit', function(e) {
        e.preventDefault();
    
        $.ajax({
            url: '/run-function',
            method: 'POST',
            data: $(this).serialize(),
            success: function(response) {
                $('#stats-table').html(response);
                $('#stats-table').find('table').addClass('table1'); // Add this line to apply styles to your table
            },
            error: function(jqXHR, textStatus, errorThrown) {
                console.error("AJAX error: " + textStatus + ' : ' + errorThrown);
            }
        });
    });
    
    // AJAX call for team-player stats
    $('#team-player-form').on('submit', function(e) {
        e.preventDefault();
        
        $.ajax({
            url: '/run-team-player-function',
            method: 'POST',
            data: $(this).serialize(),
            success: function(response) {
                $('#team-player-stats-table').html(response);
                $('#team-player-stats-table').find('table').addClass('table1'); // Add this line to apply styles to your table
            },
            error: function(jqXHR, textStatus, errorThrown) {
                console.error("AJAX error: " + textStatus + ' : ' + errorThrown);
            }
        });
    });

    // Initial call to populate the table with default players' stats
    $('#player-form').trigger('submit');
    updatePlayerImage('bowler');
    updatePlayerImage('striker');
});

function updateImageSrc(id, folder, formatter = name => name) {
    const name = $(`#${id}`).find('option:selected').text();
    const formattedName = formatter(name);
    $(`#${id}-image`).attr('src', `/static/${folder}/${formattedName}.jpeg`);
    $(`#${id}-image`).attr('alt', name);
}

$(document).ready(function() {
    $('#team1').on('change', function() {
        updateImageSrc('team1', 'team_logo', name => name);
    });

    $('#player2').on('change', function() {
        updateImageSrc('player2', 'player_images', name => name.replace(/ /g, '_').replace(/\./g, '').toLowerCase());
    });

    // Your existing code...
});
