import store from "@/plugins/vuex";
import fetchAPI from "./callAPI";

enum Method {
    GET = "GET",
}
enum APIRoutes {
    getGroups = "groups",
}

export function getGroups() {
    fetchAPI(APIRoutes.getGroups, Method.GET)
    .then(response => {
        console.log(response);
        store.commit({
            type: "setGroups",
            groups: response,
        })
    })
    .catch(err => {
        console.log(err);
        store.commit({
            type: "setGroups",
            groups: [],
        })
    })
}