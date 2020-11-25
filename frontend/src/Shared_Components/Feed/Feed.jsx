import React, { useState, useEffect } from "react";
import Post from "../../Shared_Components/Post/Post";
import Comment from '../../Shared_Components/Comment/Comment';
import ProfilePreview from '../../Shared_Components/ProfilePreview/ProfilePreview';
import ReactPaginate from 'react-paginate';

import './Feed.css';

export default function Feed({ route, topic, post_id, username, elementType, reloadFlag }) {
  const [postData, setPostData] = useState([]);
  const [postsContent, setPostsContent] = useState([]);
  const [currentPage, setCurrentPage] = useState(0);
  const [pageCount, setPageCount] = useState(0)
  const [perPage] = useState(5);
  let access_token = localStorage.getItem('access_token');
  if (access_token == null) {
    window.location = "/login"
  }

  useEffect(() => {
    const endpoint = (process.env.NODE_ENV === 'production' ? "http://weave.projectcarbon.io/server" : "http://localhost:5000") + "/" + route;
    const offset = currentPage * perPage;
    const body = {
      start: offset,
      end: perPage,
      topic: topic,
      post_id: post_id,
      username: username,
    }
    console.log(JSON.stringify(body));
    console.log(endpoint);
    fetch(endpoint, {
      method: "POST",
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + access_token
      },
      body: JSON.stringify(body)
    }).then(response => response.json()).then(data => {
      const { pull_list: post_ids, rowCount: rowCount } = data;
      setPageCount(Math.ceil(rowCount / perPage))
      setPostData(post_ids);
      setCurrentPage(0)
    }).catch(err => {
      console.log(err);
    });
  }, [route, reloadFlag]);

  useEffect(() => {
    const endpoint = (process.env.NODE_ENV === 'production' ? "http://weave.projectcarbon.io/server" : "http://localhost:5000") + "/" + route
    console.log(endpoint)
    const offset = currentPage * perPage
    const body = {
      start: offset,
      end: perPage,
      topic: topic,
      post_id: post_id,
      username: username,
    }
    fetch(endpoint, {
      method: "POST",
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + access_token
      },
      body: JSON.stringify(body)
    }).then(response => response.json()).then(data => {
      const { pull_list: post_ids, rowCount: rowCount } = data;
      setPageCount(Math.ceil(rowCount / perPage))
      setPostData(post_ids);
    }).catch(err => {
      console.log(err);
      // alert("Error in console");
    });
  }, [currentPage, reloadFlag]);

  useEffect(() => {
    let tester = [];
    if (postData) {
      postData.forEach((identifier) => {
        console.log(identifier)
        if (elementType == "comment") {
          tester.push(<Comment key={identifier} commentId={identifier} userName={"schikyal"} />)
        }
		else if (elementType == "profile") {
		  tester.push(<ProfilePreview username={identifier} />)		
		}
        else {
          tester.push(<Post key={identifier} postId={identifier} userName={"schikyal"} redesign={true} isMinimized={true} />)
        }
      });
      setPostsContent(tester);
      if (postsContent.length === 0) {
        tester = <p>No Content Yet!</p>;
      }
    }
  }, [postData, reloadFlag])


  const handlePageClick = (e) => {
    const selectedPage = e.selected;
    setCurrentPage(selectedPage);
  };

  return (
    <div className="posts-display">
      {postsContent}
      <ReactPaginate
        previousLabel={"<"}
        nextLabel={">"}
        pageCount={pageCount}
        marginPagesDisplayed={1}
        pageRangeDisplayed={5}
        onPageChange={handlePageClick}
        containerClassName={"pagination"}
        subContainerClassName={"pages pagination"}
        activeClassName={"active"} />
    </div>
  );
}