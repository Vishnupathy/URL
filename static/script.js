document.addEventListener("DOMContentLoaded", function() {
    const links = document.querySelectorAll("a");
    
    links.forEach(link => {
        link.addEventListener("click", function(event) {
            event.preventDefault();
            window.open(event.target.href, '_blank');
            location.reload();
        });
    });

    document.querySelectorAll('.copyButton').forEach(function(button) {
        button.addEventListener('click', function(e) {
            const url = e.target.getAttribute('data-url');
            navigator.clipboard.writeText("http://127.0.0.1:5000/"+url).then(function() {
                e.target.textContent = 'Copied!';
                setTimeout(function() {
                    e.target.textContent = 'Copy';
                }, 2000);
            });
        });
    });
});

function nativeShare(url) {
    if (navigator.share) {
        navigator.share({
            title: 'Share this link',
            url: url
        }).then(() => {
            console.log('Thanks for sharing!');
        })
        .catch(console.error);
    } else {
        alert('Web Share API not supported.');
    }
}

function deleteUrl(event, shortUrl) {
    event.preventDefault();

    fetch('/delete_url', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ url: shortUrl })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            location.reload();
        } else {
            alert('Failed to delete URL');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
