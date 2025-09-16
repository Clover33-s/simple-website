document.addEventListener('DOMContentLoaded', () => {
    const videoContainer = document.querySelector('.video-container');

    function createVideoPlayer(videoData) {
        const videoPlayer = document.createElement('div');
        videoPlayer.classList.add('video-player');

        const videoElement = document.createElement('video');
        videoElement.src = videoData.url;
        videoElement.loop = true;
        videoElement.muted = true;

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

        const likeBtn = videoSidebar.querySelector('.fa-heart');
        const commentBtn = videoSidebar.querySelector('.fa-comment-dots');
        const shareBtn = videoSidebar.querySelector('.fa-share');

        likeBtn.parentElement.addEventListener('click', () => alert('Liked!'));
        commentBtn.parentElement.addEventListener('click', () => alert('Commented!'));
        shareBtn.parentElement.addEventListener('click', () => alert('Shared!'));
    }

    async function loadVideos() {
        try {
            const response = await fetch('/api/videos');
            const videos = await response.json();
            videos.forEach(createVideoPlayer);
            setupIntersectionObserver();
        } catch (error) {
            console.error('Error loading videos:', error);
        }
    }

    function setupIntersectionObserver() {
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
    }

    loadVideos();

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

    // Page navigation
    const navItems = document.querySelectorAll('.nav-item');
    const pages = document.querySelectorAll('.page');

    navItems.forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();

            const targetPage = item.getAttribute('data-page');

            pages.forEach(page => {
                if (page.id === targetPage) {
                    page.style.display = 'block';
                } else {
                    page.style.display = 'none';
                }
            });

            const navArrows = document.querySelector('.nav-arrows');
            if (targetPage === 'home') {
                navArrows.style.display = 'flex';
            } else {
                navArrows.style.display = 'none';
            }

            navItems.forEach(nav => nav.classList.remove('active'));
            item.classList.add('active');
        });
    });
});
