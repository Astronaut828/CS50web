document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', () => compose_email());

  document.querySelector('#compose-form').addEventListener('submit', handleFormSubmit);

  // By default, load the inbox
  load_mailbox('inbox');
});


function compose_email(sender='', subject='', body='') {
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Pre-fill composition fields if sender, subject, and body are provided
  document.querySelector('#compose-recipients').value = sender;
  document.querySelector('#compose-subject').value = subject ? (subject.startsWith('Re: ') ? subject : 'Re: ' + subject) : '';
  const composeBody = document.querySelector('#compose-body');
  composeBody.value = body ? `\n\nOn ${new Date().toLocaleString()} ${sender} wrote:\n${body}` : '';

  // Place cursor in email body
  composeBody.focus();
  // Set cursor to the beginning of the body field
  setTimeout(() => composeBody.setSelectionRange(0, 0), 10);
}



function handleFormSubmit(event) {
  // Prevent the form from submitting !=POST
  event.preventDefault();

  // Get the values from the form
  let recipients = document.querySelector('#compose-recipients').value;
  let subject = document.querySelector('#compose-subject').value;
  let body = document.querySelector('#compose-body').value;

  // URL where to send the data
  let url = '/emails';

  // Fetch API to send data
  fetch(url, {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify({
          recipients: recipients,
          subject: subject,
          body: body
      })
  })
  .then(response => response.json())
  .then(data => {
      console.log('Success:', data);
      load_mailbox('sent');
  })
  .catch((error) => {
      console.error('Error:', error);
  });
}



function load_mailbox(mailbox) {
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Make request to server to get emails
  fetch(`/emails/${mailbox}`)
    .then(response => response.json())
    .then(emails => {
      // Loop through emails, add each one to the page
      emails.forEach(email => {
        // Create a div for each email
        const emailDiv = document.createElement('div');
        emailDiv.innerHTML = `
          <b>From:</b> ${email.sender} <br>
          <b>Subject:</b> ${email.subject} <br>
          <b>Timestamp:</b> ${email.timestamp}
        `;
        emailDiv.className = 'emailDiv';

        // If the email is unread / read, set background
        emailDiv.style.backgroundColor = email.read ? 'lightgray' : 'white';
        if (email.read) {
          emailDiv.classList.add('read'); //add checkmark
        }

        // Click to open email // function load_email(email_id)
        emailDiv.addEventListener('click', () => {
          load_email(email.id, mailbox);
        });

        // Add the email div to the page
        document.querySelector('#emails-view').append(emailDiv);
      });
    });
}


function load_email(email_id, mailbox) {
  // GET request to server / get the email's details
  fetch(`/emails/${email_id}`)
    .then(response => response.json())
    .then(email => {

      document.querySelector('#emails-view').innerHTML = '';

      // Create a div for the email details and add to page
      const emailDetails = document.createElement('div');
      emailDetails.innerHTML = `
        <b>From:</b> ${email.sender} <br>
        <b>To:</b> ${email.recipients.join(', ')} <br>
        <b>Subject:</b> ${email.subject} <br>
        <b>Timestamp:</b> ${email.timestamp} <br>
        <hr>
        ${email.body.replace(/\n/g, '<br>')}
      `; // Replace /n with a new line <br> globally

      emailDetails.className = 'emailDiv';
      document.querySelector('#emails-view').appendChild(emailDetails);

      if (mailbox !== 'sent') {
        // Archive Button
        const archiveButton = document.createElement('button');
        archiveButton.textContent = email.archived ? 'Unarchive' : 'Archive';
        archiveButton.className = 'archive-button';
        archiveButton.addEventListener('click', () => {
          toggle_archive(email_id, !email.archived);
        });
        document.querySelector('#emails-view').appendChild(archiveButton);

        // Reply Button
        const replyButton = document.createElement('button');
        replyButton.textContent = 'Reply';
        replyButton.className = 'reply-button';
        replyButton.addEventListener('click', () => {
          compose_email(email.sender, 'Re: ' + email.subject, email.body);
        });
        document.querySelector('#emails-view').appendChild(replyButton);
      }

      // Mark email as read
      fetch(`/emails/${email_id}`, {
        method: 'PUT',
        body: JSON.stringify({
          read: true
        })
      });
    });
}

// Archiving email
function toggle_archive(email_id, archive) {
  fetch(`/emails/${email_id}`, {
    method: 'PUT',
    body: JSON.stringify({
      archived: archive
    })
  })
    .then(() => {
      load_mailbox('inbox'); // Load the inbox after archiving/unarchiving
    })
    .catch(error => console.error('Error:', error));
}

