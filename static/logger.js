var last_timestamp = 0;
var list_data = [];
const moover_keys = [37, 38, 39, 40, 32, 13];
const moover_labels = [ ];


function keydown(event) {
  var keycode = event.keyCode;
  var key = event.key;
  var timecode = event.timeStamp;
  var pressed = 0;
  // Ici, si la touche est espace, envoyer les données
  // Ce système ignore le cas ou une touche est "unpress" après le press de la touche espace
  
  if (key === ' ') {
    //ADD the length of the text at the last event in the list_data
    const text = document.getElementById('text-input').value;
    list_data[list_data.length - 1]["text"] = text;
    send_data(document.cookie.substring(11), list_data);
    list_data = [];
  }
  // Ici, ajouter la donée à list_data en json
  list_data.push({
    "pressed": pressed,
    "timestamp": timecode,
    "keycode": keycode,
    "char": key,
    "pos": event.location,
    // Ce calcul ignore le fait que on peut presser des touches dans le mauvais ordre. Mieux vaudrai =t le recalculer mais bref. 
    "time_elapsed": timecode - last_timestamp,
    "caret_pos" : checkcaret(event) // On ajoute la position du curseur seulement quand la touche est appuyée
  })
  if (key==" ") {
    list_data[list_data.length - 1]["text_length"] = document.getElementById('text-input').value.length;
  }
  last_timestamp = timecode;
}

function keyup(event) {
  var keycode = event.keyCode;
  var key = event.key;
  var timecode = event.timeStamp;
  var pressed = 1;
  list_data.push({
    "pressed": pressed,
    "timestamp": timecode,
    "keycode": keycode,
    "char": key,
    "pos": event.location,
    "time_elapsed": timecode - last_timestamp
  })
  //send_data(document.cookie.substring(11), "DEFAULT", pressed, timecode, keycode, key, event.location, timecode - last_timestamp);
  last_timestamp = timecode;
}

function send_data(session_id, data) {
  var username = document.getElementById('name').value;
  console.log(data);
  const text = document.getElementById('text-input').value;

  var resp;
  fetch('http://127.0.0.1:5000/text-data', {
    method: 'POST',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(
      {
        "session_id": session_id,
        "name": username,
        "data": data,
        "text": text
      }
    )
  })
    .then(function (response) {
      console.log("Reçu : " + response.status);
      return response.json();
    })
    .then(function (dict) {
      message = document.getElementById('message')
      if (message) {
        // prendre le premier element et l'affiche dans message
        message.innerHTML = "Vous êtes : " + dict[0][0]
        // afficher tous les éléments dans l'ordre sur la droite
        liste = document.getElementById('user_list')
        liste.innerHTML = ""
        for (const [key, value] of dict) {
          liste_item = document.createElement('li')
          liste_item.innerHTML = key + " : " + value + "%"
          liste.appendChild(liste_item)
        }
      }
    })
}

function valider() {
  if (document.cookie.length === 0) {
    window.location.href = '/enregistrement'
  }
  var name = document.getElementById('name').value
  if (name === "") {
    // affiche une popup d'erreur
    window.alert("Veuillez renseigner votre nom");
    return
  }
  send_data(document.cookie.substring(11), list_data);
  list_data = [];
  document.forms['text-form'].submit();
  window.location.href = '/validate'
}

function checkcaret() {
    const textarea = document.getElementById('text-input'); // Get the textarea element
    const newPos = textarea.selectionStart;
    return newPos;
}