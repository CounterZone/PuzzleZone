import Split from "../../lib/node_modules/split-grid";
import ace from "../../lib/node_modules/ace-builds";
import "../../lib/node_modules/bootstrap";
import '../../lib/node_modules/bootstrap/dist/css/bootstrap.min.css';
import {ResizeSensor} from "../../lib/node_modules/css-element-queries";
import "../../lib/node_modules/jquery";
import "../../lib/node_modules/ace-builds/src-noconflict/mode-javascript";
import "../../lib/node_modules/bootstrap-markdown/js/bootstrap-markdown.js";
import "../../lib/node_modules/bootstrap-markdown/css/bootstrap-markdown.min.css";

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
function load_code_editor(){
var code_editor=ace.edit("app_right_top");
code_editor.session.setMode("ace/mode/javascript");
new ResizeSensor(document.getElementById('app_right_top'),function(){code_editor.resize();});
};

function load_md_editor(){

}

load_code_editor();
