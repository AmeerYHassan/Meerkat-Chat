import React from 'react'

import "../static/App.css"

export function Message(props) {
    let userName = "User Name";
    let message = "This is the message";
    let timeStamp = "10/19/20";
    return (
        <div className="message">
            <p><span class="message_user"> {props.username}</span>: {props.message}</p>
        </div>
    )
}
