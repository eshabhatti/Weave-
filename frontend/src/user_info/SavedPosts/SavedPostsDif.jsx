import React, { useState, useEffect } from "react";
import NavBar from "../../Shared_Components/NavBar";
import Post from "../../Shared_Components/Post/Post";
import ReactPaginate from 'react-paginate';

import './savedposts.css';

export default function SavedPosts() {
  const [postData, setPostData] = useState([]);
  const [currentPage, setCurrentPage] = useState(0);
  const [pageCount, setPageCount] = useState(0)
  const [perPage] = useState(5);
  const access_token = localStorage.getItem('access_token');
  if (access_token == null) {
    window.location = "/login"
  }
  useEffect(() => {
    const endpoint = "http://localhost:5000/savedposts/"
    const offset = currentPage * perPage
    fetch(endpoint, {
      method: "POST",
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + access_token
      },
      body: JSON.stringify({
        start: offset,
        end: offset + perPage
      })
    }).then(response => response.json()).then(data => {
        const { pull_list: post_ids, rowCount: rowCount} = data;
        setPageCount(Math.ceil(rowCount/perPage))
        setPostData(post_ids);
    }).catch(err => {
      console.log(err);
      alert("Error in console");
    });
  }, [currentPage]);

  let postsContent = [];
  postData.forEach((postId) => {
    postsContent.push(<Post postId={postId} userName={"sahilkapur"} />)
  });
  if (postsContent.length === 0) {
    postsContent = <p>No Posts!</p>;
  }

  const handlePageClick = (e) => {
    const selectedPage = e.selected;
    setCurrentPage(selectedPage);
  };
  
  return (
    <div>
        <NavBar />
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