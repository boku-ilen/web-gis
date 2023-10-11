const escapeHtml = (unsafe) => {
    return unsafe
        .replaceAll('&', '&amp;')
        .replaceAll('<', '&lt;')
        .replaceAll('>', '&gt;')
        .replaceAll('"', '&quot;')
        .replaceAll("'", '&#039;')
        .replaceAll("\n", "</br>")
}

// From https://www.w3schools.com/js/js_cookies.asp
const setCookie = function(cname, cvalue, exdays) {
    const d = new Date();
    d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
    let expires = "expires="+d.toUTCString();
    let samesite = "SameSite=Strict"; // Cookie is only usable by this site, not by others
    document.cookie = cname + "=" + cvalue + ";" + expires + ";" + samesite + ";" + "path=/" + location.pathname.split("/")[1];
}

const getCookie = function(cname) {
    let name = cname + "=";
    let ca = document.cookie.split(';');
    for(let i = 0; i < ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) == ' ') {
        c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
        return c.substring(name.length, c.length);
        }
    }
    return "";
}