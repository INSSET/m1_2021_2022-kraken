export default class Student {

    constructor(
        private _id: number,
        private _name: string,
        private _group_name: string
    ) {}

    get name(): string {
        return this._name;
    }

    set name(value: string) {
        this._name = value;
    }

    get id(): number {
        return this._id;
    }

    set id(value: number) {
        this._id = value;
    }

    get group_name(): string {
        return this._group_name;
    }

    set group_name(value: string) {
        this._group_name = value;
    }

}
