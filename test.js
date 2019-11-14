some TextDecoderStream
another test

gulp.task('webserver', function() {
  connect.server({
    livereload: true
  });
});

gulp.task('default', ['webserver']);