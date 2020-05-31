const path = require('path');
const webpack =require('webpack');
module.exports = {
  entry:{'puzzle': './puzzle.js','puzzle_edit':'./edit.js','puzzle_display':'./display.js'},
  output: {
    filename: '[name].min.js',
    path: path.resolve(__dirname, 'dist'),
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
