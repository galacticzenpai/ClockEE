/**
 * ClockEE Lightweight Exam Event Recorder
 * Captures millisecond-accurate student interaction telemetry for action replay.
 */

class ExamSessionRecorder {
  constructor(examId, studentId) {
    this.examId = examId;
    this.studentId = studentId;
    this.startTime = Date.now();
    this.events = [];
    this.recording = false;
  }

  start() {
    this.recording = true;
    this.events = [];
    this.startTime = Date.now();
    this.recordEvent('SESSION_START', { timestamp: this.startTime });
  }

  stop() {
    this.recording = false;
    this.recordEvent('SESSION_END', { timestamp: Date.now() });
    return this.exportEvents();
  }

  recordEvent(type, payload = {}) {
    if (!this.recording && type !== 'SESSION_START') return;
    const event = {
      t: Date.now() - this.startTime, // relative ms
      type: type,
      ...payload
    };
    this.events.push(event);
  }

  recordQuestionView(questionNum) {
    this.recordEvent('NAVIGATE_QUESTION', { q: questionNum });
  }

  recordOptionSelect(questionNum, optionIdx) {
    this.recordEvent('SELECT_OPTION', { q: questionNum, opt: optionIdx });
  }

  recordSaveNext(questionNum) {
    this.recordEvent('SAVE_NEXT', { q: questionNum });
  }

  recordMarkReview(questionNum) {
    this.recordEvent('MARK_REVIEW', { q: questionNum });
  }

  recordClear(questionNum) {
    this.recordEvent('CLEAR_ANSWER', { q: questionNum });
  }

  exportEvents() {
    return {
      exam_id: this.examId,
      student_id: this.studentId,
      total_duration_ms: Date.now() - this.startTime,
      total_events: this.events.length,
      events: this.events
    };
  }
}

if (typeof window !== 'undefined') {
  window.ExamSessionRecorder = ExamSessionRecorder;
}
