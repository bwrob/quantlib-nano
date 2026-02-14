ate, at which point this object
   would be recalculated too.  After recalculation, this object would
   again forward the first notification received.  Although not always
   correct, this behavior is a lot faster and thus is the current
   default.
*/
#ifndef QL_FASTER_LAZY_OBJECTS