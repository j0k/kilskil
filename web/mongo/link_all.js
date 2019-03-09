//use kilskil2;
user = db.users.findOne({"code":"u1"})
// db.skills.findAndModify({
//   query:{},
//   update: {
//     $set: {
//       "ref._uid": user["_id"]
//     }
//   }
// });

db.skills.find({"code":{$regex : "u1_"}}).forEach(function(item){
  item.ref._uid  = user["_id"];
  item.ref._ouid = user["_id"];
  db.skills.save(item);
});


// connect with progress
db.skills.find().forEach(function(item){
  progress = db.progress.findOne({"code" : item["code"]});
  progress.ref      = {};
  progress.ref._uid = item.ref._uid;
  progress.ref._sid = item._id;

  db.progress.save(progress);
});

//upsert: true,
//new: true
db.createView (
   "skillProgress",
   "skills",
   { $lookup: { from: "progress", localField: "_id", foreignField: "ref._sid", as: "progress" } }
);



db.createView (
   "skillProgressShort",
   "skills", [
     { $lookup: { from: "progress", localField: "_id", foreignField: "ref._sid", as: "progress" } },
     { $project: { "progress": { $arrayElemAt: [ "$progress", 0 ] },  'title' :1 , "desc": 1,  "materials" : 1, "tags":1, "freq":1, "count":1, "ref":1 } }
  ]
);


db.createView (
   "userSkills",
   "users",
   [
     { $lookup: { from: "skills", localField: "_id", foreignField: "ref._uid", as: "skills" } }
   ]
);

db.createView (
   "userSkillProgress",
   "users",
   [
     { $lookup: { from: "skillProgressShort", localField: "_id", foreignField: "ref._uid", as: "skills" } }
   ]
)
