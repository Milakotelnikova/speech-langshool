import gulp from 'gulp';
import plumber from 'gulp-plumber';
import dartSass from 'sass';
import htmlmin from 'gulp-htmlmin';
import gulpSass from 'gulp-sass';
import autoprefixer from 'gulp-autoprefixer';
import groupMedia from 'gulp-group-css-media-queries';
import gulpIf from 'gulp-if';
import del from 'del';
import webpackStream from 'webpack-stream';
import sync from 'browser-sync';
import imagemin from 'gulp-imagemin';
import rename from 'gulp-rename';
import fileinclude from 'gulp-file-include';
import cleanCss from 'gulp-clean-css';
import newer from 'gulp-newer';
import webp from 'imagemin-webp';
import fonter from 'gulp-fonter';
import ttf2woff from 'gulp-ttf2woff';
import ttf2woff2 from 'gulp-ttf2woff2';

import path from 'path';
import { fileURLToPath } from 'url';

import fs from 'fs';

const scss = gulpSass(dartSass);
const __dirname = path.dirname(fileURLToPath(import.meta.url));
const src_folder = 'src';
const dist_folder = 'dist';

const isBuild = process.argv.includes('--build');
const isDev = !process.argv.includes('--build');

// Path
const _path = {
  build: {
    html: dist_folder + '/',
    js: dist_folder + '/js/',
    css: dist_folder + '/css/',
    images: dist_folder + '/img/',
    fonts: dist_folder + '/fonts/',
    iconfonts: dist_folder + '/iconfonts/',
    videos: dist_folder + '/videos/',
    favicon: dist_folder + '/',
  },
  src: {
    html: [src_folder + '/**/*.html', '!' + src_folder + '/_*.html'],
    js: src_folder + '/js/*.js',
    css: [src_folder + '/scss/style.scss', src_folder + '/scss/iconfonts.scss'],
    images: [src_folder + '/img/**/*.{jpg,png,svg,gif,ico,webp,avif}', '!**/favicon.*'],
    fonts: src_folder + '/fonts/*.ttf',
    iconfonts: src_folder + '/iconfonts/*.{ttf,svg,eot,woff}',
    videos: src_folder + '/videos/*.*',
    favicon: [
      src_folder + '/img/favicon.{jpg,png,svg,gif,ico}',
      src_folder + '/favicon.ico',
      src_folder + '/manifest.json',
    ],
  },
  watch: {
    html: src_folder + '/**/*.html',
    js: src_folder + '/**/*.js',
    css: src_folder + '/scss/**/*.scss',
    images: src_folder + '/img/**/*.{jpg,png,svg,gif,ico,webp,avif}',
  },
  clean: './' + dist_folder + '/',
};

// Scripts
export const scripts = () => {
  //Webpack configuration
  const webPackConfig = {
    watch: false,
    entry: {
      app: './src/js/app.js',
    },
    output: {
      filename: '[name].min.js',
      publicPath: '/js/',
    },
    module: {
      rules: [
        {
          test: /\.js$/,
          loader: 'babel-loader',
          include: path.join(__dirname, 'src/js'),
        },
        {
          test: /\.css$/,
          use: ['style-loader', 'css-loader'],
        },
      ],
    },
    mode: isDev ? 'development' : 'production',
    //https://webpack.js.org/configuration/devtool/
    devtool: isDev ? 'eval-source-map' : false,
  };

  return gulp
    .src(_path.src.js)
    .pipe(plumber())
    .pipe(webpackStream(webPackConfig))
    .pipe(gulp.dest(_path.build.js))
    .pipe(sync.stream());
};

// html
export const html = () => {
  return gulp
    .src(_path.src.html, {})
    .pipe(plumber())
    .pipe(fileinclude())
    .pipe(
      gulpIf(
        isBuild,
        htmlmin({
          removeComments: true,
          collapseWhitespace: true,
        }),
      ),
    )
    .pipe(gulp.dest(_path.build.html))
    .pipe(sync.stream());
};

