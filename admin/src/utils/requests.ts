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

export function createGroupsWithCSV(group_name : string, file : object) {
    fetchAPI(`groups/${group_name}/upload`, Method.POST, {
        file: file,
    })
    .then(response => {
        
    })
    .catch(err => {

    })
}