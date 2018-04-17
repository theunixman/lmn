    $(function () {
      var image = document.getElementById('image');
      var cropBoxData;
      var canvasData;
      var cropper;

     /* SCRIPT TO OPEN THE MODAL WITH THE PREVIEW */
      $("#id_file").change(function () {
        if (this.files && this.files[0]) {
          var reader = new FileReader();
          reader.onload = function (e) {
            $("#image").attr("src", e.target.result);
            $("#modal").modal("show");
          }
          reader.readAsDataURL(this.files[0]);
        }
      });

      $('#modal').on('shown.bs.modal', function () {
        cropper = new Cropper(image, {
          autoCrop: true,
          aspectRatio: 1/1,
          minCropBoxWidth: 200,
          minCropBoxHeight: 200,
          autoCropArea: 0.5,
          ready: function () {

            // Strict mode: set crop box data first
            cropper.setCropBoxData(cropBoxData).setCanvasData(canvasData);
          }
        });
      }).on('hidden.bs.modal', function () {
        cropBoxData = cropper.getCropBoxData();
        canvasData = cropper.getCanvasData();
        $("#id_x").val(cropBoxData["left"]);
        $("#id_y").val(cropBoxData["top"]);
        $("#id_height").val(cropBoxData["height"]);
        $("#id_width").val(cropBoxData["width"]);
        cropper.destroy();
      });
    });