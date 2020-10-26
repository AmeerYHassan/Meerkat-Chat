import React from 'react';

import '../static/App.css';

import MessageList from './MessageList';
import MessageInput from './MessageInput';

function ChatWindow() {
  return (
    <div id="idChatWindow" className="chatWindow">
      <div className="messageList">
        <MessageList />
      </div>
      <div className="userInput">
        <MessageInput />
      </div>
    </div>
  );
}

export default ChatWindow;
