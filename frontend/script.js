// function runCode() {
//     const code = editor.getValue();
//     const language = document.getElementById('language').value;
//     const input = document.getElementById('input').value;

//     fetch('http://localhost:8000/api/run/', {
//         method: 'POST',
//         headers: { 'Content-Type': 'application/json' },
//         body: JSON.stringify({ code, language, input })
//     })
//     .then(response => response.json())
//     .then(data => {
//         document.getElementById('output').innerText = data.output;
//     })
//     .catch(error => {
//         document.getElementById('output').innerText = 'Error: ' + error;
//     });
// }

// let editor = CodeMirror.fromTextArea(document.getElementById("code"), {
//     lineNumbers: true,
//     mode: "python",
//     theme: "default"
// });
let editor = CodeMirror.fromTextArea(document.getElementById("editor"), {
  lineNumbers: true,
  mode: "python",
  theme: "default"
});

document.getElementById("language").addEventListener("change", function () {
  const lang = this.value;
  const modeMap = {
    python: "python",
    c: "text/x-csrc",
    cpp: "text/x-c++src",
    java: "text/x-java",
    php: "text/x-php",
    javascript: "javascript"
  };
  editor.setOption("mode", modeMap[lang]);
});

function runCode() {
  const code = editor.getValue();
  const input = document.getElementById("input").value;
  const language = document.getElementById("language").value;

  fetch("/api/run/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ code, input, language })
  })
  .then(res => res.json())
  .then(data => {
    document.getElementById("output").textContent = data.output || data.error;
  })
  .catch(err => {
    document.getElementById("output").textContent = "Error: " + err;
  });
}
