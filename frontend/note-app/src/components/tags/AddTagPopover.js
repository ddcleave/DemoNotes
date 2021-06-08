import { Button, IconButton, makeStyles, Popover, TextField } from "@material-ui/core"
import { useState } from "react"
import * as yup from 'yup'
import { useFormik } from 'formik';
import AddIcon from '@material-ui/icons/Add';
import { createTag } from "../note/notesSlice";
import { useDispatch, useSelector } from "react-redux";

const useStyles = makeStyles((theme) => ({
  createTag: {
    display: "flex"
  },
  ButtonCreateTag: {
    width: "100%"
  }
}))

const validationSchema = yup.object({
  tag: yup
    .string()
    .min(1, 'Tag should be of minimum 1 characters length')
    .max(20, 'Tag should be of maximum 20 characters length')
    .required('Tag is required'),
});

function FormCreateTag() {
  const classes = useStyles();
  const dispatch = useDispatch()
  const tags = useSelector((state) => state.notes.tags)
  const formik = useFormik({
    initialValues: {
      tag: ''
    },
    validationSchema: validationSchema,
    validate: (values => {
      const errors = {}
      if (values.tag in Object.keys(tags)) {
          errors.tag = 'Tag already exists'
      }
      return errors
    }),
    onSubmit: ((values) => {
      dispatch(createTag(values.tag))
    })
  });

  return (
    <form onSubmit={formik.handleSubmit} className={classes.createTag}>
      <TextField
        fullWidth
        id="tag"
        name="tag"
        label="Tag"
        value={formik.values.tag}
        onChange={formik.handleChange}
        error={formik.touched.tag && Boolean(formik.errors.tag)}
        helperText={formik.touched.tag && formik.errors.tag}
        autoComplete="off"
      />
      <IconButton color="secondary" variant="contained" type="submit" >
        <AddIcon />
      </IconButton>
    </form>
  )
}

export default function CreateTagButtonAndPopover() {
  const classes = useStyles();
  const [anchorEl, setAnchorEl] = useState(null)
  const open = Boolean(anchorEl)
  const id = open ? 'popover-create-tag' : undefined


  const handleOpenPopover = (event) => {
    setAnchorEl(event.currentTarget)
  }

  const handleClose = () => {
    setAnchorEl(null)
  }

  return (
    <div>
      <Button
        className={classes.ButtonCreateTag}
        variant="contained"
        onClick={handleOpenPopover}
        startIcon={<AddIcon />}
      >
        Create Tag
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
        <FormCreateTag />
      </Popover>
    </div>
  )
}