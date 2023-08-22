document.addEventListener("DOMContentLoaded", function() {
// Creating a new Post / Post-Form
  var createPostButton = document.getElementById("create-post");
  var newPostDiv = document.getElementById("new_post");
  var postButton = document.getElementById("post_button");
  var closeButton = document.getElementById("close_new_post");
  var newPostBody = document.getElementById("new_post_body");

  //New Post Box
  if (newPostDiv) {
    // Hide the new post div
    newPostDiv.style.display = "none";
  }

  // Show the new post div when create post button is clicked
  if (createPostButton && newPostDiv && newPostBody) {
    createPostButton.addEventListener("click", function() {
      newPostDiv.style.display = "block";
      newPostBody.value = "";
    });
  }

  // Hide the div when close button is clicked
  if (closeButton && newPostDiv && newPostBody) {
    closeButton.addEventListener("click", function(event) {
      event.preventDefault(); // Prevent form submission
      newPostDiv.style.display = "none";
      newPostBody.value = "";
    });
  }

  // Handle form submission
  if (postButton && newPostBody && newPostDiv) {
    postButton.addEventListener("click", function(event) {
      event.preventDefault(); // Prevent form submission

      // Retrieve post body text
      var postBody = newPostBody.value;

      // Make an AJAX request to create post
      var xhr = new XMLHttpRequest();
      xhr.open("POST", "/create_post/", true);
      // Sending form data
      xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");

      // Set the CSRF token header using the {% csrf_token %} template tag
      var csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
      xhr.setRequestHeader("X-CSRFToken", csrftoken);

      xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE) {
          if (xhr.status === 200) {
            // Success:
            var response = JSON.parse(xhr.responseText);
            console.log(response.message);
            // Refresh the page
            location.reload();
          } else {
            // Error:
            console.error("Error creating post:", xhr.responseText);
          }
        }
      };

      // Prepare the data to be sent
      var data = "body_text=" + encodeURIComponent(postBody);

      // Send the request with the data
      xhr.send(data);

      // Hide the new post div
      newPostDiv.style.display = "none";
    });
  }
// End of New Post Box //


// Follow button & count
  var followButton = document.getElementById("follow_button");
  var followersCountElement = document.getElementById("followers_count");
  // Filter for follower count
  var followersCount = followersCountElement ? parseInt(followersCountElement.textContent.split(":")[1].trim()) : 0;

  if (followButton && followersCountElement) {
    followButton.addEventListener("click", function(event) {
      event.preventDefault(); // Prevent form submission

      // Retrieve profile ID and CSRF token
      var profileId = followButton.dataset.profileId;
      var csrfToken = followButton.dataset.csrfToken;

      // Make AJAX request to toggle the follow status
      var xhr = new XMLHttpRequest();
      xhr.open("POST", "/follow-toggle/", true);
      xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
      xhr.setRequestHeader("X-CSRFToken", csrfToken);

      xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE) {
          if (xhr.status === 200) {
            // Success:
            var response = JSON.parse(xhr.responseText);

            // Toggle the button text
            if (response.following_status) {
              followButton.textContent = "Unfollow";
              followersCount++;
            } else {
              followButton.textContent = "Follow";
              followersCount--;
            }

            // Update followers count
            followersCountElement.textContent = "Followers: " + followersCount;
          } else {
            // Error:
            console.error("Error toggling follow status:", xhr.responseText);
          }
        }
      };

      // Prepare data to be sent
      var data = "profile_id=" + encodeURIComponent(profileId);

      // Send request with data
      xhr.send(data);
    });
  }
// End of Follow button & count


// Like button
  var likeButtons = document.querySelectorAll(".like_button");
  var csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

  likeButtons.forEach(function(likeButton) {
      likeButton.addEventListener("click", function(event) {
          event.preventDefault();

          var postId = likeButton.dataset.postId;
          var postLikesElement = likeButton.querySelector(".post_likes");

          var xhr = new XMLHttpRequest();
          xhr.open("POST", "/like-toggle/" + postId + "/", true);
          xhr.setRequestHeader("Content-Type", "application/json");
          xhr.setRequestHeader("X-CSRFToken", csrfToken);
          // Define a function to handle the XMLHttpRequest state change event
          xhr.onreadystatechange = function() {
              if (xhr.readyState === XMLHttpRequest.DONE) {
                  if (xhr.status === 200) {
                      var response = JSON.parse(xhr.responseText);

                      // Update likes count
                      postLikesElement.innerHTML = "&#x1F49C; " + response.likes;
                  } else {
                      console.error("Error toggling like:", xhr.responseText);
                  }
              }
          };
          // Send XMLHttpRequest
          xhr.send();
      });
  });
// End of like button


// Edit Post
  window.onload = function() {
    var editButtons = document.querySelectorAll("#edit_opt");

    editButtons.forEach(function(editButton) {
      editButton.addEventListener("click", function(event) {
        event.preventDefault();
        var postId = editButton.dataset.postId;
        var postContent = document.getElementById('post_' + postId);
        var editContent = document.getElementById('edit_' + postId);
        var currentText = postContent.querySelector('#post_body').textContent.trim();
        var textarea = editContent.querySelector('textarea');
        // Hide post content and display edit content
        postContent.style.display = 'none';
        editContent.style.display = 'block';
        textarea.value = currentText;
      });
  });
  // Get all save buttons
  var saveButtons = document.querySelectorAll(".save_button");
  // Add click event listener to each save button
  saveButtons.forEach(function(saveButton) {
      saveButton.addEventListener("click", function(event) {
        event.preventDefault();
        var postId = saveButton.dataset.postId;
        var editedText = document.getElementById('edit_text_' + postId).value;
        var csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

        var xhr = new XMLHttpRequest();
        xhr.open("POST", "/update_post/" + postId + "/", true);
        xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
        xhr.setRequestHeader("X-CSRFToken", csrfToken);

        xhr.onreadystatechange = function() {
          if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
              var response = JSON.parse(xhr.responseText);
              var postContent = document.getElementById('post_' + postId);
              var editContent = document.getElementById('edit_' + postId);
              // Update post content with the edited text
              postContent.querySelector('#post_body').textContent = response.body_text;
              // Hide edit content and display post content
              postContent.style.display = 'block';
              editContent.style.display = 'none';
            } else {
              console.error("Error updating post:", xhr.responseText);
            }
          }
        };
        // Prepare data to be sent in the request body
        var data = "text=" + encodeURIComponent(editedText) + "&csrfmiddlewaretoken=" + encodeURIComponent(csrfToken);
        xhr.send(data);
      });
    });
  };

});