//favicon
export const favicon = () => {
  return gulp
    .src(_path.src.favicon)
    .pipe(plumber())
    .pipe(gulp.dest(_path.build.favicon))
    .pipe(sync.stream());
};

//iconfonts
export const iconfonts = () => {
  return gulp
    .src(_path.src.iconfonts)
    .pipe(plumber())
    .pipe(gulp.dest(_path.build.iconfonts))
    .pipe(sync.stream());
};

// Styles
export const styles = () => {
  return gulp
    .src(_path.src.css)
    .pipe(plumber())
    .pipe(scss({ outputStyle: 'expanded' }).on('error', scss.logError))
    .pipe(groupMedia())
    .pipe(
      autoprefixer({
        grid: true,
        cascade: true,
      }),
    )
    .pipe(gulp.dest(_path.build.css))
    .pipe(cleanCss())
    .pipe(
      rename({
        extname: '.min.css',
      }),
    )
    .pipe(gulp.dest(_path.build.css))
    .pipe(sync.stream());
};

// Images
export const images = () => {
  return gulp
    .src(_path.src.images)
    .pipe(plumber())
    .pipe(newer(_path.build.images))
    .pipe(
      imagemin([
        webp({
          quality: 75,
        }),
      ]),
    )
    .pipe(
      rename({
        extname: '.webp',
      }),
    )
    .pipe(gulp.dest(_path.build.images))
    .pipe(gulp.src(_path.src.images))
    .pipe(newer(_path.build.images))
    .pipe(
      imagemin({
        progressive: true,
        svgoPlugins: [{ removeViewBox: false }],
        interlaced: true,
        optimizationLevel: 3, //0 to 7
      }),
    )
    .pipe(gulp.dest(_path.build.images));
};

// Clean
export const clean = () => {
  return del(_path.clean);
};

// Fonts: otf to ttf convert
export const fontsOtf2ttf = () => {
  return gulp
    .src('./' + src_folder + '/fonts/*.otf')
    .pipe(plumber())
    .pipe(
      fonter({
        formats: ['ttf'],
      }),
    )
    .pipe(gulp.dest('./' + src_folder + '/fonts/'));
};

// Fonts: convert ttf to woff, woff2
export const fonts = () => {
  return gulp
    .src(_path.src.fonts)
    .pipe(plumber())
    .pipe(ttf2woff())
    .pipe(gulp.dest(_path.build.fonts))
    .pipe(gulp.src(_path.src.fonts))
    .pipe(ttf2woff2())
    .pipe(gulp.dest(_path.build.fonts))
    .pipe(gulpIf(isDev, sync.stream()));
};

// Fonts: insert fonts into styles file
export const fontsInclude = (cb) => {
  const fileContent = src_folder + '/scss/fonts.scss';

  if (fs.readFileSync(fileContent) !== '') {
    fs.writeFile(fileContent, '', cb);
  }

  fs.readdir(_path.build.fonts, (err, items) => {
    if (items) {
      let c_fontname;
      for (let i = 0; i < items.length; i++) {
        let fontname = items[i].split('.');
        fontname = fontname[0];
        if (c_fontname != fontname) {
          fs.appendFile(
            fileContent,
            '@include font("' + fontname + '", "' + fontname + '", "400", "normal");\r\n',
            cb,
          );
        }
        c_fontname = fontname;
      }
    }
  });
};

// Server
export const server = () => {
  sync.init({
    ui: false,
    notify: false,
    server: {
      baseDir: './' + dist_folder + '/',
    },
  });
};

// Watch
export const watch = () => {
  gulp.watch(_path.watch.html, html);
  gulp.watch(_path.watch.css, styles);
  gulp.watch(_path.watch.js, scripts);
  gulp.watch([_path.watch.images], images);
};

export const build = gulp.series(
  clean,
  gulp.parallel(favicon, html, styles, scripts, iconfonts, images),
  fontsOtf2ttf,
  fonts,
  fontsInclude,
);

export default gulp.series(build, gulp.parallel(server, watch));


