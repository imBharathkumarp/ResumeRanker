fetch('https://resumeranker-89kg.onrender.com/upload', {
    method: 'POST',
    body: formData
  })
  .then(response => response.json())
  .then(data => {
    console.log('Score:', data.score);
  })
  .catch(error => {
    console.error('Error:', error);
  });
