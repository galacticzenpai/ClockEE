/**
 * ClockEE Runtime State Mutation Guard
 * ES6 Proxy validator enforcing strict CBT state invariants.
 */

class CBTStateGuard {
  static createGuardedState(initialState = {}, totalQuestions = 180) {
    const validator = {
      set(target, prop, value) {
        if (prop === 'currentQuestion') {
          if (typeof value !== 'number' || value < 1 || value > totalQuestions) {
            console.error(`[StateGuard] Blocked invalid question mutation: ${value}. Out of bounds [1, ${totalQuestions}]`);
            return true; // Reject mutation silently or retain target[prop]
          }
        }

        if (prop === 'remainingSec') {
          if (typeof value !== 'number' || isNaN(value) || value < 0) {
            console.error(`[StateGuard] Blocked illegal remainingSec mutation: ${value}`);
            return true;
          }
        }

        if (prop === 'selectedOption') {
          if (value !== null && (typeof value !== 'number' || value < 1 || value > 4)) {
            console.error(`[StateGuard] Blocked illegal option index: ${value}`);
            return true;
          }
        }

        target[prop] = value;
        return true;
      }
    };

    return new Proxy({ ...initialState }, validator);
  }
}

if (typeof window !== 'undefined') {
  window.CBTStateGuard = CBTStateGuard;
}
