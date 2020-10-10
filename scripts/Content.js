import React from 'react'

import "../static/App.css"

import { ChatWindow } from './ChatWindow.js';
import { SidePanel } from './SidePanel.js';

export function Content() {
    return (
        <div className="container">
            <SidePanel />
            <ChatWindow />
        </div>
    )
}
