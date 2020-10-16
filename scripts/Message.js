import React from 'react'

import "../static/App.css"

export function Message(props) {
    console.log(props)
    return (
        <div className={props.botStatus}>
            <img src={props.image} className="profilePicture"></img>
            <p>
                <span className="message_user"> {props.username}</span>
                : {props.message}
            </p>
            {props.hasLink && <a href={props.linkText}>{props.linkText}</a>}
            {props.hasImage && <img href={props.imageLink}></img>}
        </div>
    )
}
