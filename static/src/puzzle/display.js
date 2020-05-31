import {load_split,load_code_editor,render_md} from './puzzle.js'
import jQuery from "../../lib/node_modules/jquery";
window.$ = window.jQuery = jQuery;
// this file is for solution and description sections


load_split();
$('#app_left').html(render_md($('#app_left').text()));

var code_editor=load_code_editor();
var id=$('#q_attr').attr("q_id");
var section=$('#q_attr').attr("sec");

function save(){
  if(typeof(Storage)==undefined)
    return;
  window.localStorage.setItem(id+".solution",code_editor.getValue());
}
function load(){
  if(typeof(Storage)==undefined)
    return;
  var sol=window.localStorage.getItem(id+".solution");
  if (sol)code_editor.setValue(sol,-1);
}
load();


window.addEventListener('beforeunload',save);
$(document).ready(function() {
    $('#sec_'+section).addClass('active');
});
