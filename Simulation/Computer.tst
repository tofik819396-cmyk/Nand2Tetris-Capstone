load Computer.hdl,
output-file Computer.out,
compare-with Computer.cmp,
output-list time%S1.4.1 PC%D1.5.1 instruction%B1.16.1 writeM%B1.1.1 addressM%D1.5.1 outM%D1.5.1;

// Run cycles to observe keyboard echo loop execution
repeat 50 {
    tick, tock, output;
}