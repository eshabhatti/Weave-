import React, { useState, useEffect } from "react";
import { useParams, Route } from 'react-router-dom';

export default function Post() {
    const {userName} = userParams();
    const {postId} = useParams();
    const [errorMessage, updateErrorMessage] = useState("");
    const [userdata, setUserData] = useState([]);

    const endpoint = "http://localhost:5000/post/" + postId;
    const votepoint = "http://localhost:5000/vote/"
    const savepoint = "http://localhost:5000/save/"

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
            setUserData(data);
        }).catch(err => {
            console.error(err);

        });
    }, [])

    upvote(() => {
        const body = {
            username: userName,
            type: '1',
            id: postId,
            vote: '1',
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
            
        }).catch(err => {
            console.error(err);

        }
    )

    downvote(() => {
        const body = {
            username: userName,
            type: '1',
            id: postId,
            vote: '-1',
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
            
        }).catch(err => {
            console.error(err);

        }
    )

    savePost(() => {
        const body = {
            username: userName,
            post: postId,
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

        }
    )

    const { topic_name, date_created, post_type, title, content, upvoteCount, downvoteCount, anon_flag } = userdata;

    return (
        <div className="post-container">
            <div className="post-vote-container">
                {/* replace with upvote and downvote */}
                <img src="/img/weave-icon.svg" classname="post-vote-pic" alt="" onClick={upvote()} />
                <p>{upvoteCount}</p>
                <p>{downvoteCount}</p>
                <img src="/img/weave-icon.svg" classname="post-vote-pic" alt="" onClick={downvote()}/>
            </div>
            <div className="post-content-container">
                <div className="post-text-container">
                    {/* align these better later */}
                    <p className="post-text">{userName}</p>
                    <p className="post-text">{date_created}</p>
                    <p className="post-text">{topic_name}</p>
                    <h1 className="post-title">{title}</h1>
                    <p className="post-text">{content}</p>
                    <p className="post-text" onClick={savePost()}>Save</p>
                </div>
                <div className="post-pic-container">
                    <img src="/img/weave-icon.svg" classname="post-pic" alt="" />
                </div>
            </div>
        </div>
    );
}