document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById("workoutSessionForm");
    if (form) {
        form.addEventListener("submit", function(e) {
            const hours = parseInt(document.getElementById("hours").value) || 0;
            const minutes = parseInt(document.getElementById("minutes").value) || 0;
            const seconds = parseInt(document.getElementById("seconds").value) || 0;
            // Calculate total duration in seconds
            const totalSeconds = (hours * 3600) + (minutes * 60) + seconds;
            // Set the duration field's value to total seconds
            document.getElementById("duration").value = totalSeconds;
        });
    }
});
