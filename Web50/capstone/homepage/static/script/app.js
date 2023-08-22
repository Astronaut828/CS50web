document.addEventListener('DOMContentLoaded', function() {
  const menu = document.querySelector('#mobile-menu');
  const menuLinks = document.querySelector('.nav-menu');

  menu.addEventListener('click', function() {
    menu.classList.toggle('is-active');
    menuLinks.classList.toggle('active');
  });

  // Modal items
  const modal = document.getElementById('email-modal');
  const openBtn = document.querySelector('.main-btn');
  const closeBtn = document.querySelector('.close-btn');

  // Click events
  openBtn.addEventListener('click', () => {
    modal.style.display = 'block';
    disableScroll();
  });

  closeBtn.addEventListener('click', () => {
    modal.style.display = 'none';
    enableScroll();
  });

  window.addEventListener('click', (e) => {
    if (e.target === modal) {
      modal.style.display = 'none';
      enableScroll();
    }
  });

  // Form validation
  const form = document.getElementById('form');
  const name = document.getElementById('name');
  const email = document.getElementById('email');
  const message = document.getElementById('message');

  // Show error message
  function showError(input, message) {
    const formValidation = input.parentElement;
    formValidation.className = 'form-validation error';

    const errorMessage = formValidation.querySelector('p');
    errorMessage.innerText = message;
  }

  // Show valid
  function showValid(input) {
    const formValidation = input.parentElement;
    formValidation.className = 'form-validation valid';
  }

  // Check required fields
  function checkRequired(inputArr) {
    inputArr.forEach(function(input) {
      if (input.value.trim() === '') {
        showError(input, `${getFieldName(input)} is required`);
      } else {
        showValid(input);
      }
    });
  }

  // Checking input length
  function checkLength(input, min, max) {
    if (input.value.length < min) {
      showError(input, `${getFieldName(input)} must be at least ${min} characters`);
    } else if (input.value.length > max) {
      showError(input, `${getFieldName(input)} must be less than ${max} characters`);
    } else {
      showValid(input);
    }
  }

  // Get field name
  function getFieldName(input) {
    return input.name.charAt(0).toUpperCase() + input.name.slice(1);
  }

  // Email verification for contact form
  function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  }

  // Event listener for form submission
  form.addEventListener('submit', (e) => {
    e.preventDefault(); // Prevent default form submission behavior

    // Call the validation functions
    checkRequired([name, email, message]);
    checkLength(message, 30, Infinity); // Minimum 30 characters for the message field
    checkLength(email, 3, 30);

    // Validate email address
    if (!isValidEmail(email.value)) {
      showError(email, 'Invalid email address');
    }

    // Check if any error messages exist
    if (document.querySelector('.error')) {
      // There are errors, do not submit the form
      return;
    }

    // The form is valid, so you can proceed with form submission
    form.submit(); // Submit the form
  });

  // Function to disable scrolling
  function disableScroll() {
    document.body.style.overflow = 'hidden';
  }

  // Function to enable scrolling
  function enableScroll() {
    document.body.style.overflow = '';
  }

  // Function to scale content box
  function scaleContentBox() {
    var windowHeight = window.innerHeight;
    var hero = document.querySelector('.hero');
    if (hero) {
      var heroHeight = hero.offsetHeight;
      var contentBox = document.querySelector('.content-box');
      var contentBoxHeight = Math.min(windowHeight * 0.4, heroHeight * 0.4);

      contentBox.style.maxHeight = contentBoxHeight + 'px';
    }
  }

  // Call the function initially and on window resize
  scaleContentBox();
  window.addEventListener('resize', scaleContentBox);



  // Landing page
  const videoDelay = 7000; // Delay before hiding the video
  const typewriterDelay = 3000; // Delay before starting the typewriter animation

  window.onload = function() {
    if (!localStorage.getItem('videoPlayed')) {
      document.getElementById('intro-gif').addEventListener('ended', function() {
        setTimeout(function() {
          document.getElementById('intro-gif').style.display = 'none';
          localStorage.setItem('videoPlayed', 'true'); // Set the flag to indicate the video has been played
          setTimeout(function() {
            document.getElementById('info').style.display = 'block';
            typeWriter();
          }, typewriterDelay);
        }, videoDelay);
      });
    } else {
      document.getElementById('intro-gif').style.display = 'none';
      document.getElementById('info').style.display = 'block';
      if (localStorage.getItem('animationCompleted')) {
        document.getElementById('text').innerHTML = str.replace(/<br>/g, '\n'); // add the text without animation
      }
    }
  };

  var str = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.<br>Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.<br>Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.<br>Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.<br>";
  var i = 0;
  var speed = 50;

  function typeWriter() {
    if (i < str.length) {
      if (str.charAt(i) == "<") {
        $('#text').html($('#text').html() + "<br>");
        i += 4;
      } else {
        $('#text').html($('#text').html() + str.charAt(i));
        i++;
      }
      setTimeout(typeWriter, speed);
    } else {
      localStorage.setItem('animationCompleted', 'true'); // Set the flag to indicate the animation has been completed
    }
  }

  // Check if the video has been played and the animation has been completed before
  if (localStorage.getItem('videoPlayed')) {
    document.getElementById('intro-gif').style.display = 'none';
    document.getElementById('info').style.display = 'block';
    if (localStorage.getItem('animationCompleted')) {
      document.getElementById('text').innerHTML = str.replace(/<br>/g, '\n'); // add the text without animation
    } else {
      setTimeout(function() {
        typeWriter();
      }, typewriterDelay);
    }
  } else {
    setTimeout(function() {
      document.getElementById('intro-gif').style.display = 'none';
      document.getElementById('info').style.display = 'block';
      setTimeout(function() {
        typeWriter();
      }, typewriterDelay);
      localStorage.setItem('videoPlayed', 'true'); // Set the flag to indicate the video has been played
    }, videoDelay);
  }
});