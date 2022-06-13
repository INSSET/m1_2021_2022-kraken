// @ts-ignore
import Student from "@/models/student";

export default class Group {

    constructor(
        private _id: number,
        private _name: string,
        private _users: Student[]
    ) {}

    get id(): number {
        return this._id;
    }

    set id(value: number) {
        this._id = value;
    }

    get name(): string {
        return this._name;
    }

    set name(value: string) {
        this._name = value;
    }

    get users(): Student[] {
        return this._users;
    }

    set users(value: Student[]) {
        this._users = value;
    }

    addUser(student: Student): void {
        this._users.push(student);
    }

    removeUser(student: Student): void {
        this._users = this._users.filter(user => student.id !== user.id);
    }

}
