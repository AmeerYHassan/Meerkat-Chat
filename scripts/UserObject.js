import React from 'react'

import "../static/App.css"

export function UserObject(props) {
    return (
        <div className="UserObject">
            <img src={props.profilePicture} />
            <p>{props.username}</p>
        </div>
    )
}
