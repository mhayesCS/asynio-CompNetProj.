# Async IO takes long waiting periods in which functions would otherwise be blocking and allows other functions to run during that downtime. At the heart of async IO are coroutines. A coroutine is a specialized version of a Python generator function.This Project will entain Chaining Coroutines. A key feature of coroutines is that they can be chained together. (Remember, a coroutine object is awaitable, so another coroutine can await it.) This allows you to break programs into smaller, manageable, recyclable coroutines