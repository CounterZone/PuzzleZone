import "bootstrap";
import 'bootstrap/dist/css/bootstrap.min.css';
import Split from "split-grid";

Split({
columnGutters: [{
  track: 1,
  element: document.querySelector('#column-gutter-1'),
}],
columnMinSize:200

});
