const express = require("express");
const app = express();
app.use(express.urlencoded({ extended: true }));
app.use(express.json());
app.use(express.text());
app.use((req, _, next) => { console.log(req.method, req.url); next() });

const dataset = {};


//default home page
app.post("/output/:id", (req, res) => {
    if(dataset[req.params.id]==null) dataset[req.params.id]= {};
    dataset[req.params.id] = {...dataset[req.params.id],...req.body};
    res.status(200).json(dataset[req.params.id]);
});

//Interacting with page parameters
app.get("/info/:id",(req,res)=>{
    res.send(dataset[req.params.id]);
})

//The Main Page
app.get("/",(req,res)=>{
    res.send(dataset);
})

//The page is not found
app.use((req, res) => {
    res.status(404).send("invalid");
  })

//Listening on localhost:3000/ 
app.listen(3000);