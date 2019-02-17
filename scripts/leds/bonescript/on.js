// Turn on all or particular LED

var b=require('bonescript');

b.pinMode('USR0', 'out');
b.pinMode('USR1', 'out');
b.pinMode('USR2', 'out');
b.pinMode('USR3', 'out');
b.digitalWrite('USR0', 1);
b.digitalWrite('USR1', 1);
b.digitalWrite('USR2', 1);
b.digitalWrite('USR3', 1);
