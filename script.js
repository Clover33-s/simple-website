document.addEventListener('DOMContentLoaded', () => {
    const videoContainer = document.querySelector('.video-container');

    const videos = [
        {
            url: 'http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4',
            author: '@jules',
            description: 'Big Buck Bunny! #blender #animation',
            song: 'Upbeat Funky Pop',
            likes: '1.2M',
            comments: '45.3K',
            shares: '22.1K'
        },
        {
            url: 'http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4',
            author: '@jane_doe',
            description: 'Elephants Dream! #blender #animation',
            song: 'Acoustic Folk',
            likes: '876K',
            comments: '12.2K',
            shares: '5.6K'
        },
        {
            url: 'http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4',
            author: '@google',
            description: 'For Bigger Blazes! #google #chromecast',
            song: 'Cinematic',
            likes: '2.3M',
            comments: '67.8K',
            shares: '33.4K'
        }
    ];

    videos.forEach(videoData => {
        const videoPlayer = document.createElement('div');
        videoPlayer.classList.add('video-player');

        const videoElement = document.createElement('video');
        videoElement.src = videoData.url;
        videoElement.loop = true;
        videoElement.muted = true; // Muted by default to allow autoplay in most browsers

        const videoInfo = document.createElement('div');
        videoInfo.classList.add('video-info');
        videoInfo.innerHTML = `
            <div class="author"><strong>${videoData.author}</strong></div>
            <div class="description">${videoData.description}</div>
            <div class="song-info">
                <i class="fas fa-music"></i>
                <span>${videoData.song}</span>
            </div>
        `;

        const videoSidebar = document.createElement('div');
        videoSidebar.classList.add('video-sidebar');
        videoSidebar.innerHTML = `
            <div class="sidebar-icon">
                <i class="fas fa-heart"></i>
                <span>${videoData.likes}</span>
            </div>
            <div class="sidebar-icon">
                <i class="fas fa-comment-dots"></i>
                <span>${videoData.comments}</span>
            </div>
            <div class="sidebar-icon">
                <i class="fas fa-share"></i>
                <span>${videoData.shares}</span>
            </div>
            <div class="rotating-record"></div>
        `;

        videoPlayer.appendChild(videoElement);
        videoPlayer.appendChild(videoInfo);
        videoPlayer.appendChild(videoSidebar);
        videoContainer.appendChild(videoPlayer);

        // Add event listeners for sidebar icons
        const likeBtn = videoSidebar.querySelector('.fa-heart');
        const commentBtn = videoSidebar.querySelector('.fa-comment-dots');
        const shareBtn = videoSidebar.querySelector('.fa-share');

        likeBtn.parentElement.addEventListener('click', () => {
            alert('Liked!');
        });

        commentBtn.parentElement.addEventListener('click', () => {
            alert('Commented!');
        });

        shareBtn.parentElement.addEventListener('click', () => {
            alert('Shared!');
        });
    });

    const observerOptions = {
        root: videoContainer,
        rootMargin: '0px',
        threshold: 0.8
    };

    const handleIntersection = (entries, observer) => {
        entries.forEach(entry => {
            const video = entry.target.querySelector('video');
            if (entry.isIntersecting) {
                video.play().catch(error => console.log("Autoplay was prevented: ", error));
            } else {
                video.pause();
                video.currentTime = 0;
            }
        });
    };

    const observer = new IntersectionObserver(handleIntersection, observerOptions);

    const videoPlayers = document.querySelectorAll('.video-player');
    videoPlayers.forEach(player => observer.observe(player));

    // Add navigation arrows
    const appContainer = document.querySelector('.app-container');
    const navArrows = document.createElement('div');
    navArrows.classList.add('nav-arrows');

    const arrowUp = document.createElement('i');
    arrowUp.classList.add('fas', 'fa-chevron-up', 'nav-arrow');
    arrowUp.id = 'arrow-up';

    const arrowDown = document.createElement('i');
    arrowDown.classList.add('fas', 'fa-chevron-down', 'nav-arrow');
    arrowDown.id = 'arrow-down';

    navArrows.appendChild(arrowUp);
    navArrows.appendChild(arrowDown);
    appContainer.appendChild(navArrows);

    arrowUp.addEventListener('click', () => {
        const currentScroll = videoContainer.scrollTop;
        const videoHeight = videoContainer.clientHeight;
        videoContainer.scrollTo({
            top: currentScroll - videoHeight,
            behavior: 'smooth'
        });
    });

    arrowDown.addEventListener('click', () => {
        const currentScroll = videoContainer.scrollTop;
        const videoHeight = videoContainer.clientHeight;
        videoContainer.scrollTo({
            top: currentScroll + videoHeight,
            behavior: 'smooth'
        });
    });
});
