import React, { useState, useEffect } from "react";
import Collapsible from 'react-collapsible';

import "./post.css";

export default function Post({
    postId, userName
}) {

    const [errorMessage, updateErrorMessage] = useState("");
    const [postdata, setPostData] = useState([]);
    {/* keeps track if user has saved or voted */ }
    const [saveCheck, setSaved] = useState(0);
    const [voteCheck, setVoted] = useState(0);
    {/* current score of post */ }
    const [votes, setVotes] = useState(0);

	
    const access_token = localStorage.getItem('access_token');
    if (access_token == null) {
        window.location = "/login"
    }

    const endpoint = "http://localhost:5000/post/" + postId;
    const votepoint = "http://localhost:5000/vote/"
    const savepoint = "http://localhost:5000/save/"
    const statepoint = "http://localhost:5000/poststates/"

    {/* renders the post with fetch data and the states of the save and voting buttons */ }
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
            const { score } = data;
            setVotes(score);
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

    const { topic_name, date_created, post_type, pic_path, title, content, creator } = postdata;

    {/* sends the votes to the server and receives the change in score */ }
    const vote = (value) => {
        setVoted(value);
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
            const { change } = data;
            setVotes(votes + change);
        }).catch(err => {
            console.error(err);

        });
    };

    {/* sends the saved/unsaved postId to the server */ }
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
	
	const postLink = "/post/" + postId;
	const profileLink = "/profile/" + creator;
	const topicLink = "/topic/" + topic_name;
	
    return (
        <div>
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css"></link>
            <Collapsible className="post-content-header" openedClassName="post-content-header-open" triggerClassName="post-trigger" triggerOpenedClassName="post-trigger-open" trigger={title}>
                <div className="post-content-container">
                    <div className="post-vote-container">
                        {/* replace with upvote and downvote */}
                        {voteCheck > 0 ? (
                            <i class="fa fa-arrow-circle-up" style={{ fontSize: '36px', color: 'red' }} onClick={() => vote(0)} ></i>

                        ) : (
                                <i class="fa fa-arrow-circle-up" style={{ fontSize: '36px' }} onClick={() => vote(1)} ></i>
                            )}
                        <p className="post-vote-score">{votes}</p>
                        {voteCheck < 0 ? (
                            <i class="fa fa-arrow-circle-down" style={{ fontSize: '36px', color: 'red' }} onClick={() => vote(0)} ></i>
                        ) : (
                                <i class="fa fa-arrow-circle-down" style={{ fontSize: '36px' }} onClick={() => vote(-1)} ></i>
                            )}
                    </div>
                    <div className="post-text-container">
                        {/* align these better later */}
                        <p className="post-text"><a href={profileLink}>{creator}</a></p>
                        <p className="post-text">{date_created}</p>
                        <p className="post-text"><a href={topicLink}>{topic_name}</a></p>
                        <h1 className="post-title">{title}</h1>
                        <p className="post-content">{content}</p>
						<p><a href={postLink}>View Comments</a></p>
                        {saveCheck === -1 ? (
                            <button className="post-save-button" onClick={() => savePost(1)}>Save</button>
                        ) : (
                                <button className="post-save-button" onClick={() => savePost(-1)}>Unsave</button>
                            )}
                    </div>
                    <div className="post-pic-container">
                        {pic_path ? <img src={pic_path} className="post-pic" alt="" /> : null}
                    </div>
                </div>
            </Collapsible>
        </div>
    );
}