$(document).ready(function() {
    function reloadDiscussion() {
        // on va recuperer le l'url qui permet d'envoyer la discussion de l'agent 
        let url = $("#discussion-chat").data("url");
        let profileUrl = $("#discussion-chat").data("profile-url");
 
        // on fait un get pour recuper la discussion et l'afficher si une discussion est presente sinon non messages apparait.
        $.get(url, function(data) { 
            let html = ""; 

            if(data.length === 0)
            {
                html = '<p>No messages<p>';
            }
            else
            {
                data.forEach(function(item) { 
                    let userLink = ''
     
                    if(item.is_current_user) {
                        userLink = `<a href="${profileUrl}" class="font-weight-bold text-white text-decoration-none">${item.user_name}</a>`;  
                    } else {
                        userLink = `<a href="/user/${item.user_name}/" class="font-weight-bold text-white text-decoration-none">${item.user_name}</a>`; 
                    }
     
                    html += ` 
                        <div class="d-flex justify-content-end mb-5"> 
                            <div class="chat-bubble user-bubble shadow-sm p-4"> 
                                <div class="d-flex align-items-center mb-2"> 
                                    <img src="${item.user_image}" class="rounded-circle mr-3" width="45" height="45"> 
                                    ${userLink} 
                                </div> 
                                <p class="mb-0">${item.prompt}</p> 
                            </div> 
                        </div> 
     
                        <div class="d-flex justify-content-start mb-5"> 
                            <div class="chat-bubble ai-bubble shadow-sm p-4"> 
                                <div class="d-flex align-items-center mb-2"> 
                                    <img src="${item.agent_image}" class="rounded-circle mr-3" width="45" height="45"> 
                                    <strong>${item.agent_name}</strong> 
                                </div> 
                                <p class="mb-0">${item.answer}</p> 
                            </div> 
                        </div> 
                    `; 
                });
            }

            $("#discussion-chat").html(html); 
        });
    } 
 
    setInterval(reloadDiscussion, 3000); 
    reloadDiscussion(); 
    });