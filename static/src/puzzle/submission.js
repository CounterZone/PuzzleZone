import {load_split,load_code_editor,render_md,test_socket,display_log,codify} from './puzzle.js'
import jQuery from "jquery";
window.$ = window.jQuery = jQuery;

var id=$('#q_attr').attr("q_id"); // the question id
var code_editor=load_code_editor();
code_editor.setReadOnly(true);

load_split();


$(document).ready(function() {
    $('#sec_submission').addClass('active');
});
