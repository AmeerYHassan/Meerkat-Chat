import React, { useState } from 'react'

import "../static/App.css"
import { Socket } from './Socket';

export function SidePanel() {
    const [userCount, setUserCount] = useState(0);

    function getNewCount() {
        React.useEffect(() => {
            Socket.on('user count change', (data) => {
                setUserCount(userCount + data["changeBy"])
            })
            
            return () => {
              Socket.off("user count change");
            };
        });
    }
    
    getNewCount()
    
    return (
        <div className="sidePanel">
            <h1> Meerkat Chat! </h1>
            <hr />
            <p> User Count: {userCount} </p>
        </div>
    )
}
