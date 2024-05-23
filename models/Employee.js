const mongoose = require("mongoose");
const Schema = mongoose.Schema;

const EmployeeSchema = new Schema({
    username: {
        type: String,
        required: true
    },
    card: {type:Number,unique: true},
    present: {
        type:Boolean,
        default: false
    }
}, { timestamps: true })

const Employee = mongoose.model("Employee", EmployeeSchema);

module.exports = Employee;