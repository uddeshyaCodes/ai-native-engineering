console.log("A");
process.nextTick(() => {
    console.log("B");
});
console.log("C");

/* 
nextTick vs setImmediate
nextTick is a micro task and setImmediate is a macro task.
So the order of execution is:
1. A
2. C
3. B
*/