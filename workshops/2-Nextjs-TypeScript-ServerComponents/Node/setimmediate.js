console.log("A");
setTimeout(() => {
    console.log("D");
}, 0);
setImmediate(() => {
    console.log("C");
});
console.log("B");

/* 
setImmediate vs setTimeout
setImmediate is a macro task and setTimeout is a micro task.
So the order of execution is:
1. A
2. B
3. C
4. D
*/