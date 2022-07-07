const vm = new Vue({
  el: '#app',
  data() {
    return {
      url: null,
    }
  },
  methods: {
    onFileChange(e) {
      const file = e.target.files[0];
      this.url = URL.createObjectURL(file);
    }
  }
})


// /*  ==========================================
//     SHOW UPLOADED IMAGE
// * ========================================== */
// function readURL(input) {
//   if (input.files && input.files[0]) {
//     var reader = new FileReader();
//
//     reader.onload = function(e) {
//       $('#imageResult')
//         .attr('src', e.target.result);
//     };
//     reader.readAsDataURL(input.files[0]);
//   }
// }
//
// $(function() {
//   $('#app').on('change', function() {
//     readURL(input);
//   });
// });
//
// /*  ==========================================
//     SHOW UPLOADED IMAGE NAME
// * ========================================== */
//
// var input = document.getElementById('upload');
// var infoArea = document.getElementById('upload-label');
//
// input.addEventListener('change', showFileName);
//
// function showFileName(event) {
//   var input = event.srcElement;
//   var fileName = input.files[0].name;
//   infoArea.textContent = 'File name: ' + fileName;
// }


