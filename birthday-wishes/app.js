(() => {
  const screens = [...document.querySelectorAll('.screen')];
  const footer = document.getElementById('siteFooter');
  const passcodeInput = document.getElementById('passcodeInput');
  const passcodeMessage = document.getElementById('passcodeMessage');
  const tryAgainButton = document.getElementById('tryAgainButton');
  const wrongMark = document.getElementById('wrongMark');
  const cells = [...document.querySelectorAll('.digit-cell')];
  const keypadButtons = [...document.querySelectorAll('[data-key]')];
  const code = '1224';
  let digits = '';
  let noCount = 0;
  let yesCount = 0;

  const showScreen = (id) => {
    screens.forEach((screen) => {
      const active = screen.id === id;
      screen.hidden = !active;
      screen.classList.toggle('is-active', active);
    });
    footer.hidden = id !== 'giftsScreen';
    if (id === 'passcodeScreen') {
      resetPasscode();
      window.setTimeout(() => passcodeInput.focus(), 60);
    }
  };

  document.getElementById('beginButton').addEventListener('click', () => showScreen('passcodeScreen'));
  document.getElementById('backToGifts').addEventListener('click', () => showScreen('giftsScreen'));

  function updateDigits() {
    cells.forEach((cell, index) => {
      cell.textContent = digits[index] ? '•' : '';
      cell.classList.toggle('filled', Boolean(digits[index]));
    });
    passcodeInput.value = digits;
  }

  function resetPasscode() {
    digits = '';
    updateDigits();
    passcodeMessage.textContent = 'Tap the buttons or use your keyboard.';
    passcodeMessage.classList.remove('is-error');
    tryAgainButton.hidden = true;
    keypadButtons.forEach((button) => { button.disabled = false; });
    wrongMark.classList.remove('is-visible');
  }

  function submitPasscode() {
    if (digits.length !== 4) return;
    if (digits === code) {
      passcodeMessage.textContent = 'Correct. You are officially birthday-authorized.';
      passcodeMessage.classList.remove('is-error');
      window.setTimeout(() => showScreen('promptScreen'), 500);
      return;
    }
    passcodeMessage.textContent = 'Oops! Wrong passcode. Try again, birthday genius.';
    passcodeMessage.classList.add('is-error');
    wrongMark.classList.add('is-visible');
    tryAgainButton.hidden = false;
    keypadButtons.forEach((button) => { button.disabled = true; });
  }

  function addDigit(value) {
    if (digits.length >= 4 || tryAgainButton.hidden === false) return;
    digits += value;
    updateDigits();
    if (digits.length === 4) submitPasscode();
  }

  keypadButtons.forEach((button) => {
    button.addEventListener('click', () => {
      const key = button.dataset.key;
      if (key === 'backspace') {
        if (tryAgainButton.hidden) {
          digits = digits.slice(0, -1);
          updateDigits();
        }
      } else addDigit(key);
    });
  });
  passcodeInput.addEventListener('input', () => {
    if (!tryAgainButton.hidden) return;
    digits = passcodeInput.value.replace(/\D/g, '').slice(0, 4);
    updateDigits();
    if (digits.length === 4) submitPasscode();
  });
  document.addEventListener('keydown', (event) => {
    if (document.getElementById('passcodeScreen').hidden) return;
    if (/^\d$/.test(event.key)) {
      if (event.target === passcodeInput) event.preventDefault();
      addDigit(event.key);
    }
    else if (event.key === 'Backspace' && tryAgainButton.hidden) {
      if (event.target === passcodeInput) event.preventDefault();
      digits = digits.slice(0, -1);
      updateDigits();
    }
  });
  tryAgainButton.addEventListener('click', () => {
    resetPasscode();
    passcodeInput.focus();
  });

  const promptTitle = document.getElementById('promptTitle');
  const promptQuestion = document.getElementById('promptQuestion');
  const promptAside = document.getElementById('promptAside');
  const yesButton = document.getElementById('yesButton');
  const noButton = document.getElementById('noButton');
  noButton.addEventListener('click', () => {
    if (yesCount > 0) {
      showScreen('giftsScreen');
      return;
    }
    noCount += 1;
    if (noCount === 1) {
      promptQuestion.textContent = 'Are you sure? The gift is making a sad little face.';
      promptAside.textContent = 'This is your chance to make the gift feel loved.';
      noButton.textContent = 'Still no';
      noButton.animate([{ transform: 'translateX(0)' }, { transform: 'translateX(12px)' }, { transform: 'translateX(0)' }], { duration: 300 });
    } else if (noCount === 2) {
      promptQuestion.textContent = 'Wow. Playing hard to get with a birthday present.';
      promptAside.textContent = 'Fine. The “no” button has changed its mind for you.';
      noButton.textContent = 'Okay, YES';
      noButton.classList.remove('button--outline');
      noButton.classList.add('button--coral');
    } else {
      showScreen('giftsScreen');
    }
  });
  yesButton.addEventListener('click', () => {
    yesCount += 1;
    if (yesCount === 1) {
      promptTitle.innerHTML = 'You said yes.<br>Your taste is impeccable.';
      promptQuestion.textContent = 'Are you REALLY excited?';
      promptAside.textContent = 'Correct answers: YES and also YES.';
      yesButton.textContent = 'YES, obviously';
      noButton.textContent = 'YES, obviously';
      noButton.classList.remove('button--outline');
      noButton.classList.add('button--coral');
    } else showScreen('giftsScreen');
  });
  const giftDialog = document.getElementById('giftDialog');
  const giftViews = [...document.querySelectorAll('.gift-view')];
  document.querySelectorAll('[data-gift]').forEach((button) => {
    button.addEventListener('click', () => openGift(button.dataset.gift));
  });
  function openGift(kind) {
    giftViews.forEach((view) => { view.hidden = true; });
    const view = document.getElementById(`${kind}View`);
    if (!view) return;
    view.hidden = false;
    giftDialog.setAttribute('aria-labelledby', {
      memories: 'dialogTitle',
      letter: 'letterTitle',
      cake: 'cakeTitle',
    }[kind]);
    giftDialog.showModal();
    if (kind === 'cake') resetCake();
  }
  document.querySelectorAll('[data-close-dialog]').forEach((button) => button.addEventListener('click', () => giftDialog.close()));
  giftDialog.addEventListener('click', (event) => {
    if (event.target === giftDialog) giftDialog.close();
  });

  const memoryRail = document.getElementById('memoryRail');
  document.querySelectorAll('[data-gallery-step]').forEach((button) => {
    button.addEventListener('click', () => memoryRail.scrollBy({ left: Number(button.dataset.galleryStep) * 220, behavior: 'smooth' }));
  });
  const photoDialog = document.getElementById('photoDialog');
  const photoCaptions = ['main character energy', 'professional cozy person', 'fashion icon (allegedly)', 'after one (1) activity'];
  document.querySelectorAll('[data-photo]').forEach((button) => {
    button.addEventListener('click', () => {
      const image = button.querySelector('img');
      document.getElementById('largePhoto').src = image.src;
      document.getElementById('largePhoto').alt = image.alt;
      document.getElementById('largePhotoCaption').textContent = photoCaptions[Number(button.dataset.photo)];
      photoDialog.showModal();
    });
  });
  document.querySelector('[data-close-photo]').addEventListener('click', () => photoDialog.close());
  photoDialog.addEventListener('click', (event) => {
    if (event.target === photoDialog) photoDialog.close();
  });

  const candles = [...document.querySelectorAll('.candle')];
  const cakeTitle = document.getElementById('cakeTitle');
  const cakeInstruction = document.getElementById('cakeInstruction');
  const wishMessage = document.getElementById('wishMessage');
  const magicWand = document.getElementById('magicWand');
  const relightCake = document.getElementById('relightCake');
  candles.forEach((candle) => candle.addEventListener('click', () => {
    candle.classList.add('is-out');
    candle.setAttribute('aria-pressed', 'true');
    checkCandles();
  }));
  magicWand.addEventListener('click', () => {
    candles.forEach((candle) => {
      candle.classList.add('is-out');
      candle.setAttribute('aria-pressed', 'true');
    });
    checkCandles();
  });
  function checkCandles() {
    if (!candles.every((candle) => candle.classList.contains('is-out'))) return;
    cakeTitle.textContent = 'HAPPY BIRTHDAY!';
    cakeInstruction.textContent = 'Wish made. The universe has received your very specific cake-based request.';
    wishMessage.hidden = false;
    magicWand.hidden = true;
    relightCake.hidden = false;
  }
  function resetCake() {
    candles.forEach((candle) => {
      candle.classList.remove('is-out');
      candle.setAttribute('aria-pressed', 'false');
    });
    cakeTitle.textContent = 'MAKE A WISH';
    cakeInstruction.textContent = 'Tap every candle to blow it out — or use the magic wand for the lazy option.';
    wishMessage.hidden = true;
    magicWand.hidden = false;
    relightCake.hidden = true;
  }
  relightCake.addEventListener('click', resetCake);

  const confetti = document.getElementById('confetti');
  const colors = ['#e46a83', '#e5b85e', '#7bb6ae', '#aa87ba', '#f3a8bd'];
  for (let index = 0; index < 28; index += 1) {
    const piece = document.createElement('span');
    piece.className = 'confetti-piece';
    piece.style.left = `${(index * 37 + 7) % 100}%`;
    piece.style.backgroundColor = colors[index % colors.length];
    piece.style.setProperty('--fall-time', `${5 + (index % 7)}s`);
    piece.style.setProperty('--delay', `${-(index % 9)}s`);
    piece.style.setProperty('--drift', `${((index % 5) - 2) * 18}px`);
    confetti.appendChild(piece);
  }
})();
