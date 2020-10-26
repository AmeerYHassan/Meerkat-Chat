import React, { useState } from 'react';

import { Socket } from './Socket';

import '../static/App.css';

function handleSubmit(event) {
  const currMessage = document.getElementById('messageBox');
  const currMessageValue = currMessage.value;
  Socket.emit('new message', {
    message: currMessageValue,
  });

  currMessage.value = '';
  event.preventDefault();
}

function MessageInput() {
  const [chatLock, setChatLock] = useState(true);

  function unlockChat() {
    React.useEffect(() => {
      Socket.on('unlock chat', () => {
        setChatLock(false);
      });

      return () => {
        Socket.off('user login');
      };
    });
  }

  unlockChat();
  return (
    <div>
      <form onSubmit={handleSubmit}>
        <input disabled={chatLock} id="messageBox" placeholder="Enter your message here..." className="messageInput" type="text" />
      </form>
      <button type="submit" disabled={chatLock} className="submitButton" onClick={handleSubmit}>Send Message</button>
    </div>
  );
}

export default MessageInput;
