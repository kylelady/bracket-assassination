module.exports = function(grunt) {

  // Project configuration.
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
    react: {
      lib: {
        expand: true,
        cwd: 'js/lib',
        src: ['*.jsx'],
        dest: 'build',
        ext: '.js'
      },
      pages: {
        expand: true,
        cwd: 'js',
        src: ['*.jsx'],
        dest: 'static/js',
        ext: '.js'
      }
    },
    concat: {
      lib: {
        src: ['build/*.js' ],
        dest: 'static/js/lib.js'
      }
    }
  })

  // Load the plugin that provides the "uglify" task.
  grunt.loadNpmTasks('grunt-react');
  grunt.loadNpmTasks('grunt-contrib-concat');

  // Default task(s).
  grunt.registerTask('default', ['react', 'concat']);

};