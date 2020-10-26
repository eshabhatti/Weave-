import React, { useState, useEffect } from "react";
import Collapsible from 'react-collapsible';

import "./comment.css";

export default function Comment({
    commentId, userName
}) {

    const [errorMessage, updateErrorMessage] = useState("");
    const [commentdata, setCommentData] = useState([]);
    {/* keeps track if user has saved or voted */ }
    const [voteCheck, setVoted] = useState(0);
    {/* current score of post */ }
    const [votes, setVotes] = useState(0);

	
    const access_token = localStorage.getItem('access_token');
    if (access_token == null) {
        window.location = "/login"
    }

    const endpoint = "http://localhost:5000/comment/" + commentId;
    const votepoint = "http://localhost:5000/vote/"
    const statepoint = "http://localhost:5000/commentstates/"

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
            setCommentData(data);
            const { score } = data;
            setVotes(score);
        }).catch(err => {
            console.error(err);

        });

        const body = {
            username: userName,
            comment_id: commentId,
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
            const { voted } = data;
            setVoted(voted);
        }).catch(err => {
            console.error(err);
            alert(err);

        });
    }, [])

    const { topic_name, date_created, content, creator } = commentdata;

    {/* sends the votes to the server and receives the change in score */ }
    const vote = (value, arrow) => {
        setVoted(arrow);
        const body = {
            username: userName,
            type: '2',
            id: commentId,
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
	
	const postLink = "/post/" + postId;
	const profileLink = "/profile/" + creator;
	const topicLink = "/topic/" + topic_name;
	
    return (
        <div>
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css"></link>
            <Collapsible className="comment-content-header" openedClassName="comment-content-header-open" triggerClassName="comment-trigger" triggerOpenedClassName="comment-trigger-open" trigger={title}>
                <div className="comment-content-container">
                    <div className="comment-vote-container">
                        {/* replace with upvote and downvote */}
                        {voteCheck > 0 ? (
                            <i class="fa fa-arrow-circle-up" style={{ fontSize: '36px', color: 'red' }} onClick={() => vote(1, 0)} ></i>

                        ) : (
                                <i class="fa fa-arrow-circle-up" style={{ fontSize: '36px' }} onClick={() => vote(1, 1)} ></i>
                            )}
                        <p className="post-vote-score">{votes}</p>
                        {voteCheck < 0 ? (
                            <i class="fa fa-arrow-circle-down" style={{ fontSize: '36px', color: 'red' }} onClick={() => vote(-1, 0)} ></i>
                        ) : (
                                <i class="fa fa-arrow-circle-down" style={{ fontSize: '36px' }} onClick={() => vote(-1, -1)} ></i>
                            )}
                    </div>
                    <div className="comment-text-container">
                        {/* align these better later */}
                        <p className="comment-text"><a href={profileLink}>{creator}</a></p>
                        <p className="comment-text">{date_created}</p>
                        <p className="comment-text"><a href={topicLink}>{topic_name}</a></p>
                        <p className="comment-content">{content}</p>
                    </div>
                </div>
            </Collapsible>
        </div>
    );
}