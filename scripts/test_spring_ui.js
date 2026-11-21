
function calcInnerRadius(outerRadius, padding) {
  const inner = outerRadius - padding;
  return inner > 0 ? inner : 0;
}

const cases = [
  { outer: 24, pad: 8, expected: 16 },
  { outer: 16, pad: 16, expected: 0 },
  { outer: 12, pad: 16, expected: 0 },
  { outer: 32, pad: 12, expected: 20 },
];

for (const c of cases) {
  const result = calcInnerRadius(c.outer, c.pad);
  if (result !== c.expected) {
    throw new Error(`Radius mismatch: outer=${c.outer}, pad=${c.pad}, got=${result}, expected=${c.expected}`);
  }
}

function checkDampingRatio(stiffness, damping, mass = 1) {
  const criticalDamping = 2 * Math.sqrt(mass * stiffness);
  const zeta = damping / criticalDamping;
  return { criticalDamping, zeta };
}

const preset1 = checkDampingRatio(400, 40, 1);
if (Math.abs(preset1.zeta - 1.0) < 0.001) {
  console.log("PASS: Spring dynamics damping ratio zeta=1.0 critically damped preset verified!");
} else {
  throw new Error("Spring preset error: " + JSON.stringify(preset1));
}

console.log("PASS: Nested Corner Radius Law and Spring Formulas verified successfully!");
