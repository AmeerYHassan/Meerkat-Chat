import React from 'react'
import { Socket } from './Socket';

import { Message } from './Message.js';
import { MessageList } from './MessageList.js';

import "../static/App.css"

function handleSubmit(event) {
    let currMessage = document.getElementById("messageBox");
    let currMessageValue = currMessage.value;
    Socket.emit('new message', {
        'message': currMessageValue,
    });
    
    currMessage.value = '';
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
