import React, { useState, useEffect } from 'react'

import "../static/App.css"

import { Message } from './Message.js';
import { Socket } from './Socket';

export function MessageList() {
    const [messageList, setMessageList] = useState([]);
    
    function getNewMessages() {
        React.useEffect(() => {
            Socket.on('message recieved', (data) => {
                console.log("Received Message!: " + data['message']);
            })
        });
    }
    
    getNewMessages()
    
    return (
        <div>
            <Message username="Ameer" message="This is my message" />
        </div>
    )
}
