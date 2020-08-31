import Split from "split-grid";
import ace from "ace-builds";
import "bootstrap";
import 'bootstrap/dist/css/bootstrap.min.css';
import {ResizeSensor} from "css-element-queries";
import "ace-builds/src-noconflict/mode-python";
import WebSocketAsPromised from 'websocket-as-promised';
import jQuery from "jquery";

window.$ = window.jQuery = jQuery;

var MDit = require("markdown-it")();

$('[data-toggle="tooltip"]').tooltip()

export function load_split(){
  /*
 * load the split.js layout
 */

  Split({
  columnGutters: [{
    track: 1,
    element: document.querySelector('#column-gutter-1'),
  }],
  rowGutters: [{
    track: 2,
    element: document.querySelector('#row-gutter-1'),
  }]
});
}
export function load_code_editor(){
  /*
 * load the ace code editor to the right-top grid of the layout
 */
var init_txt= $('#app_right_top').text();

var code_editor=ace.edit("app_right_top");
code_editor.session.setMode("ace/mode/python");
code_editor.setFontSize("15px");
new ResizeSensor(document.getElementById('app_right_top'),function(){code_editor.resize();});

if (init_txt!='' && !( /^\s*$/.test(init_txt))){
  // only deal with non-empty text
var code=JSON.parse(init_txt);
code_editor.setValue(code,-1)
}

return code_editor;
}


export function render_md(text){

return MDit.render(text);

}
export function codify(code){
  /*

  make line breaks correctly encoded with /n

  */
  return JSON.stringify(code);

}


export function display_log(msg){
  for (var m of msg.split('\n')) if(m)
    $('#app_right_bottom').append('<p>>  '+m+'</p>');
  $('#app_right_bottom').scrollTop($('#app_right_bottom')[0].scrollHeight);// roll to the bottom
}

export function test_socket(){
  const testSocket = new WebSocketAsPromised(
    'ws://'
    + window.location.host
    + '/puzzle/'
);
return testSocket;
}
