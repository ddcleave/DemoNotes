import { makeStyles } from '@material-ui/core/styles';


const drawerWidth = 240;

const useStyles = makeStyles((theme) => ({
  root: {
    display: 'flex',
  },
  icon: {
    marginRight: theme.spacing(2),
  },
  heroContent: {
    backgroundColor: theme.palette.background.paper,
    padding: theme.spacing(8, 0, 6),
  },
  heroButtons: {
    marginTop: theme.spacing(4),
  },
  cardGrid: {
    paddingTop: theme.spacing(8),
    paddingBottom: theme.spacing(8),
  },
  card: {
    height: '100%',
    display: 'flex',
    flexDirection: 'column',
    overflow: 'hidden',
    maxHeight: '200px',
    position: "relative",
    minWidth: '200px'
  },
  cardContent: {
    flexGrow: 1,
  },
  footer: {
    backgroundColor: theme.palette.background.paper,
    padding: theme.spacing(6),
  },
  appBar: {
    // zIndex: theme.zIndex.tooltip
    zIndex: 1201,
  },
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
  },
  paper: {
    position: 'absolute',
    width: 600,
    top: '50%',
    left: '50%',
    transform: 'translate(-50%, -50%)',
  },
  toolbar: {
    position: "absolute",
    bottom: "0%",
    right: "0%"
  },
  edit: {
    width: 600
  },
  loginButton: {
    marginTop: "30px"
  },
  loginTitle: {
    textAlign: "center"
  },
  appBarTitle: {
    flexGrow: 1
  },
  appBarButton: {
    color: '#FFF'
  },
  progress: {
    position: "absolute",
    top: "50%",
    left: "50%"
  },
  sidebarAndMain: {
    display: "flex"
  },
  main: {
    width: "calc(100vw - 240px)"
  }
}));

export default useStyles;