$(document).ready(function () {
    // Handle batsman form submission
    $('.batsman-form').on('submit', function (event) {
        event.preventDefault();
        var selectedTeam3 = $('#batsmanTeamSelect').val();

        // Show the loading spinner for batsman
        $('#batsmanLoadingSpinner').show();

        $.ajax({
            type: 'POST',
            url: '/update_statistics',
            data: { team3: selectedTeam3 },
            success: function (data) {
                // Hide the loading spinner for batsman and update the batsman content
                $('#batsmanLoadingSpinner').hide();
                $('#batsmanTableContent').html(data);
            }
        });
    });

    // Handle bowler form submission
    $('.bowler-form').on('submit', function (event) {
        event.preventDefault();
        var selectedTeam4 = $('#bowlerTeamSelect').val();

        // Show the loading spinner for bowler
        $('#bowlerLoadingSpinner').show();

        $.ajax({
            type: 'POST',
            url: '/update_statistics_bowler',
            data: { team4: selectedTeam4 },
            success: function (data) {
                // Hide the loading spinner for bowler and update the bowler content
                $('#bowlerLoadingSpinner').hide();
                $('#bowlerTableContent').html(data);
            }
        });
    });
});
