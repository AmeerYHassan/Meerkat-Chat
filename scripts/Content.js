import React from 'react';

import '../static/App.css';

import ChatWindow from './ChatWindow';
import SidePanel from './SidePanel';

function Content() {
  return (
    <div className="container">
      <SidePanel />
      <ChatWindow />
    </div>
  );
}

export default Content;
