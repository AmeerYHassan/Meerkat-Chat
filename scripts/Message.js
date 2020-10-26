import React from 'react';

import '../static/App.css';

function Message(props) {
  const {
    hasImage, hasLink, botStatus, image, username, message, linkText, imageLink,
  } = props;
  let noImageOrLink = true;

  if (hasImage || hasLink) {
    noImageOrLink = false;
  }

  return (
    <div className={botStatus}>
      <img alt="" src={image} className="profilePicture" />
      <p>
        <span className="message_user">
          {' '}
          {username}
        </span>
        :
        {' '}
        {noImageOrLink && message}
      </p>
      {hasLink && <a href={linkText}>{linkText}</a>}
      {hasImage && <img alt="" className="displayImage" src={imageLink} />}
    </div>
  );
}

export default Message;
