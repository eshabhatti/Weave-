import React, { useState, useEffect } from "react";
import Post from "../../Shared_Components/Post/Post";
import ReactPaginate from 'react-paginate';

import './Feed.css';

export default function PostFeed({route, topic, post_id}) {
  const [postData, setPostData] = useState([]);
  const [postsContent, setPostsContent] = useState([]);
  const [currentPage, setCurrentPage] = useState(0);
  const [pageCount, setPageCount] = useState(0)
  const [perPage] = useState(5);
  const access_token = localStorage.getItem('access_token');
  if (access_token == null) {
    window.location = "/login"
  }
  useEffect(() => {
    const endpoint = "http://localhost:5000/" + route
    const offset = currentPage * perPage
    const body = {
      start: offset,
      end: perPage,
	  topic: topic,
	  post_id, post_id,
    }
    fetch(endpoint, {
      method: "POST",
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + access_token
      },
      body: JSON.stringify(body)
    }).then(response => response.json()).then(data => {
        const { pull_list: post_ids, rowCount: rowCount} = data;
        setPageCount(Math.ceil(rowCount/perPage))
        setPostData(post_ids);
        console.log(post_ids)
        console.log(postData)
    }).catch(err => {
      console.log(err);
      alert("Error in console");
    });
  }, [currentPage]);

  useEffect(() => {
    let tester = [];
    postData.forEach((postId) => {
      //console.log(postId)
      tester.push(<Post key={postId} postId={postId} userName={"schikyal"} />)
    });
    if (postsContent.length === 0) {
      tester = <p>No Posts!</p>;
    }
    console.log(postData);
    setPostsContent(tester);
  }, [postData])


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
            activeClassName={"active"}/>
    </div>
  );
}