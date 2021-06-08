import { Button, Dialog, Divider, Drawer } from "@material-ui/core"
// import useStyles from "../../style"
import AddIcon from '@material-ui/icons/Add'
import { useState } from "react";
import CreateNote from "../note/CreateNote";
import TagList from "../tags/TagList";
import CreateTagButtonAndPopover from "../tags/AddTagPopover";
import { makeStyles } from '@material-ui/core/styles';

const drawerWidth = 240;

const useStyles = makeStyles((theme) => ({
  drawer: {
    width: drawerWidth,
    flexShrink: 0,
  },
  drawerPaper: {
    width: drawerWidth,
  },
  button: {
    marginTop: theme.spacing(10),
    marginBottom: theme.spacing(1),
    marginLeft: theme.spacing(3),
    marginRight: theme.spacing(3),
  }
}));
export default function Sidebar() {
  const classes = useStyles()
  const [open, setOpen] = useState(false);

  const handleOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  return (
    <>
      <Drawer
        className={classes.drawer}
        variant="permanent"
        classes={{
          paper: classes.drawerPaper,
        }}
      >
        <Button
          variant="contained"
          color="secondary"
          onClick={handleOpen}
          className={classes.button}
          startIcon={<AddIcon />}
        >
          Create
        </Button>
        <Dialog open={open} onClose={handleClose} >
          <CreateNote close={handleClose} />
        </Dialog>
        <TagList />
        <CreateTagButtonAndPopover />
      </Drawer>
    </>
  )
}