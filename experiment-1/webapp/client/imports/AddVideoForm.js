import React, {Component, PropTypes} from 'react';
import {reduxForm} from 'redux-form';

class AddVideoForm extends Component {
  render() {
    const {
      fields: {url, isLargelyObjectionable},
      handleSubmit
    } = this.props;

    return (
      <form onSubmit={handleSubmit}>
        <div>
          <label>Link to YouTube video</label>
          <div>
            <input type="text" placeholder="https://youtube.com/" {...url} />
          </div>
        </div>
        <div>
          <div>
            <label>
              <input type="radio" {...isLargelyObjectionable} value={"y"}
                checked={isLargelyObjectionable.value === 'y'}/>
              BUZZ!!
            </label>

            <label>
              <input type="radio" {...isLargelyObjectionable} value={""}
                checked={isLargelyObjectionable.value === ''}/>
              ...yawn...
            </label>
          </div>
        </div>

        <div>
          <button type="submit">
            Add
          </button>
        </div>
      </form>
    );
  }
}

export default reduxForm({
  form: 'addVideo',
  fields: ['url', 'isLargelyObjectionable']
})(AddVideoForm);
