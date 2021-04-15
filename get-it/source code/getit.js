function getRandomInt(min, max) {
  min = Math.ceil(min);
  max = Math.floor(max);
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

document.addEventListener("DOMContentLoaded", function () {
  // Faz textarea aumentar a altura automaticamente
  // Fonte: https://www.geeksforgeeks.org/how-to-create-auto-resize-textarea-using-javascript-jquery/#:~:text=It%20can%20be%20achieved%20by,height%20of%20an%20element%20automatically.
  let textareas = document.getElementsByClassName("autoresize");
  for (let i = 0; i < textareas.length; i++) {
    let textarea = textareas[i];
    function autoResize() {
      this.style.height = "auto";
      this.style.height = this.scrollHeight + "px";
    }

    textarea.addEventListener("input", autoResize, false);
  }

  // Sorteia classes de cores aleatoriamente para os cards
  let cards = document.getElementsByClassName("card");
  for (let i = 0; i < cards.length; i++) {
    let card = cards[i];
    card.className += ` card-color-${getRandomInt(
      1,
      5
    )} card-rotation-${getRandomInt(1, 11)}`;
  }
});

// #################################################################################################

// const editables = document.querySelectorAll("[contenteditable]");

// // save edits
// editables.forEach(el => {
//   el.addEventListener("blur", () => {
//     localStorage.setItem("dataStorage-" + el.id, el.innerHTML);
//   })
// });

function editNote(id) {
	var title = document.getElementsByName('id_title-' + id)[0].innerText
	var content = document.getElementsByName('id_content-' + id)[0].innerText
	document.getElementsByName("form-btn")[0].innerText = "Atualizar"
	document.getElementsByName('edit_note_id')[0].value = id
	document.getElementsByName('titulo')[0].value = title
	document.getElementsByName('detalhes')[0].value = content
}

window.onbeforeunload = function resetEdit() {
  document.getElementsByName('edit_note_id')[0].value = ""
  document.getElementsByName('titulo')[0].value = ""
	document.getElementsByName('detalhes')[0].value = ""
}