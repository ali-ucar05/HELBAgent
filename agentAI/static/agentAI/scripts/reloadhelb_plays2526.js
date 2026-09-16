$(document).ready(function() {
    // la même chose que les agents.
    function reloadDiscussion() {
        let url = $("#discussion-chat").data("url");

        $.get(url, function(data) {
            console.log(data);
            let html = "";
            let lines = data.trim().split('\n');

            lines.forEach(line => {
                let parts = line.split(':');
                if (parts.length >= 3) {
                    let userName = parts[0];
                    let message = parts.slice(1, -1).join(':');

                    if (userName !== 'ali') {
                        html += `
                        <div class="d-flex justify-content-start mb-4">
                            <div class="chat-bubble other-bubble shadow-sm">
                                <strong>${userName}</strong><br>
                                ${message}
                            </div>
                        </div>`;
                    } else {
                        html += `
                        <div class="d-flex justify-content-end mb-4">
                            <div class="chat-bubble user-bubble shadow-sm">
                                <strong>${userName}</strong><br>
                                ${message}
                            </div>
                        </div>`;
                    }
                }
            });

            $("#discussion-chat").html(html);
        });
    }

    // permet d'actualiser l'image avec le temps actuel
    function reloadFrameImage() {
        $("#frame-image").attr("src","https://helbplays2526.alwaysdata.net/frame.jpg?" + new Date().getTime());
    }

    setInterval(reloadDiscussion, 1000);
    setInterval(reloadFrameImage, 1000);
    reloadDiscussion();
});