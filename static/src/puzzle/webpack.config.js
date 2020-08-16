const path = require('path');

module.exports = {
  entry:{'puzzle': './puzzle/puzzle.js',
  'puzzle_edit':'./puzzle/edit.js',
  'puzzle_display':'./puzzle/display.js',
  'puzzle_list':'./puzzle/puzzle_list.js',
  'puzzle_submission':'./puzzle/submission.js'

},
  output: {
    filename: '[name].min.js',
    path: path.resolve(__dirname, '../puzzle/dist'),
  },

  optimization: {
        minimize: false
    },

  module:{
    rules: [
          {
            test: /\.css$/,
            use: ['style-loader', 'css-loader']
          }
        ]
  }
};
// todo: remove duplications
