import store from "@/plugins/vuex";
import fetchAPI from "./callAPI";

enum Method {
    GET = "GET",
    POST = "POST",
}
enum APIRoutes {
    getGroups = "groups",
}

export function getGroups() {
    fetchAPI(APIRoutes.getGroups, Method.GET, {})
    .then(response => {
        store.commit({
            type: "setGroups",
            groups: response,
        })
    })
    .catch(err => {
        store.commit({
            type: "setGroups",
            groups: [],
        })
    })
}