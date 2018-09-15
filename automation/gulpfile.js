var gulp = require('gulp');
var rename = require("gulp-rename");
var sass = require('gulp-sass');
var cssnano = require('gulp-cssnano');

gulp.task('sass', function () {
    return gulp.src('../Sass/master.scss')
        .pipe(sass().on('error', sass.logError))
        .pipe(gulp.dest('../Sass'));
});

gulp.task('css', function () {
    return gulp.src('../Sass/master.css')
        .pipe(cssnano())
        .pipe(rename('master.min.css'))
        .pipe(gulp.dest('../Sass'));
});

gulp.task('automate', ['sass','css']);

gulp.task('watch', function () {
    gulp.watch('../Sass/master.scss', ['sass']);
    gulp.watch('../Sass/master.css', ['css']);
});

gulp.task('default', ['automate', 'watch']);