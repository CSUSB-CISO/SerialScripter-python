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
function checkAllBoxes(source) {
    var checkboxes = document.querySelectorAll('input[class="boxes"]');

    for (var i = 0; i < checkboxes.length; i++) {
        if (checkboxes[i] != source)
            checkboxes[i].checked = source.checked;
    }
}
function checkAllScripts(source) {
    var checkboxes = document.querySelectorAll('input[class="scripts"]');

    for (var i = 0; i < checkboxes.length; i++) {
        if (checkboxes[i] != source)
            checkboxes[i].checked = source.checked;
    }
}
