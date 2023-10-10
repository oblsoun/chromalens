
// get element by id message
const button = document.getElementById("submitBtn");
const file = document.getElementById("file");

// if button is clicked, check the file input
button.addEventListener("click", function (event) {
  if (file.files.length ==! 0) {
    img-src.innerHTML = file.name;
  }else{
  img-src.innerHTML = {% static 'images/default.png' %};
  }
});
