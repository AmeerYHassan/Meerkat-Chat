import React from 'react'

import "../static/App.css"

import { MessageList } from './MessageList.js';
import { MessageInput } from './MessageInput.js';

export function ChatWindow() {
    return (
        <div id="idChatWindow" className="chatWindow">
            <div className="messageList">
                <MessageList />
            </div>
            <div className="userInput">
                <MessageInput />
            </div>
        </div>
    )
}