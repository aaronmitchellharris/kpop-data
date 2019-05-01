function fillForm(number) {
    document.getElementById("id_vid_title").value = dic[number]["title"]
    document.getElementById("id_vid_publish_date").value = dic[number]["publish"]
    document.getElementById("id_vid_yt_id").value = dic[number]["videoId"]
    document.getElementById("id_vid_thumbnail_url").value = dic[number]["thumbnail"]
};

var m, dic;
dic = [];
function loadClient() {
    gapi.client.setApiKey("AIzaSyDmyWkyolg4wqglm6HVed3-7zxuui9aVSU");
    return gapi.client.load("https://www.googleapis.com/discovery/v1/apis/youtube/v3/rest")
    .then(function() { console.log("GAPI client loaded for API"); },
    function(err) { console.error("Error loading GAPI client for API", err); });
}

function execute() {
    return gapi.client.youtube.search.list({
        "part": "snippet",
        "channelId": "UCOmHUn--16B90oW2L6FRR3A",
        "maxResults": 10,
        "q": "intitle:(mv|m/v)&blackpink",
        "type": "video"
        })
        .then(function(response) {
        // Handle the results here (response.result has the parsed body).
        console.log("Response", response);
        var i, j, hold;
        for (i=0;i<10;i++) {
        dic[i] = {"title":null, "publish":null, "videoId":null, "thumbnail":null};
        j = i.toString()
        hold = response["result"]["items"][i]["snippet"]["publishedAt"].split("T");
        document.getElementById(j).innerHTML = response["result"]["items"][i]["snippet"]["title"];
        dic[i]["title"] =  response["result"]["items"][i]["snippet"]["title"];
        dic[i]["publish"] = hold[0];
        dic[i]["videoId"] = response["result"]["items"][i]["id"]["videoId"];
        dic[i]["thumbnail"] = response["result"]["items"][i]["snippet"]["thumbnails"]["high"]["url"];
        }
        },
        function(err) { console.error("Execute error", err); });
}
gapi.load("client");

function fillForm(number) {
    document.getElementById("id_vid_title").value = dic[number]["title"]
    document.getElementById("id_vid_publish_date").value = dic[number]["publish"]
    document.getElementById("id_vid_yt_id").value = dic[number]["videoId"]
    document.getElementById("id_vid_thumbnail_url").value = dic[number]["thumbnail"]
}