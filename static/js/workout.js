document.addEventListener("DOMContentLoaded", () => {
    const videoElement = document.getElementById("video");
    const startButton = document.getElementById("start");
    const stopButton = document.getElementById("stop");

    // Timer setup
    const timerElement = document.getElementById("timer");
    let timerInterval = null; // Timer interval reference
    let secondsElapsed = 0;

    // Format time in mm:ss
    function formatTime(seconds) {
        const minutes = Math.floor(seconds / 60);
        const secondsLeft = seconds % 60;
        return `${minutes.toString().padStart(2, "0")}:${secondsLeft
            .toString()
            .padStart(2, "0")}`;
    }

    // Start the timer
    function startTimer() {
        if (!timerInterval) {
            timerInterval = setInterval(() => {
                secondsElapsed++;
                timerElement.textContent = formatTime(secondsElapsed);
            }, 1000);
        }
    }

    // Stop the timer and reset it
    function stopTimer() {
        clearInterval(timerInterval); // Stop the timer
        timerInterval = null; // Reset the interval reference
        secondsElapsed = 0; // Reset elapsed seconds
        timerElement.textContent = "00:00"; // Reset timer display
    }

    // Start the workout session
    startButton.addEventListener("click", () => {
        fetch("/start_video_feed", { method: "POST" })
            .then((response) => response.json())
            .then((data) => {
                if (data.status === "started") {
                    videoElement.src = "/video_feed"; // Set the video feed source
                    startTimer(); // Start the timer
                } else {
                    alert("Could not start the video feed. Please check your webcam.");
                }
            })
            .catch((err) => console.error("Error starting video feed:", err));
    });

    // Stop the workout session
    stopButton.addEventListener("click", () => {
        fetch("/stop_video_feed", { method: "POST" })
            .then((response) => response.json())
            .then((data) => {
                if (data.status === "stopped") {
                    videoElement.src = ""; // Clear the video feed source
                    stopTimer(); // Stop and reset the timer
                } else {
                    alert("Could not stop the video feed.");
                }
            })
            .catch((err) => console.error("Error stopping video feed:", err));
    });
});
