function load(url, data, callback) {
  var xhr = new XMLHttpRequest();
  xhr.onreadystatechange = function() {
    if (xhr.readyState === 4) {
      try {
        callback(JSON.parse(xhr.response));
      } catch(e) {
        console.error(e)
      }
    }
  }
  xhr.open('POST', url, true);
  xhr.send(JSON.stringify(data));
}

function on_response(data) {
  console.log(data)


  ch = document.createElement('pre')
  ch.id = 'test-target'
  ch.textContent = JSON.stringify(data)
  document.body.appendChild(ch)
}

setTimeout(() => {
  load("/api", {"test": "data"}, on_response)
}, 1000);

