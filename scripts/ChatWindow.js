import React from 'react'

import "../static/App.css"

import { MessageList } from './MessageList.js';
import { MessageInput } from './MessageInput.js';

export function ChatWindow() {
    return (
        <div className="chatWindow">
            <MessageList />
            <MessageInput />
        </div>
    )
}
