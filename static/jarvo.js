const chatBox=document.getElementById("chatBox");
const userInput=document.getElementById("userInput");
const typingIndicator=document.getElementById("typingIndicator");

function startVoiceInput(){
  const recognition=new(window.SpeechRecognition||window.webkitSpeechRecognition)();
  recognition.lang="en-US";
  recognition.start();
  recognition.onresult=(event)=>{
    const transcript=event.results[0][0].transcript;
    userInput.value=transcript;
    sendMessage();
  };
}


function sendMessage(){
  const userInput=document.getElementById("userInput");
  const message=userInput.value.trim();
  if(!message)return;

  const chatBox=document.getElementById("chatBox");
  const typing=document.getElementById("typingIndicator");

 
  const userMsg=document.createElement("div");
  userMsg.className="message user";
  userMsg.textContent=message;
  chatBox.appendChild(userMsg);

  //clearing the input field
  userInput.value="";
  typing.style.display="inline-block";

  fetch("/chat",{
    method:"POST",
    headers:{"Content-Type":"application/json"},
    body:JSON.stringify({message})
  })
    .then(res=>res.json())
    .then(data=>{
      typing.style.display="none";
      const botMsg=document.createElement("div");
      botMsg.className="message bot";
      botMsg.textContent=data.reply;
      chatBox.appendChild(botMsg);
      chatBox.scrollTop=chatBox.scrollHeight;
    });
}


function appendMessage(sender,text,emoji) {
  const msg=document.createElement("div");
  msg.innerHTML=`<strong>${emoji} ${sender}:</strong> ${text}`;
  msg.style.marginBottom="10px";
  chatBox.appendChild(msg);
  chatBox.scrollTop=chatBox.scrollHeight;
}
function toggleTheme(){
  document.body.classList.toggle("dark");
}
