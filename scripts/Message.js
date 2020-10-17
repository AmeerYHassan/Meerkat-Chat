import React from 'react'

import "../static/App.css"

export function Message(props) {
    console.log("NEW MESSAGE")
    console.log(props)
    console.log("NEW MESSAGE")
    let noImageOrLink = true
    
    if (props.hasImage || props.hasLink){
        noImageOrLink = false;
    }
    
    console.log(props.linkText);
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
