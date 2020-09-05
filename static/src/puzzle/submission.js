import {load_split,load_code_editor,render_md,test_socket,display_log,codify} from './puzzle.js'
import jQuery from "jquery";
import "bootstrap";
import 'bootstrap/dist/css/bootstrap.min.css';
window.$ = window.jQuery = jQuery;

var id=$('#q_attr').attr("q_id"); // the question id
var code_editor=load_code_editor();
code_editor.setReadOnly(true);

load_split();

{
let log=$('#app_right_bottom').html();
$('#app_right_bottom').html('');
let tmp = log.split('\n');

for (const line of tmp) {
  if (line.length>0)
    display_log(`${line}`);
  }
}
$(document).ready(function() {
    $('#sec_submission').addClass('active');
});
