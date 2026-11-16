/**
 * ClockEE Keyboard-First Navigation Controller
 * Dispatches official NTA CBT exam hotkeys.
 */

class CBTKeyboardController {
  constructor(handlers = {}) {
    this.handlers = {
      onSelectOption: handlers.onSelectOption || ((optIdx) => console.log('Select option:', optIdx)),
      onSaveNext: handlers.onSaveNext || (() => console.log('Save & Next')),
      onMarkReview: handlers.onMarkReview || (() => console.log('Mark for Review')),
      onClear: handlers.onClear || (() => console.log('Clear')),
      onPrev: handlers.onPrev || (() => console.log('Prev')),
      onNext: handlers.onNext || (() => console.log('Next')),
      onToggleHUD: handlers.onToggleHUD || (() => console.log('Toggle HUD'))
    };
    this.enabled = true;
    this.boundListener = this.handleKeydown.bind(this);
    this.attach();
  }

  attach() {
    window.addEventListener('keydown', this.boundListener);
  }

  detach() {
    window.removeEventListener('keydown', this.boundListener);
  }

  handleKeydown(e) {
    if (!this.enabled) return;
    // Don't intercept if focus is inside an input, textarea or contenteditable
    const tag = (e.target && e.target.tagName) || '';
    if (tag === 'INPUT' || tag === 'TEXTAREA' || e.target.isContentEditable) {
      return;
    }

    const key = e.key;
    switch (key) {
      case '1':
      case '2':
      case '3':
      case '4':
        e.preventDefault();
        this.handlers.onSelectOption(parseInt(key, 10));
        break;
      case 's':
      case 'S':
      case 'Enter':
        e.preventDefault();
        this.handlers.onSaveNext();
        break;
      case 'm':
      case 'M':
      case 'r':
      case 'R':
        e.preventDefault();
        this.handlers.onMarkReview();
        break;
      case 'c':
      case 'C':
        e.preventDefault();
        this.handlers.onClear();
        break;
      case 'p':
      case 'P':
      case 'ArrowLeft':
        e.preventDefault();
        this.handlers.onPrev();
        break;
      case 'n':
      case 'N':
      case 'ArrowRight':
        e.preventDefault();
        this.handlers.onNext();
        break;
      case '?':
        e.preventDefault();
        this.handlers.onToggleHUD();
        break;
    }
  }
}

if (typeof window !== 'undefined') {
  window.CBTKeyboardController = CBTKeyboardController;
}
