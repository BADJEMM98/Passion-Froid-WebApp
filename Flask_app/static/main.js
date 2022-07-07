
/*  ==========================================
    SHOW UPLOADED IMAGE
* ========================================== */
function readURL(input) {
  if (input.files && input.files[0]) {
    var reader = new FileReader();

    reader.onload = function(e) {
      $('#imageResult')
        .attr('src', e.target.result);
    };
    reader.readAsDataURL(input.files[0]);
  }
}

$(function() {
  $('#app').on('change', function() {
    readURL(input);
  });
});

/*  ==========================================
    SHOW UPLOADED IMAGE NAME
* ========================================== */
var input = document.getElementById('upload');
var infoArea = document.getElementById('upload-label');

input.addEventListener('change', showFileName);

function showFileName(event) {
  var input = event.srcElement;
  var fileName = input.files[0].name;
  infoArea.textContent = 'File name: ' + fileName;
}



// const v = new Vue({
//   el: '#app',
//   template: `
//     <p>
//       <input type="file" accept="image/*" @change="uploadImage">
//       <img :src="previewImage" />
//     </p>
//   `,
//   data: {
//     previewImage: undefined
//   },
//   methods: {
//     uploadImage(e) {
//       const [image] = e.target.files;
//       const reader = new FileReader();
//       reader.readAsDataURL(image);
//       reader.onload = e => {
//         this.previewImage = e.target.result;
//         console.log(this.previewImage);
//       };
//     }
//   }
// })