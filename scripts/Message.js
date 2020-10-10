import React from 'react'

import "../static/App.css"

export function Message() {
    let userName = "User Name";
    let message = "This is the message";
    let timeStamp = "10/19/20";
    return (
        <div className="message">
            <p>{userName} -- {message} -- {timeStamp}</p>
        </div>
    )
}
