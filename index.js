const express = require("express");
const app = express();
app.use(express.urlencoded({ extended: true }));
app.use(express.json());
app.use(express.text());
app.use((req, _, next) => { console.log(req.method, req.url); next() });
const mongoose = require("mongoose");
const dbUri = "mongodb+srv://myuser:myuser@employee.n3nlvkh.mongodb.net/?retryWrites=true&w=majority&appName=Employee";
mongoose.connect(dbUri, { useNewUrlParser: true, useUnifiedTopology: true })
    .then((result) => {
        console.log("connected");
    })
    .catch((err) => console.log(err));

app.set("view engine", "ejs");

const Employee = require("./models/Employee");

app.set("views", "views-ejs");

let toggle = false;

let Employees = {}

Employee.find()
    .then((result) => {
        Employees = result;
    })
    .catch((err) => console.log(err));


let  username = "me" ;

app.get("/toggle/:name",(req, res) => {
    username = req.params.name;
    toggle = !toggle;
    res.send("");
})

app.get("/employee",(req, res) => {
    console.log(Employees)
    Employee.find()
    .then(result => {
    res.render("employee",{Employees:result})
    })
})


app.post("/newid/:user", (req, res) => {


    if (toggle == true) {
        
    Employee.find()
    .then((result) => {
        Employees = result;
    
        Object.keys(Employees).forEach(element => {
            if (Employees[element].card == req.params.user) res.send("Already there")
        });
        const employee = new Employee({ username, card: req.params.user });
        employee.save()
            .then(() => res.send("Employee saved"))
            .catch((err) => console.log(err));
    })
    .catch((err) => console.log(err));
    } else {
        Employee.findOne({ card: req.params.user })
            .then(result => {
                result.present = !result.present;
                result.save().then(() =>
                    res.send("Added")
                )
            })
    }
})

const dataset = {};

//default home page
app.post("/output/:id", (req, res) => {
    if (dataset[req.params.id] == null) dataset[req.params.id] = {};
    dataset[req.params.id] = { ...dataset[req.params.id], ...req.body };
    res.status(200).json(dataset[req.params.id]);
});

//Interacting with page parameters
app.get("/info/:id", (req, res) => {
    res.send(dataset[req.params.id]);
})

//The Main Page
app.get("/", (req, res) => {
    res.render("index", { dataset });
})
//The Main Page
app.get("/data", (req, res) => {
    res.send(dataset);
})

//The page is not found
app.use((req, res) => {
    res.status(404).send("invalid");
})

//Listening on localhost:3000/ 
app.listen(3000);
