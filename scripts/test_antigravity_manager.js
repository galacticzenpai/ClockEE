/**
 * scripts/test_antigravity_manager.js
 * Verification suite for antigravity_manager.html functional logic
 */

const fs = require('fs');
const path = require('path');

const managerHtmlPath = path.join(__dirname, '..', 'antigravity_manager.html');
const managerStatePath = path.join(__dirname, '..', 'mesh', 'manager_state.json');

console.log('--- [TEST 1] Verifying File Integrity & Parsing ---');
if (!fs.existsSync(managerHtmlPath)) {
  console.error('FAIL: antigravity_manager.html does not exist');
  process.exit(1);
}
if (!fs.existsSync(managerStatePath)) {
  console.error('FAIL: mesh/manager_state.json does not exist');
  process.exit(1);
}

const htmlContent = fs.readFileSync(managerHtmlPath, 'utf8');
const stateData = JSON.parse(fs.readFileSync(managerStatePath, 'utf8'));

console.log('PASS: Files loaded successfully. State version:', stateData.version);

console.log('\n--- [TEST 2] Verifying Interactive Element Bindings in HTML ---');
const requiredElements = [
  'id="mesh-svg-canvas"',
  'id="svg-vectors-group"',
  'id="svg-nodes-group"',
  'id="hud-active-sprint"',
  'id="hud-next-task"',
  'id="hud-trello-stage"',
  'id="mesh-sync-text"',
  'id="last-sync-time"',
  'id="log-search-input"',
  'id="logs-filter-stats"',
  'id="logs-cards-container"',
  'id="swarms-grid-container"',
  'id="chat-messages-stream"',
  'id="chat-message-input"',
  'id="chan-all-hands"',
  'id="chan-delegates-lounge"',
  'id="chan-p1-staggered-handoffs"',
  'id="view-overview"',
  'id="view-logs"',
  'id="view-chat"',
  'onclick="toggleAllLogCards(true)"',
  'onclick="toggleAllLogCards(false)"',
  'onclick="sendMockMessage()"'
];

for (const el of requiredElements) {
  if (!htmlContent.includes(el)) {
    console.error(`FAIL: Missing required DOM element: ${el}`);
    process.exit(1);
  }
}
console.log('PASS: All 23 required interactive DOM targets confirmed.');

console.log('\n--- [TEST 3] Verifying JavaScript Logic Specifications ---');
const requiredLogic = [
  'localStorage.getItem(\'antigravity_mesh_state\')',
  'localStorage.setItem(\'antigravity_mesh_state\'',
  'localStorage.getItem(\'antigravity_custom_chat_messages\')',
  'localStorage.setItem(\'antigravity_custom_chat_messages\'',
  'localStorage.setItem(\'antigravity_active_channel\'',
  'data-convid',
  'animateMotion',
  'showNodeDetailModal',
  'card-highlighted',
  'toggleAllLogCards',
  'copyNodePayload',
  'CACHED (OFFLINE FALLBACK)'
];

for (const logic of requiredLogic) {
  if (!htmlContent.includes(logic)) {
    console.error(`FAIL: Missing required script logic: ${logic}`);
    process.exit(1);
  }
}
console.log('PASS: All required script logic patterns verified.');

console.log('\n--- [TEST 4] Simulating Mock Mesh State Parsing & Node Profiles ---');
const nodes = Object.keys(stateData.nodes);
if (nodes.length !== 10) {
  console.error(`FAIL: Expected 10 nodes, found ${nodes.length}`);
  process.exit(1);
}
console.log(`PASS: Confirmed 10 nodes in manager state: ${nodes.join(', ')}`);

console.log('\n=== ALL PHASE 3 / P2 COCKPIT FUNCTIONAL VERIFICATIONS PASSED ===');
