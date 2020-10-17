import React, { useState, useEffect } from 'react'

import { Socket } from './Socket';
import { Message } from './Message.js';
import { MessageList } from './MessageList.js';

import "../static/App.css"

let chatLock = "disabled"

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
    const [chatLock, setChatLock] = useState(true);
    
    function unlockChat() {
        React.useEffect(() => {
            Socket.on('unlock chat', (data) => {
                setChatLock(false);
            })

            return () => {
              Socket.off("user login");
            };
        });
    }
    
    unlockChat();
    return (
        <div>
            <form onSubmit={handleSubmit}>
                <input disabled={chatLock} id="messageBox" placeholder="Enter your message here..." className="messageInput" type="text" />
            </form>
            <button disabled={chatLock} className="submitButton" onClick={handleSubmit}>Send Message</button>
        </div>
    )
}
