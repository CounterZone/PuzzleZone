import Split from "../../lib/node_modules/split-grid";
import ace from "../../lib/node_modules/ace-builds";
import "../../lib/node_modules/bootstrap";
import '../../lib/node_modules/bootstrap/dist/css/bootstrap.min.css';
import {ResizeSensor} from "../../lib/node_modules/css-element-queries";
import "../../lib/node_modules/ace-builds/src-noconflict/mode-python";
import WebSocketAsPromised from '../../lib/node_modules/websocket-as-promised';

var MDit = require("../../lib/node_modules/markdown-it")();

export function load_split(){
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
var code_editor=ace.edit("app_right_top");
code_editor.session.setMode("ace/mode/python");
new ResizeSensor(document.getElementById('app_right_top'),function(){code_editor.resize();});
return code_editor;
}


export function render_md(text){
return MDit.render(text);
}



export function display_log(msg){
  $('#app_right_bottom').append('<p> > '+msg+'</p>');
  $('#app_right_bottom').scrollTop($('#app_right_bottom')[0].scrollHeight);

}

export function test_socket(id){
  const testSocket = new WebSocketAsPromised(
    'ws://'
    + window.location.host
    + '/puzzle/'+id
);



return testSocket;
}
