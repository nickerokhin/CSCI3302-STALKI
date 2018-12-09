var bebop = require('node-bebop');

var drone = bebop.createClient();

try {
  drone.connect(function() {
    drone.takeOff();

    console.log(1);
    setTimeout(function(){
      console.log(2);
      // throw("We got an error mid-flight!");
      drone.land();
    }, 5000);
  });
}
catch(ex)
{
  console.log(3);
  // Ensures the drone lands if the code breaks
  drone.land();
  console.log(4);
  setTimeout(function(){
    callback(ex);
  }, 5000);
}
