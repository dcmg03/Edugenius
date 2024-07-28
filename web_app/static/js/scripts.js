document.addEventListener("DOMContentLoaded", function() {
    const socket = io();

    socket.on('update_progress', function(data) {
        const loader = document.getElementById("loader");
        const content = document.getElementById("content");
        const percentage = document.getElementById("loading-percentage");

        if (data.progress < 100) {
            loader.style.display = "block";
            content.style.display = "none";
            percentage.innerText = `${data.progress.toFixed(2)}%`;
        } else {
            loader.style.display = "none";
            content.style.display = "block";
        }
    });
});
