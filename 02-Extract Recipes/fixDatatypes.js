
db.recipes.find({likes: {$exists: true}}).forEach(function(obj) { 
    obj.likes = new NumberInt(obj.likes);
    db.recipes.save(obj);
});
db.recipes.find().forEach(function(element){
  element.pub = new Date(element.pub);
  db.recipes.save(element);
});

db.runCommand ( { compact: 'recipes', paddingFactor: 1.0 } );
db.recipes.reIndex();




