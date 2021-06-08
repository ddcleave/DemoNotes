import React, { useRef, useState } from 'react';

import EditorJs from 'react-editor-js';
import Card from '@material-ui/core/Card';
import { Button, CardActions, CardContent, Checkbox, FormControlLabel, FormGroup, makeStyles, Popover } from '@material-ui/core';
import Typography from '@material-ui/core/Typography';
import { useDispatch, useSelector } from 'react-redux'
import { addNote } from './notesSlice';

const useStyles = makeStyles((theme) => ({
  CreatePaper: {
    width: 600
  }
}))


function CheckboxTags(props) {
  const { tagMap, handleChange } = props

  return (
    <FormGroup>
      {Object.keys(tagMap).map((tag) => (
        <FormControlLabel
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


function CreateNote(props) {
  const classes = useStyles()
  const tags_obj = useSelector((state) => state.notes.tags)
  const tags = Object.keys(tags_obj)
  const initialState = tags.reduce(
    (acc, curr) => (acc[curr] = false, acc), {}
  )
  const [tagMap, setTagMap] = useState(initialState)
  const handleChange = (event) => {
    setTagMap({ ...tagMap, [event.target.name]: event.target.checked })
  }

  const instanceRef = useRef(null);
  const dispatch = useDispatch()

  const handleSave = (async () => {
    const savedData = await instanceRef.current.save()
    const add_tags = Object.entries(tagMap).reduce(
      (newArr, el) => {
        if (el[1] === true)
          newArr.push(el[0])
        return newArr
      }, [])
    dispatch(addNote({ savedData: savedData, tags: add_tags }))
    props.close()
  })

  const [anchorEl, setAnchorEl] = useState(null)
  const handleOpenPopover = (event) => {
    setAnchorEl(event.currentTarget)
  }

  const handleClose = () => {
    setAnchorEl(null)
  }


  const open = Boolean(anchorEl);
  const id = open ? 'popover-add-tags' : undefined;

  return (
    <Card className={classes.CreatePaper}>
      <CardContent>
        <Typography >
          <EditorJs
            instanceRef={instance => (instanceRef.current = instance)}
            placeholder={'Take a note'}
          />
        </Typography>

      </CardContent>
      <CardActions>
        <Button onClick={handleSave} variant='contained' color='primary'>
          Save
        </Button>
        <Button
          onClick={handleOpenPopover}
          variant='contained'
          color='primary'
        >
          Add Tags
        </Button>
        <Popover
          id={id}
          open={open}
          anchorEl={anchorEl}
          onClose={handleClose}
          anchorOrigin={{
            vertical: 'bottom',
            horizontal: 'center',
          }}
          transformOrigin={{
            vertical: 'top',
            horizontal: 'center',
          }}
        >
          <CheckboxTags tagMap={tagMap} handleChange={handleChange} />
        </Popover>
      </CardActions>
    </Card>
  );
}

export default CreateNote;