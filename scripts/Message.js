import React from 'react'

import "../static/App.css"

export function Message(props) {
    let noImageOrLink = true
    
    if (props.hasImage || props.hasLink){
        noImageOrLink = false;
    }
    
    return (
        <div className={props.botStatus}>
            <img src={props.image} className="profilePicture"></img>
            <p>
                <span className="message_user"> {props.username}</span>
                : {noImageOrLink && props.message}
            </p>
            {props.hasLink && <a href={props.linkText}>{props.linkText}</a>}
            {props.hasImage && <img className="displayImage" src={props.imageLink}></img>}
        </div>
    )
}
