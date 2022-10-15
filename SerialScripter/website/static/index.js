function deleteKey(keyId) {
    // fetch the end point created in views.py
    fetch("/delete-key", {
        method: "POST",
        body: JSON.stringify({ keyId: keyId }),
        // creates a json object that we can access as a dict in python containing the keyId that we need
    }).then((_res) => {
        // refreshes the page
        window.location.href = "/key-management";
    });
}