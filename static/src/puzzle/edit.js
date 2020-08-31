import {load_split,load_code_editor,render_md,test_socket,display_log,codify} from './puzzle.js'
import jQuery from "jquery";
window.$ = window.jQuery = jQuery;
// this file is for edit
load_split();

const fsec={"description":['edit','text'],"pre_solution":['edit','code'],"solution":['edit_solution','text'],"solution_code":['edit_solution','code'],"test_cases":['edit_test','text'],"test_code":['edit_test','code']};

var code_editor=load_code_editor();
var default_code=code_editor.getValue();

var id=$('#q_attr').attr("q_id");
var q_name=$('#q_attr').attr("q_name");
var section=$('#q_attr').attr("sec");
var in_preview=false;
$('#description_editor').val(JSON.parse($('#description_editor').val()));



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
  save();

  for (const k in fsec)
  $("#f_"+k).val(codify(window.sessionStorage.getItem(id+"."+fsec[k][0]+'.'+fsec[k][1])));

  if (q_name=='new')$("#f_name").val(window.sessionStorage.getItem('1.name'));
  else $("#f_name").val($('#q_name').text());

  document.getElementById("f_isdraft").checked = draft;
  document.getElementById("q_form").submit();
}


var ws=test_socket(id);


ws.onClose.addListener(event => {
$("#test_question").prop('disabled',false);
});


ws.onMessage.addListener(msg => {
  var msg_json=JSON.parse(msg);
  if (msg_json['command']=='display')display_log(msg_json['message']);
});

function send_test(){
  ws.close();
  $('#app_right_bottom').html('');
  display_log('Connecting...');
  save();
  ws.open().then(
    ()=>{display_log('Connected.');
    ws.send(JSON.stringify({
              'command':'question_test',
              'question_id':id,
          })
)});
}



$("#save_draft").on('click',()=>{submit(true)});


$("#test_question").on('click',()=>{
  // todo
});


$("#submit_question").on('click',()=>{
  if (confirm("Once submitted, it cannot be editted. Are you sure?")) {
             submit(false);
         }
});


$("#return_default").on('click',()=>{
code_editor.setValue(default_code)
});














$(document).ready(function() {
    $('#sec_'+section).addClass('active');
});
