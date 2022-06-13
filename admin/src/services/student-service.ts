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
                type: "containerInfo",
                allContainer: response.data,
            });
        }).catch(err => {
            container.commit({
                type: "containerInfo",
                allContainer: [],
            });
        });

    }

    /**
     * get Student information
     * 
     * @param idStudent
     */
    async getStudentInformation(idStudent: string) {
        axios.get(`/student/${idStudent}`).then(response => {
            container.commit({
                type: "students",
                studentInformation: response.data,
            });
        }).catch(err => {
            container.commit({
                type: "students",
                studentInformation: [],
            })
        })
    }

}
