// future enhancements

console.log("Photo Organizer UI loaded");

// could add:
// - infinite scroll
// - keyboard navigation
// - fullscreen viewer

function deleteFile(path) {
    fetch("/delete", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ path })
    }).then(() => {
        location.reload();
    });
}