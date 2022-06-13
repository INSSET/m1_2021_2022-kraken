import axios from "axios";
import container from "@/plugins/vuex";
import Student from "@/models/student";

export default new class StudentService {


    /**
     * Get all Container
     *
     * @param idStudent
     */
    async getContainerInfo(idStudent: string) {

        axios.get(`/student/${idStudent}`).then(response => {
            container.commit({
                type: "reloadContainer",
                allContainer: response.data[idStudent],
            });
        })

    }

    /**
     * get Student information
     * 
     * @param idStudent
     */
    async getStudentInformation(idStudent: string) {
        axios.get(`/student/${idStudent}`).then(response => {
            container.commit({
                type: "reloadStudents",
                studentInformation: response.data,
            });
        }).catch(err => {
            container.commit({
                type: "reloadStudents",
                studentInformation: [],
            })
        })
    }

}
