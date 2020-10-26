import React from 'react';

import '../static/App.css';

function UserObject({ profilePicture, username }) {
  return (
    <div className="UserObject">
      <img alt="" src={profilePicture} />
      <p>{username}</p>
    </div>
  );
}

export default UserObject;
