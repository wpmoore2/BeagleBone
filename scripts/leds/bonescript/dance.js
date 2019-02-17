// Turn on all or particular LED

var b=require('bonescript');

b.pinMode('USR0', 'out');
b.pinMode('USR1', 'out');
b.pinMode('USR2', 'out');
b.pinMode('USR3', 'out');

led_list = [1, 1, 2, 3, 1, 3, 2, 1, 1, 2, 3, 1, 0];
// led_list = [1, 1, 2]
rate = .2
var i = 0;
for (i; i < led_list.length; i++) {
    led = 'USR' + led_list[i];
    b.digitalWrite(led, 1);
    sleep(rate)
    setTimeout(turn_off_led(led), 1000)
}


function sleep(seconds) {
  var waitTill = new Date(new Date().getTime() + seconds * 1000);
  while(waitTill > new Date()){}
}
function turn_off_led(led) {
    b.digitalWrite(led, 0);
    sleep(rate)
}
