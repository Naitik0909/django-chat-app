
var chatSocket = null;


function findGetParameter(parameterName) {
  var result = null,
      tmp = [];
  location.search
      .substr(1)
      .split("&")
      .forEach(function (item) {
        tmp = item.split("=");
        if (tmp[0] === parameterName) result = decodeURIComponent(tmp[1]);
      });
  return result;
}

window.onload = () => {
  // console.log('heere');
  const token="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjUyMDAxNjMzLCJpYXQiOjE2NTE4Mjg4MzMsImp0aSI6IjA5MDI0MTJhMjA4OTQ2YzJiMmNlNDhlNDRjNGIwYzJjIiwidXNlcl9pZCI6M30.e2vwlQr0upw06vrQahb14cJJX6S1XTvxyWswK_drERo";
  const userAction = async () => {
     const response=await fetch('http://127.0.0.1:8000/chat_screen/?access=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjUyMTA2NzM3LCJpYXQiOjE2NTE5MzM5MzcsImp0aSI6ImUyM2ZmZDU2OTM0NDQyYzliMjdiMDA3NTQ3ZmViM2Y0IiwidXNlcl9pZCI6M30.XJx29e4-9v_JsWyxsuObSaRqZAUkgvDlIeYQ9CnN1wU'
      );

    const myJson = await response.json(); //extract JSON from the http response
    // console.log(myJson); // log the result
    for(let i=0;i<myJson.length;i++){
      $("#people").append(`
      <li class="person" data-chat="person`+(myJson[i].room).toString(10)+`">
        <img src="https://s3-us-west-2.amazonaws.com/s.cdpn.io/382994/thomas.jpg" alt="" />
        <span class="name">`+myJson[i].user_name+`</span><span class="time">2:09 PM</span>
        <span class="preview">I was wondering...</span>
      </li>`);
        // console.log(data.user_name);
    }

    // Prev code

    // make dynamic
    document.querySelector('.chat[data-chat=person3]').classList.add('active-chat');
    document.querySelector('.person[data-chat=person3]').classList.add('active');

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

    function setAciveChat(f){
      // MAKE DYNAMIC

      var USER_ID = findGetParameter('user_id');
      var room_id = f.getAttribute('data-chat').slice(6, 7);

      // ON CLICKING CHAT WINDOW

      chatSocket = new WebSocket(
          'ws://'
          + window.location.host
          + '/ws/chat/'
          + room_id
          + '/'
          + '?access=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjUxNzM1MjMwLCJpYXQiOjE2NTE1NjI0MzAsImp0aSI6IjgzYzFhMjhjZGQ5YzRlMDhhMTIyNzZmODRlNjE5NmJiIiwidXNlcl9pZCI6MX0.16cUyDr2VhkFvcNjYSW34kIQMhhETnsD85WbXCLGsP8'
      );

         // When someone(anyone) sends message-
    chatSocket.onmessage = function(e) {
      const data = JSON.parse(e.data);
        // add new message to chatbox
        console.log("RECEIVED A MESSAGE- ");
        console.log(data);
        if(data.sender==USER_ID){
          $('.active-chat').append(`
                <div class="bubble me">
                    `+data.message+`
                </div>
                
            `);
        }
        else{
          $('.active-chat').append(`
                <div class="bubble you">
                    `+data.message+`
                </div>
                
            `);
        }
          
    };

      friends.list.querySelector('.active').classList.remove('active');
      f.classList.add('active');
      chat.current = chat.container.querySelector('.active-chat');
      chat.person = f.getAttribute('data-chat');
      chat.current.classList.remove('active-chat');
      // chat.container.querySelector('[data-chat="' + chat.person + '"]').classList.add('active-chat');
      // friends.name = f.querySelector('.name').innerText;
      // chat.name.innerHTML = friends.name;
      // console.log(chat.person.slice(6, 7))
      const getReq = async () => {
        // MAKE DYNAMIC
        const response=await fetch('http://127.0.0.1:8000/view_messages/?room_id='+room_id+'&access=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjUyMTA2NzM3LCJpYXQiOjE2NTE5MzM5MzcsImp0aSI6ImUyM2ZmZDU2OTM0NDQyYzliMjdiMDA3NTQ3ZmViM2Y0IiwidXNlcl9pZCI6M30.XJx29e4-9v_JsWyxsuObSaRqZAUkgvDlIeYQ9CnN1wU'
      );

      const myJson = await response.json(); //extract JSON from the http response
        // console.log(myJson); // log the result

        if(myJson.length==0){
          $('.right').append(`
        <div class="chat active-chat" data-chat="`+chat.person+`">
            <div>No messages</div>
            
        </div>
        `)
        }
        else{

          $('.right').append(`
            <div class="chat active-chat" data-chat="`+chat.person+`">
                <div class="conversation-start">
                    <span>`+myJson[0].sent_at_date+`, `+myJson[0].sent_at_time+`</span>
                </div>
            </div>
            `);

          for(var i=0;i<myJson.length;i++){
            if(myJson[i].sender==USER_ID){
              
              $('.active-chat').append(`
              <div class="bubble me">
                 `+myJson[i].message+`
              </div>
              
              `);
            }
            else{

              $('.active-chat').append(`
                  <div class="bubble you">
                     `+myJson[i].message+`
                  </div>
                  
              `);
            }
          }
        }


    }
      
      getReq();
      
      
    }



  }
  userAction();

}


function sendNewMessage(){

  USER_ID = findGetParameter('user_id');

  // MAKE DYNAMIC
  // var USER_ID = "3";
  var message = $('#message-content').val();
  // console.log(message);
  var room_id = $('.active-chat').attr('data-chat').slice(6, 7);
  console.log(room_id, message, USER_ID);
  // SEND MESSAGE TO ONLINE STREAM/SOCKET
    chatSocket.send(JSON.stringify({
        'message': message,
        'room_id': room_id,
        'sender': USER_ID,
        'sender_type': '0',
    }));

    $('#message-content').val('');


        // When someone(anyone) sends message-
    // chatSocket.onmessage = function(e) {
    //   const data = JSON.parse(e.data);
    //     // add new message to chatbox
    //     console.log("RECEIVED A MESSAGE- ");
    //     console.log(data);
    //     if(data.sender==USER_ID){
    //       $('.active-chat').append(`
    //             <div class="bubble me">
    //                 `+data.message+`
    //             </div>
                
    //         `);
    //     }
    //     else{
    //       $('.active-chat').append(`
    //             <div class="bubble you">
    //                 `+data.message+`
    //             </div>
                
    //         `);
    //     }
          
    // };

// MAKE DYNAMIC- DISCONNECT USEFROM SOCKET

}

document.querySelector('#message-content').onkeyup = function(e) {
  if (e.keyCode === 13) {  // enter, return
      document.querySelector('#message-content').click();
  }
};
