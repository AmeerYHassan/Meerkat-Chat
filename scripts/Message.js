import React from 'react'

import "../static/App.css"

export function Message(props) {
    return (
        <div className={props.botStatus}>
            <p><span className="message_user"> {props.username}</span>: {props.message}</p>
        </div>
    )
}
