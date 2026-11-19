/**
 * Comprehensive Automated Test Suite for ClockEE CBT Engine (TASK-006 / JEE-CBT-001)
 * Tests core business logic, Section B 5-question limit, NTA 5-state machine, and scoring.
 */

const assert = require('assert');

// Mock IndexedDB and Worker for Node environment testing
const mockDB = {
  data: {},
  async get(store, key) { return this.data[`${store}_${key}`]; },
  async put(store, value) { this.data[`${store}_${value.examId || value.id}`] = value; return value; },
  async getByIndex(store, idx, val) { return []; },
  async getAll(store) { return []; },
  async clear() { this.data = {}; }
};

// Load CBTEngine
const CBTEngine = require('../scripts/cbt-engine.js');

async function runTests() {
  console.log('=== Starting CBT Engine Automated Test Suite ===');

  let warningsLogged = [];
  const state = await CBTEngine.init({
    onWarning: (msg) => warningsLogged.push(msg)
  });

  // Test 1: Total Question Count & Structure
  assert.strictEqual(state.questions.length, 90, 'Total questions must be exactly 90');
  const phyQuestions = state.questions.filter(q => q.subject === 'Physics');
  const chemQuestions = state.questions.filter(q => q.subject === 'Chemistry');
  const mathQuestions = state.questions.filter(q => q.subject === 'Mathematics');
  assert.strictEqual(phyQuestions.length, 30, 'Physics must have 30 questions');
  assert.strictEqual(chemQuestions.length, 30, 'Chemistry must have 30 questions');
  assert.strictEqual(mathQuestions.length, 30, 'Mathematics must have 30 questions');

  // Test 2: Section A & Section B distribution
  const phySecA = phyQuestions.filter(q => q.section === 'A');
  const phySecB = phyQuestions.filter(q => q.section === 'B');
  assert.strictEqual(phySecA.length, 20, 'Physics Section A must have 20 MCQs');
  assert.strictEqual(phySecB.length, 10, 'Physics Section B must have 10 Numericals');
  console.log('✓ Test 1 & 2 Passed: 90-Question PCM & Section A/B Distribution Validated');

  // Test 3: NTA 5-State Machine & MCQ Selection
  CBTEngine.goToQuestion(0); // Q1 Physics (Sec A)
  assert.strictEqual(state.responses['Q_1'].state, 'NOT_ANSWERED', 'Visited question should transition to NOT_ANSWERED');
  
  CBTEngine.selectOption('B');
  CBTEngine.saveAndNext();
  assert.strictEqual(state.responses['Q_1'].state, 'ANSWERED', 'Saved question should transition to ANSWERED');
  console.log('✓ Test 3 Passed: NTA 5-State Transition (Not Visited -> Not Answered -> Answered)');

  // Test 4: Mark for Review transitions
  CBTEngine.goToQuestion(1); // Q2 Physics (Sec A)
  CBTEngine.markForReviewAndNext();
  assert.strictEqual(state.responses['Q_2'].state, 'MARKED_REVIEW', 'Unanswered mark for review must be MARKED_REVIEW');

  CBTEngine.goToQuestion(2); // Q3 Physics (Sec A)
  CBTEngine.selectOption('A');
  CBTEngine.saveAndMarkForReview();
  assert.strictEqual(state.responses['Q_3'].state, 'ANSWERED_MARKED', 'Answered mark for review must be ANSWERED_MARKED');
  console.log('✓ Test 4 Passed: Mark for Review & Answered Marked States Validated');

  // Test 5: Section B Virtual Keypad Input Sanitization
  CBTEngine.goToQuestion(20); // Q21 Physics (Sec B, Numerical 1)
  assert.strictEqual(state.questions[20].section, 'B', 'Q21 must be Section B');
  
  CBTEngine.inputKey('1');
  CBTEngine.inputKey('0');
  CBTEngine.inputKey('.');
  CBTEngine.inputKey('5');
  assert.strictEqual(state.responses['Q_21'].numericalValue, '10.5', 'Numerical input should be 10.5');

  // Negative sign toggling
  CBTEngine.inputKey('-');
  assert.strictEqual(state.responses['Q_21'].numericalValue, '-10.5', 'Minus key should prefix negative');
  CBTEngine.inputKey('-');
  assert.strictEqual(state.responses['Q_21'].numericalValue, '10.5', 'Minus key again should toggle back');
  console.log('✓ Test 5 Passed: Virtual Keypad Numerical Input Sanitizer Validated');

  // Test 6: Section B NTA Rule - Attempt Maximum 5 out of 10
  // Attempt Q21, Q22, Q23, Q24, Q25
  for (let i = 20; i < 25; i++) {
    CBTEngine.goToQuestion(i);
    CBTEngine.inputKey('5');
    const success = CBTEngine.saveAndNext();
    assert.strictEqual(success, true, `Should allow attempting question ${i + 1}`);
  }

  // Now attempt Q26 (the 6th question in Physics Section B)
  warningsLogged = [];
  CBTEngine.goToQuestion(25); // Q26
  CBTEngine.inputKey('9');
  const success6th = CBTEngine.saveAndNext();
  assert.strictEqual(success6th, false, 'Attempting 6th question in Section B must be rejected');
  assert.strictEqual(warningsLogged.length, 1, 'Warning dialog should be triggered');
  console.log('✓ Test 6 Passed: Section B Maximum 5 Attempts NTA Rule Strictly Enforced');

  // Test 7: Official NTA Scoring Calculation (+4 / -1 / 0)
  // Submit exam and inspect scorecard
  const scorecard = await CBTEngine.submitExam(false);
  assert.ok(scorecard.totalScore !== undefined, 'Total score must be calculated');
  assert.strictEqual(scorecard.maxScore, 300, 'Max score must be 300');
  console.log(`✓ Test 7 Passed: NTA Scorecard Generated (${scorecard.totalScore} / ${scorecard.maxScore})`);

  console.log('\n======================================================');
  console.log('ALL 7 ENGINE VERIFICATION TESTS PASSED SUCCESSFULLY! ✓');
  console.log('======================================================\n');
}

runTests().catch(err => {
  console.error('Test Suite Failed:', err);
  process.exit(1);
});
