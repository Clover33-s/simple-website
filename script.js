document.addEventListener('DOMContentLoaded', () => {
    const videoContainer = document.querySelector('.video-container');

    const videos = [
        {
            url: 'https://assets.mixkit.co/videos/preview/mixkit-a-girl-blowing-a-bubble-gum-at-an-amusement-park-4533-large.mp4',
            author: '@jules',
            description: 'Having fun at the park! #fun #bubblegum',
            song: 'Upbeat Funky Pop',
            likes: '1.2M',
            comments: '45.3K',
            shares: '22.1K'
        },
        {
            url: 'https://assets.mixkit.co/videos/preview/mixkit-mother-with-her-little-daughter-eating-a-marshmallow-in-nature-4576-large.mp4',
            author: '@jane_doe',
            description: 'Sweet treats with my sweetie pie! #family #marshmallow',
            song: 'Acoustic Folk',
            likes: '876K',
            comments: '12.2K',
            shares: '5.6K'
        },
        {
            url: 'https://assets.mixkit.co/videos/preview/mixkit-girl-in-a-leather-jacket-and-a-hat-with-a-coffee-to-go-4530-large.mp4',
            author: '@coffee_lover',
            description: 'Coffee is life! #coffee #citylife',
            song: 'Chill Lo-fi Hip Hop',
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
});
