import axios from "axios";
import store from "@/plugins/vuex";

export default new class GroupService {

    /**
     * Fetch all groups
     */
    async findAll() {

        axios.get(`/groups`).then(response => {
            store.commit({
                type: "setGroups",
                groups: response.data,
            });
        }).catch(err => {
            store.commit({
                type: "setGroups",
                groups: [],
            });
        });

    }

    /**
     * Creation of a group
     *
     * @param groupName
     * @param groupFile
     */
    async create(groupName: string, groupFile: object) {

        axios.post(`/groups/${groupName}/upload`,
            {
                file: groupFile
            },
            {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            }).then(response => {
            // TODO : Check response

            console.log(response)
        }).catch(error => {

            // TODO : Set error

        });

    }

}
