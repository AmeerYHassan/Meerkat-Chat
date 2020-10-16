import React, { useState, useEffect } from 'react'

import "../static/App.css"

import { Message } from './Message.js';
import { Socket } from './Socket';

export function MessageList() {
    const [messageList, setMessageList] = useState([]);
    let testMessage = <Message username="Dummy" message="This is a test" />
    
    function getNewMessages() {
        React.useEffect(() => {
            Socket.on('message recieved', (data) => {
                console.log(data);
                testMessage = <Message 
                                image={data["profilePicture"]} 
                                key={messageList.length + 1} 
                                username={data['username']} 
                                message={data['message']} 
                                botStatus={data['isBot'] ? "botMessage" : "humanMessage"}
                                hasImage = {data["hasImage"]}
                                hasLink = {data["hasLink"]}
                                imageLink = {data["imageLink"]}
                                linkText = {data["linkText"]}
                              />;
                setMessageList(messageList => [...messageList, testMessage])
            })
            
            Socket.on('message dump', (data) => {
                if (messageList.length == 0){
                    for (let i=0; i<data.length; i++){
                        console.log(data[i])
                        let currMessage = <Message 
                                            image={data[i].profilePicture}
                                            key={i} 
                                            username={data[i].username} 
                                            message={data[i].message} 
                                            botStatus={data[i].isBot ? "botMessage" : "humanMessage"} 
                                            hasImage={data[i].hasImage}
                                            hasLink={data[i].hasLink}
                                            imageLink={data[i].imageLink}
                                            linkText={data[i].linkText}
                                          />;
                        setMessageList(messageList => [...messageList, currMessage])
                    }
                }
            })
            
            return () => {
              Socket.off("message recieved");
              Socket.off("new user");
              Socket.off('message dump');
            };
        });
    }
    
    getNewMessages()
    
    return (
        <div>
            {messageList}
        </div>
    )
}
