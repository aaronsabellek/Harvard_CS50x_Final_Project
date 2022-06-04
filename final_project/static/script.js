// Show "Top"-button after scrolling
mybutton = document.getElementById("myBtn");
window.onscroll = function() {scrollFunction()};
function scrollFunction() {
    if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
        mybutton.style.display = "block";
    } else {
        mybutton.style.display = "none";
    }
}

// Scroll to top of the document after click on the button
function topFunction() {
    document.body.scrollTop = 0;
    document.documentElement.scrollTop = 0;
}

// Show post content after click on post
function expand(post) {
    var element = document.getElementById("content_" + post.id);
    if (element.style.display == "none") {
        element.style.display = "block";
    } else {
        element.style.display = "none";
    }
}

// Display and filter followers
function filter_follower() {
    var posts = document.getElementById('posts');
    var own = document.getElementById('own');
    var followed = document.getElementById('followed');
    var follower = document.getElementById('follower');
    var text = document.getElementById('filter_follower_btn');
    posts.style.display = "none";
    own.style.display = "none";
    if (text.firstChild.data == "Follower") {
        follower.style.display = "block";
        followed.style.display = "none";
        text.firstChild.data = "Followed";
    } else {
        text.firstChild.data = "Follower";
        followed.style.display = "block";
        follower.style.display = "none";
    }
}

// Show and display posts
function filter_posts() {
    var posts = document.getElementById('posts');
    var own = document.getElementById('own');
    var followed = document.getElementById('followed');
    var follower = document.getElementById('follower');
    var text = document.getElementById('filter_posts_btn');
    followed.style.display = "none";
    follower.style.display = "none";
    if (text.firstChild.data == "All Posts") {
        own.style.display = "none";
        posts.style.display = "block";
        text.firstChild.data = "User Posts";
    } else {
        text.firstChild.data = "All Posts";
        own.style.display = "block";
        posts.style.display = "none";
    }
}
