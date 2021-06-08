import React, { useEffect, useState } from 'react';

import EditorJs from 'react-editor-js';
import Card from '@material-ui/core/Card';
import { Button, CardActions, CardContent, Checkbox, Dialog, FormControlLabel, FormGroup, Popover } from '@material-ui/core';
import Typography from '@material-ui/core/Typography';
import { useDispatch, useSelector } from 'react-redux'
import useStyles from '../../style';
import { closeEdit, openEdit } from './editSlice';
import { useRouteMatch, useHistory } from "react-router-dom";
import { addTagToNote, removeTagFromNote, updateNote } from './notesSlice';
import { setTag } from '../tags/tagSlice';
import getNoteAPI from '../utils/API/getNote';


function EditNoteTags(props) {
  const id = useSelector((state) => state.editnote.id)
  const tagged = useSelector((state) => state.editnote.tagged)
  const tags_obj = useSelector((state) => state.notes.tags)
  const tags = Object.keys(tags_obj)
  const initialState = tags.reduce(
    (acc, curr) => (tagged.includes(curr) ? acc[curr] = true : acc[curr] = false , acc), {}
  )
  const [tagMap, setTagMap] = useState(initialState)
  const [disableChange, setDisableChange] = useState(false)
  const openTag = useSelector((state) => state.tag.name)
  const dispatch = useDispatch()

  const handleChange = (event) => {
    if( event.target.name === openTag )
      dispatch(setTag(''))
    setTagMap({ ...tagMap, [event.target.name]: event.target.checked })
    if( event.target.checked === true ){
      dispatch(addTagToNote({ noteid: id, tag: event.target.name }))
    }
    else {
      dispatch(removeTagFromNote({ noteid: id, tag: event.target.name }))
    }      
  }

  return (
    <FormGroup>
      {Object.keys(tagMap).map((tag) => (
        <FormControlLabel
          disabled={disableChange}
          control={
            <Checkbox
              checked={tagMap[tag]}
              onChange={handleChange}
              name={tag}
            />
          }
          label={tag}
        />
      ))}
    </FormGroup>
  )
}


function GlobalEditNote(props) {
  const classes = useStyles();
  const instanceRef = React.useRef(null);
  const dispatch = useDispatch()
  const edit = useSelector((state) => state.editnote)

  const match = useRouteMatch("/id/:id");
  const history = useHistory();

  useEffect(() => {
    async function fetchGetNote() {
      if (match && !edit.open) {
        const response = await getNoteAPI(match.params.id)
        const data = await response.json()
        const dataFromResp = JSON.parse(data.note.data)
        dispatch(openEdit({ id:match.params.id, data: dataFromResp, tagged: data.tags }))
      }
    }
    fetchGetNote()
  },[]);

  const handleSave = (async () => {
    const savedData = await instanceRef.current.save()
    dispatch(updateNote({ id: edit.id, savedData: savedData }))
  });

  const handleClose = (() => {
    history.push("/")
    dispatch(closeEdit())
  });

  const [anchorEl, setAnchorEl] = useState(null)
  const handleOpenPopover = (event) => {
    setAnchorEl(event.currentTarget)
  }

  const handleClosePopover = () => {
    setAnchorEl(null)
  }


  const open = Boolean(anchorEl);
  const id = open ? 'popover-edit-tags' : undefined;



  return (
    <Dialog open={edit.open} onClose={handleClose}>
      <Card className={classes.edit}>
        <CardContent>
          <Typography >
            <EditorJs
              data={edit.data}
              instanceRef={instance => (instanceRef.current = instance)}
            />
          </Typography>

        </CardContent>
        <CardActions>
          <Button onClick={handleSave} variant="contained" color="primary">Save</Button>
          <Button
          onClick={handleOpenPopover}
          variant='contained'
          color='primary'
        >
          Edit Tags
        </Button>
        <Popover
          id={id}
          open={open}
          anchorEl={anchorEl}
          onClose={handleClosePopover}
          anchorOrigin={{
            vertical: 'bottom',
            horizontal: 'center',
          }}
          transformOrigin={{
            vertical: 'top',
            horizontal: 'center',
          }}
        >
          <EditNoteTags />
        </Popover>
        </CardActions>
      </Card>
    </Dialog>
  );
}

export default GlobalEditNote;