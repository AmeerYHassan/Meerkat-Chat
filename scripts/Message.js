import React from 'react'

import "../static/App.css"

export function Message(props) {
    return (
        <div className={props.botStatus}>
            <img src={props.image} className="profilePicture"></img><p><span className="message_user"> {props.username}</span>: {props.message}</p>
        </div>
    )
}
