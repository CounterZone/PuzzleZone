import {load_split,load_code_editor,render_md,test_socket,display_log,codify} from './puzzle.js'
import jQuery from "jquery";
window.$ = window.jQuery = jQuery;
// this file is for solution and description sections


load_split();
$('#app_left').html(render_md(JSON.parse($('#app_left').text())));

var code_editor=load_code_editor();
var id=$('#q_attr').attr("q_id"); // the question id
var section=$('#q_attr').attr("sec");// the section. description/solution


function save(){

  // save the solution code to the local storage

  if(typeof(Storage)==undefined)
    return;
  window.localStorage.setItem(id+".solution",code_editor.getValue());
}


function load(){
  // load the solution code from the local storage

  if(typeof(Storage)==undefined)
    return;
  var sol=window.localStorage.getItem(id+".solution");
  if (sol)code_editor.setValue(sol,-1);
}
load();
window.addEventListener('beforeunload',save);





var ws=test_socket(id);


ws.onClose.addListener(event => {
$("#test_solution").prop('disabled',false);
});


ws.onMessage.addListener(msg => {
  var msg_json=JSON.parse(msg);
  if (msg_json['command']=='pass_sample_test') {

    $("#submit_solution").prop('disabled',false);
    display_log('You have passed the test! Please click "Submit" to submit your solution.');

}
  else if (msg_json['command']=='display')display_log(msg_json['message']);
else if (msg_json['command']=='fail_sample_test')display_log('You did not pass the test!');
else if (msg_json['command']=='submission_redirect')
window.location.href = "./submission/"+msg_json['message'];


});





function send_test(command){
  ws.close();
  $("#test_solution").prop('disabled',true);
  $("#submit_solution").prop('disabled',true);
  $('#app_right_bottom').html('');
  display_log('Connecting...');
  save();

  ws.open().then(
    ()=>{display_log('Connected.');
    ws.send(JSON.stringify({
              'command':command,
              'question_id':id,
              'solution': codify(code_editor.getValue())
          })
)});
}

$("#test_solution").on('click',()=>{
    send_test('sample_test');
});

$("#submit_solution").on('click',()=>{
    send_test('full_test');
});



$(document).ready(function() {
    $('#sec_'+section).addClass('active');
});
