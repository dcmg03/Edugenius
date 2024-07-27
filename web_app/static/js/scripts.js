document.addEventListener("DOMContentLoaded", function() {
    var loader = document.getElementById("loader");
    var content = document.getElementById("content");
    var loadingPercentage = document.getElementById("loading-percentage");

    function updateLoadingPercentage(percentage) {
        loadingPercentage.innerText = `${percentage}%`;
    }

    var socket = io.connect('http://' + document.domain + ':' + location.port);

    socket.on('progress', function(data) {
        updateLoadingPercentage(data.progress);
    });

    fetch('/load_content')
        .then(response => response.json())
        .then(data => {
            loader.style.display = "none";
            content.style.display = "block";
            updateLoadingPercentage(100); // Asegúrate de mostrar 100% al final
        });
});
