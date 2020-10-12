import React, { useState, useEffect } from 'react'

import "../static/App.css"

import { Message } from './Message.js';
import { Socket } from './Socket';

export function MessageList() {
    const [messageList, setMessageList] = useState([]);
    let testMessage = <Message username="Dummy" message="This is a test" />
    
    function getNewMessages() {
        React.useEffect(() => {
            Socket.on('message recieved', (data) => {
                console.log("Received Message!: " + data['message']);
                testMessage = <Message key={messageList.length + 1} username={data['username']} message={data['message']} botStatus={data['isBot'] ? "botMessage" : "humanMessage"} />;
                setMessageList([...messageList, testMessage]);
            })
            
            return () => {
              Socket.off("message recieved");
              Socket.off("new user");
            };
        });
    }
    
    getNewMessages()
    
    return (
        <div>
            {messageList}
        </div>
    )
}
