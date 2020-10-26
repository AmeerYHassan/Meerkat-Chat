import React, { useState } from 'react';

import '../static/App.css';
import { GoogleLogin } from 'react-google-login';
import UserObject from './UserObject.js';
import { Socket } from './Socket';

function SidePanel() {
  const [userList, setUserList] = useState([]);
  const clientID = '881732433179-jr7i2r1pnm1ks26cq6o59elir11g74s6.apps.googleusercontent.com';

  function getUserList() {
    React.useEffect(() => {
      Socket.on('user update', (data) => {
        const updatedList = [];
        for (let i = 0; i < data.length; i += 1) {
          const currUser = (
            <UserObject
              key={i}
              profilePicture={data[i].profilePicture}
              username={data[i].username}
            />
          );
          updatedList.push(currUser);
        }
        setUserList(updatedList);
      });
      return () => {
        Socket.off('user update');
      };
    });
  }

  const responseGoogle = (response) => {
    Socket.emit('user login', {
      id: response.profileObj.googleId,
      name: response.profileObj.name,
      image: response.profileObj.imageUrl,
    });
  };

  getUserList();

  return (
    <div className="sidePanel">
      <h1> Meerkat Chat! </h1>
      <hr />
      <p> In order to chat, please login with your google account! </p>
      <hr />
      <GoogleLogin
        clientId={clientID}
        buttonText="Login"
        onSuccess={responseGoogle}
        onFailure={responseGoogle}
        cookiePolicy="single_host_origin"
        id="googleButton"
      />
      <hr />
      <p>
        Users Online:
        {userList.length}
      </p>
      {userList}
    </div>
  );
}

export default SidePanel;
