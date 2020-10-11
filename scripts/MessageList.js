import React from 'react'

import "../static/App.css"

import { Message } from './Message.js';

export function MessageList() {
    return (
        <div>
            <Message username="Ameer" message="This is my message" />
        </div>
    )
}
