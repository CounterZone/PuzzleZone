import {load_split,load_code_editor,render_md,test_socket,display_log} from './puzzle.js'
import jQuery from "../../lib/node_modules/jquery";
window.$ = window.jQuery = jQuery;
// this file is for edit
load_split();


var code_editor=load_code_editor();
var id=$('#q_attr').attr("q_id");
var q_name=$('#q_attr').attr("q_name");
var section=$('#q_attr').attr("sec");
var in_preview=false;

function save(){
  if(typeof(Storage)==undefined)
    return;
    if (q_name=='new')window.sessionStorage.setItem('1.name',$('#q_name').val());
  window.sessionStorage.setItem(id+'.'+section+'.code',code_editor.getValue());
  window.sessionStorage.setItem(id+'.'+section+'.text',$('#description_editor').val());
}
function load(){
  if(typeof(Storage)==undefined)
    return;
    if (q_name=='new')$("#q_name").val(window.sessionStorage.getItem('1.name'));
  var sol=window.sessionStorage.getItem(id+'.'+section+'.code');
  var des=window.sessionStorage.getItem(id+'.'+section+'.text');
  if (sol)code_editor.setValue(sol,-1);
  if (des)$('#description_editor').val(des);
}
load();
window.addEventListener('beforeunload',save);

$("#toggle_preview").on('click',()=>{{
  console.log('yyy');
  if (in_preview){
    $("#preview").hide();
    $("#description_editor").show();
    in_preview=false;
  }else{
    $("#description_editor").hide();
$("#preview").html(render_md($('#description_editor').val())).show();
in_preview=true;
  };
}});

function submit(draft){
  save();const fsec={"description":['edit','text'],"pre_solution":['edit','code'],"solution":['edit_solution','text'],"solution_code":['edit_solution','code'],"test_cases":['edit_test','text'],"test_code":['edit_test','code']};
  for (const k in fsec)
  $("#f_"+k).val(window.sessionStorage.getItem(id+"."+fsec[k][0]+'.'+fsec[k][1]));
  if (q_name=='new')$("#f_name").val(window.sessionStorage.getItem('1.name'));
  else $("#f_name").val($('#q_name').text());
  document.getElementById("f_isdraft").checked = draft;
  document.getElementById("q_form").submit();
}

$("#save_draft").on('click',()=>{submit(true)});

$("#submit_question").on('click',()=>{
  if (confirm("Once submitted, it cannot be editted. Are you sure?")) {
             submit(false);
         }
});


$(document).ready(function() {
    $('#sec_'+section).addClass('active');
});
