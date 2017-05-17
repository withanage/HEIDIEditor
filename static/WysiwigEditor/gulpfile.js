var gulp = require('gulp');
var cleanCSS = require('gulp-clean-css');
var concat = require('gulp-concat');
var concatCss = require('gulp-concat-css');
var cssmin = require('gulp-minify-css')


gulp.task('concat-css', function () {
    return gulp.src(
        [   'src/css/*.css',
            './bower_components/bootstrap/dist/css/bootstrap.min.css',
            './bower_components/bootstrap-additions/dist/bootstrap-additions.min.css',
            './bower_components/font-awesome/css/font-awesome.css',
            './bower_components/jstree/dist/themes/default/style.css',
            './bower_components/angular-xeditable/dist/css/xeditable.css'

        ]
    )
        .pipe(concat("styles/main.css"))
        .pipe(gulp.dest('dist/'));
});

gulp.task('copy-fonts', function (){
    return gulp.src(['src/fonts/*'])
        .pipe(gulp.dest('dist/fonts/'));
});

ulp.task('scripts', function() {
    gulp.src(['./lib/file3.js', './lib/file1.js', './lib/file2.js'])
        .pipe(concat('all.js'))
        .pipe(uglify())
        .pipe(gulp.dest('./dist/'))
});




gulp.task('default',
    ['concat-css','copy-fonts']
);

