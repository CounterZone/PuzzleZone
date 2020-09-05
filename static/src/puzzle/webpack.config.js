const path = require('path');

module.exports = {
  context: path.resolve(__dirname),
  entry:{'puzzle': './puzzle.js',
  'edit':'./edit.js',
  'display':'./display.js',
  'puzzle_list':'./puzzle_list.js',
  'submission':'./submission.js',
  'sign_in':'./sign_in.js',
  'profile':'./profile.js'
  },
  resolve: {
    modules: ['node_modules']
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
    rules:[
            {
                test: /\.js$/,
                use: {
                    loader: 'babel-loader',
                    options:{
                        presets: ['@babel/preset-react']
                    }
                }
            },
            {
                test: /\.(sass|scss|css)$/,
                use: ['style-loader','css-loader','sass-loader']
            },
            {
                test: /\.(svg|eot|woff|woff2|ttf)$/,
                loader: 'file-loader',
                options: {
                publicPath: '/static/src/puzzle/dist'
            }
            }
        ]
  }
};
// todo: remove duplications
