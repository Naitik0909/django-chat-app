document.querySelector('.chat[data-chat=person2]').classList.add('active-chat');
document.querySelector('.person[data-chat=person2]').classList.add('active');

let friends = {
  list: document.querySelector('ul.people'),
  all: document.querySelectorAll('.left .person'),
  name: '' },

chat = {
  container: document.querySelector('.container .right'),
  current: null,
  person: null,
  name: document.querySelector('.container .right .top .name') };


friends.all.forEach(f => {
  f.addEventListener('mousedown', () => {
    f.classList.contains('active') || setAciveChat(f);
  });
});

function setAciveChat(f) {
  friends.list.querySelector('.active').classList.remove('active');
  f.classList.add('active');
  chat.current = chat.container.querySelector('.active-chat');
  chat.person = f.getAttribute('data-chat');
  chat.current.classList.remove('active-chat');
  chat.container.querySelector('[data-chat="' + chat.person + '"]').classList.add('active-chat');
  friends.name = f.querySelector('.name').innerText;
  chat.name.innerHTML = friends.name;
}

window.onload = () => {
  console.log('heere');
  const token="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjUyMDAxNjMzLCJpYXQiOjE2NTE4Mjg4MzMsImp0aSI6IjA5MDI0MTJhMjA4OTQ2YzJiMmNlNDhlNDRjNGIwYzJjIiwidXNlcl9pZCI6M30.e2vwlQr0upw06vrQahb14cJJX6S1XTvxyWswK_drERo";
  const userAction = async () => {
     const response=await fetch('http://127.0.0.1:8000/chat_screen/?access=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjUyMDAxNjMzLCJpYXQiOjE2NTE4Mjg4MzMsImp0aSI6IjA5MDI0MTJhMjA4OTQ2YzJiMmNlNDhlNDRjNGIwYzJjIiwidXNlcl9pZCI6M30.e2vwlQr0upw06vrQahb14cJJX6S1XTvxyWswK_drERo'
      );

    const myJson = await response.json(); //extract JSON from the http response
    console.log(myJson); // log the result

  }
  userAction();
}