import axios from "axios";
import container from "@/plugins/vuex";
import type Student from "@/models/student";
import type Group from "@/models/group";
import groupService from "./group-service";

export default new class StudentService {

    BASE_URL = "http://backend.insset.localhost/api/v1/";

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
     * get Student information by his id
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

    /**
     * Get Student information by his name
     * 
     * @param nameStudent 
     */
    async getStudentInformationByName(nameStudent: string) {
        axios.get("http://0.0.0.0:5000/api/v1/students/"+nameStudent).then(response => {
            container.commit({
                type: "reloadStudents",
                studentInformation: response.data,
            })
        })
    }

    /**
     * Set action to container
     * 
     * @param idStudent 
     * @param action 
     */
    async setActionContainer(idStudent: string, action: string) {
        axios.post("http://0.0.0.0:5000/api/v1/students/" + idStudent + "/container/command/" + action).then(function (response) {
            if (response.status == 200) {
                container.commit({
                    type: "reloadContainer"
                })
            }
        })
    }

    /**
     * Get all ssh keys for a student
     * 
     * @param idStudent 
     */
    async getSshKeys(idStudent: string) {
        axios.get("http://0.0.0.0:5000/api/v1/students/" + idStudent + "/keys")
        .then(function (response) {
            container.commit({
                type: "reloadSshKey",
                sshKeys: response.data,
            })
        })
    }

    /**
     * Add ssh key to a student
     * 
     * @param idStudent 
     */
    async addSshKey(idStudent: string) {
        axios.post("http://0.0.0.0:5000/api/v1/students"+idStudent+"/ssh/upload").then(function (response) {
            if (response.status == 200) {
                container.commit({
                    type: "reloadSshKey"
                })
            }
        })
    }

    /**
     * Delete a student from a group
     * 
     * @param student 
     * @param groupId 
     */
    async deleteStudentFromGroup(student: Student, groupId: number) {

        axios.delete(`${this.BASE_URL}students/${student.name}`)
        .then(res => {
            if (res.status == 200) {
                groupService.findAll()
            }
        })

    }
    /**
     * 
     * @param idStudent 
     */
     async getDockerFile(idStudent: string) {
        axios.get("http://0.0.0.0:5000/api/v1/students"+idStudent+"/dockerfile").then(function (response) {
            if (response.status == 200) {
                container.commit({
                    type: "reloadDockerfile",
                    dockerfile: response.data
                })
            }
        })
    }

    /**
     * 
     * @param idStudent 
     */
     async setDockerFile(idStudent: string) {
        axios.post("http://0.0.0.0:5000/api/v1/students"+idStudent+"/dockerfile").then(function (response) {
            if (response.status == 200) {
                container.commit({
                    type: "reloadDockerfile",
                    dockerfile: response.data
                })
            }
        })
    }
}
