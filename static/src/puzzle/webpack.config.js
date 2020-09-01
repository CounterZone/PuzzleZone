const path = require('path');

module.exports = {
  entry:{'puzzle': './puzzle/puzzle.js',
  'edit':'./puzzle/edit.js',
  'display':'./puzzle/display.js',
  'puzzle_list':'./puzzle/puzzle_list.js',
  'submission':'./puzzle/submission.js',
  'sign_in':'./puzzle/sign_in.js',
  'profile':'./puzzle/profile.js'
  },
  output: {
    filename: '[name].min.js',
    path: path.resolve(__dirname, '../puzzle/dist'),
  },

  optimization: {
      splitChunks: {
        cacheGroups: {
        bundle: {
          name(module, chunks, cacheGroupKey) {
            return `${cacheGroupKey}`;
          },
          chunks: 'all'
        }
      }
      },
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
