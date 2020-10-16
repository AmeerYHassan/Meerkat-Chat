import React, { useState } from 'react'

import "../static/App.css"
import { Socket } from './Socket';
import { GoogleLogin } from 'react-google-login';

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
    
    const responseGoogle = (response) => {
        console.log(response);
        console.log(response.profileObj.googleId)
        Socket.emit('user login', {
            'id': response.profileObj.googleId,
            'name': response.profileObj.name,
            'image': response.profileObj.imageUrl
        });
    }
    
    return (
        <div className="sidePanel">
            <h1> Meerkat Chat! </h1>
              <GoogleLogin
                clientId="881732433179-jr7i2r1pnm1ks26cq6o59elir11g74s6.apps.googleusercontent.com"
                buttonText="Login"
                onSuccess={responseGoogle}
                onFailure={responseGoogle}
                cookiePolicy={'single_host_origin'}
              />
            <hr />
            <p> User Count: {userCount} </p>
        </div>
    )
}
