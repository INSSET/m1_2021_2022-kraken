import fetchAPI from "./callAPI";

enum Method {
    GET = "GET",
}
enum APIRoutes {
    getGroups = "students",
}

function getGroups() {
    fetchAPI(APIRoutes.getGroups, Method.GET)
    .then(response => {
        console.log(response);
    })
    .catch(err => {
        console.log(err);
    })
}

export default {
    getGroups,
}