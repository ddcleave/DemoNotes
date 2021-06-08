import React from 'react';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemIcon from '@material-ui/core/ListItemIcon';
import ListItemText from '@material-ui/core/ListItemText';
import LabelIcon from '@material-ui/icons/Label';
import { useDispatch, useSelector } from 'react-redux'
import { setTag } from './tagSlice';


function TagItem(props) {
  return (
    <ListItem
      button
      key={props.label}
      selected={props.selected}
      onClick={(event) => props.handleClick(event, props.label)}
    >
      <ListItemIcon>
        <LabelIcon />
      </ListItemIcon>
      <ListItemText primary={props.label} />
    </ListItem>
  )
}



export default function TagList() {
  const tags = useSelector((state) => state.notes.tags)

  const openTag = useSelector((state) => state.tag.name)
  const dispatch = useDispatch()

  const handleAllClick = (event, label) => {
    dispatch(setTag(''))
  }

  const handleTagClick = (event, label) => {
    dispatch(setTag(label))
  }
  console.log(tags)

  return (
    <List>
      <TagItem
        label={'All'}
        selected={'' === openTag}
        handleClick={handleAllClick}
      />
      {Object.keys(tags).map((label) => (
        <TagItem
          key={label}
          label={label}
          selected={label === openTag}
          handleClick={handleTagClick}
        />
      ))}
    </List>
  )
}