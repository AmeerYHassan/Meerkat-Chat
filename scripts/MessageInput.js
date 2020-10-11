import React from 'react'
import { Socket } from './Socket';

import "../static/App.css"

function handleSubmit(event) {
    let currMessage = document.getElementById("messageBox");
    Socket.emit('new message', {
       'message': currMessage.value,
    });
    
    currMessage.value = ''
    event.preventDefault();
}

export function MessageInput() {
    return (
        <div>
            <input id="messageBox" placeholder="Enter your message here..." className="messageInput" type="text" />
            <button className="submitButton" onClick={handleSubmit}>Send Message</button>
        </div>
    )
}
