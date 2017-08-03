module.exports = function(grunt) {

  // Project configuration.
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
    copy: {
      main: {
        files: [
          {
            expand: true,
            cwd: 'bower_components/bootstrap/dist/',
            src: ['css/*.min.css', 'fonts/*', 'js/*.min.js'],
            dest: 'bookmarks/static/bootstrap/'
          },
          {
            expand: true,
            cwd: 'bower_components/jquery/dist/',
            src: 'jquery.min.js',
            dest: 'bookmarks/static/jquery/'
          },
        ],
      },
    },
  });

  grunt.loadNpmTasks('grunt-contrib-copy');

  // Default task(s).
  grunt.registerTask('default', ['copy']);

};
