var bebop = require('node-bebop');

var drone = bebop.createClient();

try {
  drone.connect(function() {
    drone.takeOff();
    throw("We got an error mid-flight!");
    setTimeout(function() {
      drone.land();
    }, 5000);
  });
}
catch(err)
{
  // Ensures the drone lands if the code breaks
  drone.land();
  throw(err);
}
