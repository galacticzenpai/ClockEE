
let activeListener = null;

function createSignal(initialValue) {
  let value = initialValue;
  const subscribers = new Set();

  const read = () => {
    if (activeListener) subscribers.add(activeListener);
    return value;
  };

  const write = (newValue) => {
    value = typeof newValue === 'function' ? newValue(value) : newValue;
    [...subscribers].forEach(sub => sub.execute());
  };

  return [read, write];
}

function createEffect(fn) {
  const effect = {
    execute() {
      activeListener = effect;
      try {
        fn();
      } finally {
        activeListener = null;
      }
    }
  };
  effect.execute();
  return effect;
}

function createMemo(fn) {
  const [get, set] = createSignal(undefined);
  createEffect(() => set(fn()));
  return get;
}

// Verification Test: Diamond Dependency
const [count, setCount] = createSignal(1);
const double = createMemo(() => count() * 2);
const quadruple = createMemo(() => double() * 2);

let observed = [];
createEffect(() => {
  observed.push(quadruple());
});

console.log("Initial Quadruple:", quadruple());
setCount(2);
console.log("Updated Quadruple (count=2):", quadruple());
setCount(5);
console.log("Updated Quadruple (count=5):", quadruple());

if (quadruple() === 20 && observed.join(",") === "4,8,20") {
  console.log("PASS: OmniReactive Signal Engine diamond dependency test succeeded!");
} else {
  console.error("FAIL: Unexpected reactive state", observed);
  process.exit(1);
}
