import "bootstrap";
import 'bootstrap/dist/css/bootstrap.min.css';
import Split from "split-grid";
import {render_md} from './puzzle.js'

Split({
columnGutters: [{
  track: 1,
  element: document.querySelector('#column-gutter-1'),
}],
columnMinSize:200

});
$('#app_left').html(render_md($('#app_left').text()));
