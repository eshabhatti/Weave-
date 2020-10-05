import React, { useState, useEffect } from "react";

import "./post.css";

export default function Post({
    postId, userName
}) {

    const [errorMessage, updateErrorMessage] = useState("");
    const [postdata, setPostData] = useState([]);
    const [saveCheck, setSaved] = useState(0);
    const [voteCheck, setVoted] = useState(0);
    
    const access_token = localStorage.getItem('access_token');
	if (access_token == null) {
		window.location = "/login"
	}

    const endpoint = "http://localhost:5000/post/" + postId;
    const votepoint = "http://localhost:5000/vote/"
    const savepoint = "http://localhost:5000/save/"
    const statepoint = "http://localhost:5000/poststates/"

    useEffect(() => {
        fetch(endpoint, {
            method: "GET",
            headers: {
                'Content-Type': 'application/json',
				'Authorization': 'Bearer ' + access_token
            },
        }).then(response => response.json()).then(data => {
            if (data.error_message) {
                updateErrorMessage(data.error_message);
				window.location = "/404"
            }
			/* catches jwt errors that don't use the form "error_message:" */
			if (data.msg) {
				window.location = "/login"
			}
            setPostData(data);
        }).catch(err => {
            console.error(err);

        });

        const body = {
            username: userName,
            post_id: postId,
        }

        fetch(statepoint, {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
				'Authorization': 'Bearer ' + access_token
            },
            body: JSON.stringify(body)
        }).then(response => response.json()).then(data => {
            if (data.error_message) {
                updateErrorMessage(data.error_message);
				window.location = "/404"
            }
			/* catches jwt errors that don't use the form "error_message:" */
			if (data.msg) {
				window.location = "/login"
			}
            /* setStateData(data); */
            const { saved, voted } = data;
            setSaved(saved);
            setVoted(voted);
        }).catch(err => {
            console.error(err);
            alert(err);

        });
    }, [])

    {/*useEffect(() => {
        
    }, [saveCount, voteCount])*/}

    

    const { topic_name, date_created, post_type, title, content, upvoteCount, downvoteCount, anon_flag } = postdata;
    {/*const { saved, voted } = statedata;*/}

    const vote = (value) => {
        const body = {
            username: userName,
            type: '1',
            id: postId,
            vote: value,
        }
        fetch(votepoint, {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
				'Authorization': 'Bearer ' + access_token
            },
            body: JSON.stringify(body)
        }).then(response => response.json()).then(data => {
            if (data.error_message) {
                updateErrorMessage(data.error_message);
				window.location = "/404"
            }
			/* catches jwt errors that don't use the form "error_message:" */
			if (data.msg) {
				window.location = "/login"
            }
            setVoted(value);
        }).catch(err => {
            console.error(err);

        });
    };

    const savePost = (value) => {
        setSaved(value);
        const body = {
            username: userName,
            post: postId,
            type: value,
        }
        fetch(savepoint, {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
				'Authorization': 'Bearer ' + access_token
            },
            body: JSON.stringify(body)
        }).then(response => response.json()).then(data => {
            if (data.error_message) {
                updateErrorMessage(data.error_message);
                window.location = "/404"
            }
			/* catches jwt errors that don't use the form "error_message:" */
			if (data.msg) {
				window.location = "/login"
            }
        }).catch(err => {
            console.error(err);

        });
    };
    

    return (
        <div>
            <div className="post-content-container">
                <div className="post-vote-container">
                    {/* replace with upvote and downvote */}
                    {voteCheck > 0 ? (
                        <button>Un<img src="/img/weave-icon.svg" className="post-vote-pic" alt="" onClick={() => vote(0)} /></button>
                    
                    ) : (
                        <button>U<img src="/img/weave-icon.svg" className="post-vote-pic" alt="" onClick={() => vote(1)} /></button>
                    )}
                    <p>{upvoteCount}</p>
                    <p>{downvoteCount}</p>
                    {voteCheck < 0 ? (
                        <button>Dn<img src="/img/weave-icon.svg" className="post-vote-pic" alt="" onClick={() => vote(0)} /></button>
                    ) : (
                        <button>D<img src="/img/weave-icon.svg" className="post-vote-pic" alt="" onClick={() => vote(-1)} /></button>
                    )}
                </div>
                <div className="post-text-container">
                    {/* align these better later */}
                    <p className="post-text">Creator</p>
                    <p className="post-text">{date_created}</p>
                    <p className="post-text">{topic_name}</p>
                    <h1 className="post-title">{title}</h1>
                    <p className="post-text">{content}</p>
                    <h1>{saveCheck}</h1>
                    {saveCheck === -1 ? (
                        <button className="post-save-button" onClick={() => savePost(1)}>Save</button>
                    ) : (
                        <button className="post-save-button" onClick={() => savePost(-1)}>Unsave</button>
                    )}
                </div>
                <div className="post-pic-container">
                    <img src="/img/weave-icon.svg" classname="post-pic" alt="" />
                </div>
            </div>
        </div>
    );
}