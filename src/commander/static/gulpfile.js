'use strict';

var gulp = require('gulp');
var browserify = require('browserify');
var through = require('through2');
var globby = require('globby');
var source = require('vinyl-source-stream');
var buffer = require('vinyl-buffer');
var gutil = require('gulp-util');
var sourcemaps = require('gulp-sourcemaps');
var sass = require('gulp-sass');
var watch = require('gulp-watch');


gulp.task('css', function() {
    return gulp.src('css-dev/**/*.scss')
           .pipe(sass().on('error', sass.logError))
           .pipe(gulp.dest('./dist/css'));
});

gulp.task('javascript', function() {
  var b = browserify({
    entries: 'js-dev/main.js',
    debug: true
  });

  b.bundle()
    .pipe(source('app.js'))
    .pipe(buffer())
    .pipe(sourcemaps.init({loadMaps: true}))
        .on('error', gutil.log)
    .pipe(gulp.dest('dist/js/'));

  return b
});

gulp.task('watch', function() {
    gulp.watch('js-dev/**/*.js', ['javascript']);
    gulp.watch('css-dev/**/*.scss', ['css']);
});

gulp.task('default', ['watch']);
gulp.task('build', ['javascript', 'css']);

