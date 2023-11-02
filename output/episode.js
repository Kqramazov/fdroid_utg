function getNodeByIdx(nodeIdx) {
    return utg.nodes[nodeIdx];
}
function getEdgeByIdx(edgeIdx) {
    return utg.edges[edgeIdx];
}

function getPathDetails(path) {
    var len = path.nodes.length;
    pathInfo = "<h2>Transition Details</h2><hr/>\n";
    var i;
    for (i = 0; i < len; i++) {
        state = getNodeByIdx(path.nodes[i]);
        pathInfo += "<img class=\"col-md-5\" src=\"" + state.image + "\">\n"

    }
    pathInfo += "<table class=\"table table-striped\">\n"
    pathInfo += "<tr class=\"active\"><th colspan=\"4\"><h4>Events</h4></th></tr>\n";
    pathInfo += "<tr><th>id</th><th>type</th><th>view</th><th>event_str</th></tr>\n"
    var k;
    for (k = 0; k < len - 1; k++) {
        var selectedEdge = getEdgeByIdx(k);
        for (i = 0; i < selectedEdge.events.length; i++) {
            event = selectedEdge.events[i];
            eventStr = event.event_str;
            var viewImg = "";
            if (event.view_images != null) {
                var j;
                for (j = 0; j < event.view_images.length; j++) {
                    viewImg += "<img class=\"viewImg\" src=\"" + event.view_images[j] + "\">\n"
                }
            }
            pathInfo += "<tr><td>" + event.event_id + "</td><td>" + event.event_type + "</td><td>" + viewImg + "</td><td>" + event.event_str + "</td></tr>"
        }
    }

    pathInfo += "</table>\n"
    return pathInfo;
}

// 示例用法，假设你有一个路径对象 path
var path = {
    "nodes": [
        0,
        1,
        2,
        11,
        12,
        0,
        24,
        5,
        13,
        0
    ],
    "edges": [
        0,
        5,
        13,
        39,
        46,
        3,
        66,
        22,
        51
    ]
};

var pathDetail = getPathDetails(path);
var tableContainer = document.getElementById("table-container");
tableContainer.innerHTML = pathDetail;


