const path = require('path');
const webpack =require('webpack');
module.exports = {
  entry: './puzzle.js',
  output: {
    filename: 'puzzle.min.js',
    path: path.resolve(__dirname, 'dist'),
  },
  plugins: [
   new webpack.ProvidePlugin({
     $: "jquery",
     jQuery: "jquery"
   })
 ],
  module:{
    rules: [
          {
            test: /\.css$/,
            use: ['style-loader', 'css-loader']
          }
        ]
  }
};
