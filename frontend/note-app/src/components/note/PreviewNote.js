import CardActionArea from '@material-ui/core/CardActionArea';
import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';
import EditorJs from 'react-editor-js';
import useStyles from '../../style';
import { useState } from "react";
import CardActions from "@material-ui/core/CardActions";
import IconButton from "@material-ui/core/IconButton";
import DeleteIcon from "@material-ui/icons/Delete";
import { useDispatch } from 'react-redux'
import { openEdit } from './editSlice';
import { useHistory } from 'react-router';
import { deleteNote } from './notesSlice';


export default function PreviewNote(props) {
  const { id, datanote, tagged } = props
  const classes = useStyles();
  const [toolbarVis, setToolbarVis] = useState("hidden")
  const dispatch = useDispatch()
  const history = useHistory()

  const onMouseEnter = () => {
    setToolbarVis("visible")
  };
  const onMouseLeave = () => {
    setToolbarVis("hidden")
  };

  const handleDelete = (async () => {
    dispatch(deleteNote(id))
  })

  const handleClickOpenEdit = (() => {
    dispatch(openEdit({id:id, data:datanote, tagged: tagged}))
    history.push(`/id/${id}`)
  })

  return (
    <>
    <Card onMouseEnter={onMouseEnter}
      onMouseLeave={onMouseLeave}
      className={classes.card}
    >
      <CardActionArea onClick={handleClickOpenEdit}>
        <CardContent className={classes.cardContent}>
          <EditorJs data={datanote} readOnly={true} />
        </CardContent>
      </CardActionArea>
      <CardActions
        className={classes.toolbar}
        style={{ visibility: toolbarVis, zIndex: 2 }}
      >
        <IconButton
            color="secondary"
            aria-label="delete"
            onClick={handleDelete}
        >
            <DeleteIcon fontSize="large" />
        </IconButton>
      </CardActions>
    </Card>
    </>
  );
}